"""What the compiler does to a literal, before your program ever runs."""

import itertools
import re
import warnings

# Escape processing happens at COMPILE time, so a literal that would warn
# cannot simply be written here -- the warning would fire when this file is
# read, not where the lesson is. Sections 4 and 6 build their source text at
# run time out of chr(92) and hand it to eval(), which is also the only way to
# show an invalid escape without the file itself containing one.
BS = chr(92)
warnings.simplefilter("ignore")


def literal(source):
    """Compile one string-literal source and return its value."""
    return eval(source, {})


def compiles(source):
    """True when `source` is a valid string literal."""
    try:
        literal(source)
    except SyntaxError:
        return False
    return True


print("1. NINE PREFIXES, AND THE ONES THAT DO NOT EXIST")
letters = "rbfu"
candidates = [""] + list(letters) + ["".join(p) for p in itertools.permutations(letters, 2)]
valid, invalid = [], []
for prefix in candidates:
    try:
        valid.append((prefix, type(literal(prefix + '"x"')).__name__))
    except SyntaxError:
        invalid.append(prefix)
print(f"     {'prefix':<10} {'type':<8} what it changes")
print("     " + "-" * 62)
MEANING = {
    "": "nothing -- this is the plain form",
    "r": "backslash sequences are NOT interpreted",
    "b": "the result is bytes; source must be ASCII",
    "f": "braces are expressions, evaluated at run time",
    "u": "nothing at all -- a no-op kept for 2-to-3 ports",
    "rb": "both of the above",
    "br": "both, spelled the other way round",
    "rf": "raw and f, which do compose",
    "fr": "the same, other order",
}
for prefix, kind in valid:
    shown = repr(prefix) if prefix else "'' (none)"
    print(f"     {shown:<10} {kind:<8} {MEANING[prefix]}")
print()
print(f"     {len(valid)} valid, {len(invalid)} rejected: {' '.join(sorted(invalid))}")
print("     Read the rejected list as two rules. 'u' combines with nothing --")
print("     it is a compatibility no-op and was never meant to be useful. And")
print("     'b' and 'f' cannot meet: an f-string is built at run time out of")
print("     str pieces, and there is no such thing as an f-bytes literal.")
upper = ['B"x"', 'R"x"', 'F"x"', 'U"x"', 'Rb"x"', 'BR"x"', 'bR"x"', 'RB"x"']
print(f"     Case does not matter: {sum(map(compiles, upper))} of {len(upper)} "
      "uppercase spellings compile,")
print("     B'x' and Rb'x' and BR'x' among them.")

print("\n2. FIVE LITERAL SPELLINGS OF ONE NUMBER, AND ONE THAT IS NOT PYTHON")
spellings = [
    ("the character itself", "'é'", "é"),
    ("hex escape, 2 digits", "'\\xe9'", "\xe9"),
    ("hex escape, 4 digits", "'\\u00e9'", "\u00e9"),
    ("hex escape, 8 digits", "'\\U000000e9'", "\U000000e9"),
    ("by name", "'\\N{LATIN SMALL LETTER E WITH ACUTE}'", "\N{LATIN SMALL LETTER E WITH ACUTE}"),
    ("built at run time", "chr(0xE9)", chr(0xE9)),
]
print(f"     {'how':<22} {'written':<40} value  len")
print("     " + "-" * 72)
for label, written, value in spellings:
    print(f"     {label:<22} {written:<40} {value}      {len(value)}")
print()
print(f"     all six are the same object value: {len({v for _, _, v in spellings}) == 1}")
print("     U+00E9 is a sixth notation and it is NOT Python syntax. It is the")
print("     Unicode standard's way of NAMING the code point; 0xE9 is an integer")
print("     literal that happens to equal it; and 'é' is source text. Same")
print("     number, three jobs -- and only two of the three are code.")

print("\n3. TWO NUMERIC ESCAPES, TWO DIFFERENT WIDTHS")
print(f"     {'literal':<16} {'value':<12} {'len':<5} why")
print("     " + "-" * 66)
rows = [
    ("'\\x41'", "\x41", "exactly two hex digits, always"),
    ("'\\xA1A'", "\xA1A", "the A is data -- \\x stopped after two"),
    ("'\\101'", "\101", "octal, and 101 octal is 65"),
    ("'\\1010'", "\1010", "octal took three digits, then '0' is data"),
    ("'\\10'", "\10", "octal will take one, two or three"),
    ("'\\0'", "\0", "NUL -- and it is octal zero, not a special case"),
]
for written, value, why in rows:
    print(f"     {written:<16} {value!r:<12} {len(value):<5} {why}")
