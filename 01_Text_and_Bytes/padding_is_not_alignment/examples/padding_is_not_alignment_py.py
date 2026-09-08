"""Five methods that pad, five specs that duplicate them, and the column they
all get wrong.

Every width here is derived from the Unicode character database that ships with
Python (`unicodedata`), never from the terminal this happens to run in -- a
lesson whose output depends on the reader's font is not a lesson.
"""

import struct
import unicodedata as ud

# The model every terminal implements some version of. East_Asian_Width 'W'
# (Wide) and 'F' (Fullwidth) take two cells; a combining mark or a format
# character takes none, because it is drawn onto its neighbour rather than
# beside it. 'A' (Ambiguous) is the interesting one and gets its own column.
ZERO_WIDTH = ("Mn", "Me", "Cf")


def cells(text, ambiguous=1):
    """Terminal cells this string asks for, under a stated model."""
    total = 0
    for ch in text:
        if ud.category(ch) in ZERO_WIDTH:
            continue
        eaw = ud.east_asian_width(ch)
        if eaw in ("W", "F"):
            total += 2
        elif eaw == "A":
            total += ambiguous
        else:
            total += 1
    return total


def pad_to_cells(text, width):
    """ljust, but counting cells instead of code points."""
    return text + " " * max(0, width - cells(text))


print("1. FIVE PAIRS: A METHOD, AND THE SPEC THAT DUPLICATES IT")
print("     the value is 'ab', the field is 6 wide, so four characters to place")
print()
print("     method                   spec                     result     agree?")
print("     " + "-" * 63)
for m_call, m_out, f_call, f_out in [
    ("'ab'.ljust(6)", "ab".ljust(6), "format('ab', '<6')", format("ab", "<6")),
    ("'ab'.rjust(6)", "ab".rjust(6), "format('ab', '>6')", format("ab", ">6")),
    ("'ab'.center(6)", "ab".center(6), "format('ab', '^6')", format("ab", "^6")),
    ("'ab'.ljust(6, '.')", "ab".ljust(6, "."), "format('ab', '.<6')", format("ab", ".<6")),
    ("'42'.zfill(6)", "42".zfill(6), "format(42, '06d')", format(42, "06d")),
]:
    print("     %-24s %-24s %-10r %s"
          % (m_call, f_call, m_out, "yes" if m_out == f_out else "NO"))
print()
print("     Five names for one job. The methods came first; the mini-language")
print("     arrived with str.format and absorbed them. Nothing was removed, so")
print("     both spellings are still here and both are still correct. On these")
print("     inputs they agree exactly -- sections 4 and 5 are where they stop.")
print("     expandtabs is the one method with no spec at all: the mini-language")
print("     has no tab-stop slot, so there is nothing for it to have absorbed.")

print()
print("2. NOT ONE OF THE FIVE TRUNCATES")
name = "Bartholomew"
print("     'Bartholomew' is %d characters, and every field below asks for 6:"
      % len(name))
print()
print("     call                          result           length")
print("     " + "-" * 55)
for label, out in [
    ("'Bartholomew'.ljust(6)", name.ljust(6)),
    ("'Bartholomew'.rjust(6)", name.rjust(6)),
    ("'Bartholomew'.center(6)", name.center(6)),
    ("'Bartholomew'.zfill(6)", name.zfill(6)),
    ("format('Bartholomew', '<6')", format(name, "<6")),
]:
    print("     %-29s %-16r %d" % (label, out, len(out)))
print()
print("     ljust(6) does not even copy -- it returns the same object: %s"
      % (name.ljust(6) is name))
print()
print("     So a 'fixed-width' column built from these is not fixed width. It is")
print("     a MINIMUM width, and one long value makes the whole table ragged")
print("     without raising anything. Two things in the standard library do cut:")
print()
for label, cut in [
    ("format('Bartholomew', '<6.6')", format(name, "<6.6")),
    ("struct.pack('6s', b'Bartholomew')", struct.pack("6s", name.encode())),
    ("struct.pack('6s', b'ab')", struct.pack("6s", b"ab")),
]:
    print("     %-34s %-21r %d wide, always" % (label, cut, len(cut)))

