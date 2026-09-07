"""Ten line boundaries in str, three in a file, one in a regex -- one library."""

import io
import re
import unicodedata as ud

# The C0 controls and the two Unicode separators that are candidates for
# "this ends a line". US is here as the control: it is the one member of the
# information-separator family that splitlines() does NOT split on.
NAMES = {
    0x000A: ("LF", "LINE FEED"),
    0x000B: ("VT", "LINE TABULATION"),
    0x000C: ("FF", "FORM FEED"),
    0x000D: ("CR", "CARRIAGE RETURN"),
    0x001C: ("FS", "INFORMATION SEPARATOR FOUR (file)"),
    0x001D: ("GS", "INFORMATION SEPARATOR THREE (group)"),
    0x001E: ("RS", "INFORMATION SEPARATOR TWO (record)"),
    0x001F: ("US", "INFORMATION SEPARATOR ONE (unit)"),
    0x0085: ("NEL", "NEXT LINE"),
    0x2028: ("LS", "LINE SEPARATOR"),
    0x2029: ("PS", "PARAGRAPH SEPARATOR"),
}


def splits(ch: str) -> bool:
    """Does this one character break 'a<ch>b' into two lines?"""
    return len(("a" + ch + "b").splitlines()) > 1


print("1. EVERY CODE POINT, AND THE TEN THAT SPLIT")
scanned = 0
boundaries = []
for cp in range(0x110000):
    if 0xD800 <= cp <= 0xDFFF:            # surrogates are not characters
        continue
    scanned += 1
    if splits(chr(cp)):
        boundaries.append(cp)
print(f"     Scanned {scanned:,} code points. {len(boundaries)} of them end a line:")
print()
print(f"     {'':<5} {'code point':<11} {'bidi':<5} {'isspace':<8} name")
print("     " + "-" * 66)
for cp in boundaries:
    short, full = NAMES[cp]
    print(f"     {short:<5} U+{cp:04X}      {ud.bidirectional(chr(cp)):<5} "
          f"{str(chr(cp).isspace()):<8} {full}")
print()
print("     Plus one two-character sequence: CR LF counts once, not twice.")
print("     And one near miss -- U+001F, unit separator, is whitespace to")
print("     isspace() and a separator to split(), and is not a line boundary.")

print("\n2. THE SAME TEXT, THREE ANSWERS")
text = "a\nb\x0bc\rd\x1ce\x85f g"
raw = text.encode("utf-8")
by_method = text.splitlines()
by_file = io.TextIOWrapper(io.BytesIO(raw), encoding="utf-8").readlines()
by_regex = re.findall(r"(?m)^.*", text)
print(f"     text = {text!r}")
print("     Seven pieces, separated by six different candidates: LF VT CR FS NEL LS.")
print()
print(f"     text.splitlines()        {len(by_method)} lines  {by_method}")
print(f"     iterating those bytes    {len(by_file)} lines  {by_file}")
print(f"     re.findall('^.*', re.M)  {len(by_regex)} lines  {by_regex}")
print()
print("     Nothing about the text changed. str.splitlines() knows ten")
print("     boundaries, universal newlines knows three (LF, CR, CRLF), and")
print("     re knows exactly one -- \\n -- even in MULTILINE mode.")

print("\n3. WHERE THE TEN COME FROM")
bidi_b = [cp for cp in range(0x110000)
          if not (0xD800 <= cp <= 0xDFFF) and ud.bidirectional(chr(cp)) == "B"]
extra = [cp for cp in boundaries if cp not in bidi_b]
missing = [cp for cp in bidi_b if cp not in boundaries]
print(f"     Bidi_Class B ('paragraph separator') holds {len(bidi_b)} code points:")
print("       " + "  ".join(f"U+{cp:04X}" for cp in bidi_b))
print(f"     Of those, {len(missing)} are missing from splitlines().")
print(f"     splitlines() adds {len(extra)}: "
      + ", ".join(f"U+{cp:04X} {NAMES[cp][1]}" for cp in extra))
print()
print("     So the rule is: every character Unicode's bidirectional algorithm")
print("     calls a paragraph separator, plus vertical tab, form feed and")
print("     LINE SEPARATOR. FS, GS and RS are in the set because Unicode")
print("     puts them there -- they were ASCII's file, group and record")
print("     separators, and Unicode classifies all three as paragraph ends.")

print("\n4. bytes.splitlines() KNOWS TWO")
byte_boundaries = [i for i in range(256)
                   if len((b"a" + bytes([i]) + b"b").splitlines()) > 1]
print("     Over all 256 byte values, bytes.splitlines() splits on: "
      + ", ".join(f"0x{i:02X}" for i in byte_boundaries))
print(f"     b'a\\r\\nb'.splitlines() = {b'a\r\nb'.splitlines()}   (CRLF, still one)")
print()
print(f"     {'':<5} {'as str':<10} as utf-8 bytes")
print("     " + "-" * 40)
for cp in (0x0B, 0x1E, 0x85):
    s = "a" + chr(cp) + "b"
    print(f"     {NAMES[cp][0]:<5} {len(s.splitlines()):<10} "
          f"{len(s.encode('utf-8').splitlines())}")
print()
print("     A bytes object does not know which table produced it, so it")
print("     answers for ASCII only. Decode first and the answer changes.")

print("\n5. THE CODEC DECIDES WHETHER THERE IS A LINE THERE")
ebcdic = "amount".encode("cp037") + b"\x15" + "date".encode("cp037")
print(f"     {'codec':<10} {'decodes to':<20} lines")
print("     " + "-" * 44)
for data, codec in [(b"amount\x85date", "latin-1"),
                    (b"amount\x85date", "cp1252"),
                    (b"amount\x85date", "cp437"),
                    (ebcdic, "cp037")]:
    decoded = data.decode(codec)
    print(f"     {codec:<10} {decoded!r:<20} {len(decoded.splitlines())}")
print()
print(f"     The first three read the same bytes: {b'amount\x85date'!r}")
print(f"     The fourth is EBCDIC:                {ebcdic!r}")
print()
print("     Byte 0x85 is NEXT LINE in latin-1, a horizontal ellipsis in")
print("     cp1252 and an a-grave in cp437. Same byte, same file, and only")
print("     the codec you passed to .decode() decides whether your data has")
print("     two lines or one. The last row is why NEL is in the set at all:")
print("     byte 0x15 is the mainframe's newline, and cp037 maps it to U+0085.")

print("\n6. splitlines() IS NOT split('\\n')")
print(f"     {'input':<16} {'splitlines()':<26} split('\\n')")
print("     " + "-" * 62)
for s in ["", "a", "a\n", "a\n\n", "a\r\nb", "a\x0bb"]:
    print(f"     {s!r:<16} {str(s.splitlines()):<26} {s.split(chr(10))}")
print()
crlf = "a\r\nb"
print(f"     keepends=True on {crlf!r}: {crlf.splitlines(keepends=True)}")
print("     splitlines() treats a trailing terminator as ending the last")
print("     line rather than starting an empty one, and returns [] for the")
print("     empty string where split() returns ['']. That difference is why")
print("     a file's last line does not arrive twice -- and why reaching for")
print("     split('\\n') to dodge the FS problem adds a phantom empty line.")