print()
print("     Python has one fixed-width numeric escape and one greedy one, in")
print("     the same grammar. '\\x' can never swallow a following hex digit;")
print("     '\\NNN' can, and does. If you write octal at all, write all three")
print("     digits -- which is the same advice other languages have to give")
print("     about their \\x, because theirs is the greedy one.")

print("\n4. AN UNKNOWN ESCAPE IS KEPT, NOT REJECTED -- AND THAT IS THE TRAP")
print(f"     {'source':<10} {'value':<12} backslash survived?")
print("     " + "-" * 48)
for name in "dwsbAZnt":
    source = BS + name
    value = literal('"' + source + '"')
    print(f"     {source!r:<10} {value!r:<12} {value == source}")
print()
print("     Five of those eight are regex syntax that arrives at re intact")
print("     purely because Python did not recognise them. '\\b' is the")
print("     exception, and it is the one every real pattern uses:")
cooked = literal('"' + BS + "bfoo" + BS + 'b"')
raw = literal('r"' + BS + "bfoo" + BS + 'b"')
text = "a foo b"
for label, pattern in (("cooked", cooked), ("raw   ", raw)):
    match = re.search(pattern, text)
    print(f"     {label} pattern {pattern!r:<14} on {text!r} -> {match.span() if match else None}")
print()
print("     The cooked pattern asked for a BACKSPACE character on both sides")
print("     of 'foo' and found nothing. It did not raise; it just never")
print("     matches. This is the whole reason regex patterns are written r''")
print("     -- not style, and not about the backslashes you can see.")
print("     Since Python 3.12 an unrecognised escape is a SyntaxWarning, and")
print("     it is documented as becoming an error in a future release. Until")
print("     then '\\d' works and '\\b' silently does not.")

print("\n5. RAW DOES NOT MEAN 'NO BACKSLASH RULES'")
raw_quote = literal('r"' + BS + '""')
print(f"     r'{BS}\"'  is {raw_quote!r}, length {len(raw_quote)}")
print("     -- the backslash still escaped the quote, so the string did not")
print("        end there. It just also stayed in the result.")
try:
    literal('r"' + BS + '"')
    ending = "accepted"
except SyntaxError as exc:
    ending = type(exc).__name__
print(f"     a raw literal ending in ONE backslash -> {ending}")
print("     So a raw string cannot end in an odd number of backslashes, which")
print("     is why r'C:\\Users\\' does not compile and every Windows path")
print("     example ends one character short of where you wanted it.")
raw_u = literal('r"' + BS + 'u0041"')
print(f"     And a code-point escape is not one either: r'{BS}u0041' is "
      f"{raw_u!r}, {len(raw_u)} characters.")

print("\n6. A bytes LITERAL IS ASCII-ONLY, AND HAS A SMALLER ESCAPE SET")
print(f"     {'escape':<32} {'in a str':<14} in a bytes")
print("     " + "-" * 62)
for esc in ["n", "x41", "101", "u0041", "U00000041", "N{LATIN CAPITAL LETTER A}"]:
    source = BS + esc
    as_str = literal('"' + source + '"')
    as_bytes = literal('b"' + source + '"')
    print(f"     {source!r:<32} {as_str!r:<14} {as_bytes!r}")
print()
try:
    literal('b"é"')
    non_ascii = "accepted"
except SyntaxError as exc:
    non_ascii = type(exc).__name__
print(f"     b'e-acute' written directly -> {non_ascii}")
print("     The three that survive as text are the three that name a CODE")
print("     POINT, and a byte does not have one. So they are not escapes")
print("     inside a bytes literal at all -- they stay as a backslash and a")
print("     letter, and since 3.12 they warn. A bytes literal is ASCII-only")
print("     no matter what encoding the source file declares, because it is")
print("     spelling out bytes and the source encoding is not one of them.")

print("\n7. TWO STRINGS SIDE BY SIDE ARE ONE STRING")
joined = "spam" "eggs"
print(f"     'spam' 'eggs'  ->  {joined!r}, length {len(joined)}")
print("     Adjacent literals are concatenated by the COMPILER, so there is")
print("     no run-time cost and no '+' -- which is how a long literal gets")
print("     wrapped over several lines inside brackets.")
menu = [
    "spam",
    "eggs"
    "beans",
    "toast",
]
print(f"     a list with one comma missing -> {menu}")
print(f"     len(menu) is {len(menu)}, and nobody typed a concatenation.")
print("     That is the cost of the feature: a missing comma in a list of")
print("     strings is not a syntax error, it is a shorter list. Linters look")
print("     for it precisely because the language cannot.")
print()
print("     (No answer above depends on which Python you ran it under: this")
print("      grammar has been this shape since 3.6, and the file prints the")
print("      same bytes on 3.11, 3.12, 3.13 and 3.14.)")