print()
print("3. THE PADDING IS COUNTED IN CODE POINTS; A TERMINAL LAYS OUT CELLS")
composed = "Łódź"
samples = [
    (composed, "Latin-2, composed"),
    (ud.normalize("NFD", composed), "the same word, decomposed"),
    ("日本", "CJK"),
    ("ＡＢ", "fullwidth Latin"),
    ("\U0001f44d", "emoji"),
    ("\U0001f469‍\U0001f4bb", "emoji, ZWJ sequence"),
    ("Reid", "ASCII, for scale"),
]
print("     len() is the number every method on this page pads to. The two right")
print("     columns are what the character database says the string occupies.")
print()
print("     string                        len()   cells   cells if 'A' is wide")
print("     " + "-" * 68)
for text, note in samples:
    print("     %-29s %5d %7d %13d   %s"
          % (ascii(text), len(text), cells(text), cells(text, 2), note))
print()
print("     ljust(10), then a bar, so the ragged edge is visible:")
print()
for text, _ in samples:
    padded = text.ljust(10)
    print("       [%s]  padding added %d, cells %2d" % (padded, 10 - len(text), cells(padded)))
print()
print("     The same list padded by CELLS instead of by code points:")
print()
for text, _ in samples:
    print("       [%s]" % pad_to_cells(text, 10))
print()
print("     Nothing in the standard library computes that second column.")
print("     unicodedata.east_asian_width is the raw material; the model at the")
print("     top of this file -- W and F are two cells, combining marks are zero")
print("     -- is a convention, and the convention has two holes of its own:")
print()
print("     Hole 1: 'A' means AMBIGUOUS, and two of the four letters in Łódź are")
print("     in it.")
for ch in composed[:2]:
    print("       %-10s %-40s EAW=%s"
          % (ascii(ch), ud.name(ch), ud.east_asian_width(ch)))
print("     One cell in a Western terminal, two in a legacy East Asian one. The")
print("     string does not carry the answer; the terminal's configuration does.")
print()
zwj = "\U0001f469‍\U0001f4bb"
print("     Hole 2: East_Asian_Width predates emoji sequences.")
for ch in zwj:
    print("       %-14s %-40s EAW=%s"
          % (ascii(ch), ud.name(ch), ud.east_asian_width(ch)))
print("     The model scores that at %d cells -- two Wide characters, joiner"
      % cells(zwj))
print("     skipped -- but a terminal that supports the sequence draws ONE glyph,")
print("     two cells wide. So the column-aware padding above is wrong too, just")
print("     less often. There is no correct answer inside the standard library.")

print()
print("4. center AND ^ DISAGREE ABOUT WHERE THE ODD SPACE GOES")
print("     'ab' -- an even length -- in fields of every width from 3 to 9")
print()
print("     width   'ab'.center(w)     format('ab', '^w')")
print("     " + "-" * 51)
for w in range(3, 10):
    centred = "ab".center(w)
    spec = format("ab", "^" + str(w))
    print(("     %5d   %-18r %-18r %s"
           % (w, centred, spec, "" if centred == spec else "<- DIFFER")).rstrip())
print()
print("     center's tiebreak reads the parity of BOTH numbers. CPython computes")
print("     left = margin // 2 + (margin & width & 1), so the spare space goes")
print("     LEFT when margin and width are both odd. The format spec has no such")
print("     rule: '^' always puts pad // 2 on the left and the remainder on the")
print("     right. Two spellings of 'centre this', one apart, in exactly the case")
print("     where centring is genuinely ambiguous.")

print()
print("5. zfill IS SIGN-AWARE, AND THE SPEC THAT LOOKS LIKE IT IS NOT")
print()
print("     input      zfill(5)   what it did")
print("     " + "-" * 57)
for value, note in [
    ("-42", "sign kept in front, zeros behind it"),
    ("+4", "'+' is a sign too"),
    ("42", "no sign, so the zeros go all the way"),
    ("-", "a lone sign is still a sign"),
    ("--42", "only the FIRST character is a sign"),
    ("a-42", "not at position 0, so not a sign"),
    ("-4.2", "it never looks at what follows"),
    ("", "an empty string is five zeros"),
]:
    print("     %-10r %-10r %s" % (value, value.zfill(5), note))
print()
print("     Four ways to ask for 'five wide, zero padded', and three answers:")
print()
print("       '-42'.zfill(5)         %-8r the sign is found and kept in place"
      % "-42".zfill(5))
print("       format(-42, '05d')     %-8r the int agrees with zfill"
      % format(-42, "05d"))
print("       format('-42', '0>5')   %-8r fill='0', align='>': padding, no sign"
      % format("-42", "0>5"))
print("       format('-42', '05')    %-8r and this one is a different bug"
      % format("-42", "05"))
print()
print("     The last line is the trap. On an int, a '0' before the width is a")
print("     flag meaning 'pad after the sign'. On a str there is no sign to pad")
print("     after, so the '0' degrades to a plain fill character -- and the")
print("     default alignment for a str is LEFT, which puts the zeros on the")
print("     wrong end of the number. zfill is '{:05d}' for a value that is")
print("     already text, and it is that for no other spelling.")

print()
print("6. expandtabs IS COLUMN ARITHMETIC, NOT REPLACEMENT")
line = "01\t012\t0123"
print("     %s.expandtabs(4)" % ascii(line))
print("       -> %s" % ascii(line.expandtabs(4)))
print()
print("     Two spaces, then one. A tab is not N spaces; it is 'advance to the")
print("     next multiple of N', so what one expands to depends on everything")
print("     in front of it on the line:")
print()
print("     piece    column before   next stop   spaces written")
print("     " + "-" * 51)
column = 0
tabs = line.count("\t")
for index, piece in enumerate(line.split("\t")):
    before = column + len(piece)
    if index < tabs:
        stop = before + (4 - before % 4)
        print("     %-8r %13d %11d %14d" % (piece, before, stop, stop - before))
        column = stop
    else:
        print("     %-8r %13d %11s %14s" % (piece, before, "-", "-"))
print()
print("     tabsize    'a\\tb'.expandtabs(n)")
for size in (8, 4, 1, 0, -1):
    print("     %7d    %s" % (size, ascii("a\tb".expandtabs(size))))
print("     Zero and negative delete the tab rather than raising.")
print()
print("     It counts characters, so it misses a wide column for exactly the")
print("     reason ljust does -- the next tab stop after 'X' should be cell 4:")
print()
for text in ("ab", "日本", "\U0001f44d"):
    expanded = (text + "\tX").expandtabs(4)
    landed = cells(expanded) - 1
    print(("       %-22s -> %-24s X lands at cell %d %s"
           % (ascii(text + "\tX"), ascii(expanded), landed,
              "" if landed == 4 else "<- not 4")).rstrip())
print()
print("     And what resets the column back to zero is a shorter list than you")
print("     would guess from splitlines:")
print()
print("     separator             expandtabs resets?   splitlines() splits?")
print("     " + "-" * 62)
for sep, sep_name in [
    ("\n", "LINE FEED"),
    ("\r", "CARRIAGE RETURN"),
    ("\v", "LINE TABULATION"),
    ("\f", "FORM FEED"),
    ("\x1c", "FILE SEPARATOR"),
    ("\x85", "NEXT LINE"),
    (" ", "LINE SEPARATOR"),
    (" ", "PARAGRAPH SEPARATOR"),
]:
    probe = "abcdef" + sep + "x\ty"
    tail = probe.expandtabs(4).split(sep)[-1]
    resets = "yes" if tail == "x   y" else "no"
    splits = "yes" if len(("a" + sep + "b").splitlines()) == 2 else "no"
    print("     %-21s %-20s %s" % (sep_name, resets, splits))
print()
print("     Two against eight. Every separator here begins a new line as far as")
print("     splitlines is concerned; only LF and CR begin one as far as the tab")
print("     stops are concerned.")

print()
print("7. ON bytes THE METHODS SURVIVE AND THE BRACES DO NOT")
print("     b'ab'.ljust(5, b'.')      %r" % b"ab".ljust(5, b"."))
print("     b'-42'.zfill(5)           %r" % b"-42".zfill(5))
print("     b'01\\t012'.expandtabs(4)  %s" % ascii(b"01\t012".expandtabs(4)))
print("     b'%%-5s|' %% b'ab'          %r" % (b"%-5s|" % b"ab"))
try:
    format(b"ab", "<5")
except TypeError as exc:
    print("     format(b'ab', '<5')       %s" % type(exc).__name__)
print()
print("     str.format and f-strings do not exist on bytes, so for binary output")
print("     the padding methods and % are the whole toolbox. That is the honest")
print("     answer to 'why are there two ways to do this': one of the two still")
print("     works on the type the other one never learned.")
