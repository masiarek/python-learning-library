"""'Printable' does not mean 'makes ink'. It means repr() will not escape it."""

import string
import sys
import unicodedata
from fractions import Fraction

TAB = "\t"
NL = "\n"
CR = "\r"
VT = "\x0b"
FF = "\x0c"

print("1. TWO FUNCTIONS, TWO QUESTIONS")
print("     str(x)  -- 'show this to a person'   -> characters, no quotes")
print("     repr(x) -- 'show this to a Python programmer'")
print("     ascii(x) is repr(x) with every non-ASCII character escaped.")
print()
print(f"     {'object':<22} {'repr(x)':<22} ascii(x)")
print("     " + "-" * 62)
for value in ["a", "é", "\U0001F638", TAB, b"Zoot!", Fraction(1, 3)]:
    label = repr(value) if not isinstance(value, Fraction) else "Fraction(1, 3)"
    print(f"     {label:<22} {repr(value):<22} {ascii(value)}")
print()
print("     The bytes row is the one to stare at: repr and ascii agree,")
print("     and str() -- which is not in this table for a reason -- gives")
print("     the same thing again. Section 5.")
print("     The cat row does not line up, and that is not a bug in this")
print("     table: the columns were padded with ljust, which counts code")
print("     points, and that glyph is one code point two columns wide.")

print("\n2. WHAT 'PRINTABLE' ASKS, CHECKED OVER ALL 1,114,112 CODE POINTS")
print("     The docs rule: printable = General_Category in L, M, N, P or S,")
print("     plus the ASCII space U+0020. Everything else (Z, C) is not.")
disagree = 0
z_printable = []
not_zc = 0
for cp in range(0x110000):
    ch = chr(cp)
    cat = unicodedata.category(ch)
    rule = cat[0] in "LMNPS" or cp == 0x20
    if ch.isprintable() != rule:
        disagree += 1
    if ch.isprintable():
        if cat[0] == "Z":
            z_printable.append(cp)
    elif cat[0] not in "ZC":
        not_zc += 1
print(f"     code points where isprintable() disagrees with that rule:  {disagree}")
print(f"     non-printable code points that are NOT in Z or C:          {not_zc}")
names = ", ".join(f"U+{cp:04X} {unicodedata.name(chr(cp))}" for cp in z_printable)
print(f"     separator characters that ARE printable:  {names}")
print()
print("     Three families that are non-printable and never change size:")
for cat, human in (("Cc", "control"), ("Cs", "surrogate"), ("Co", "private use")):
    n = sum(1 for cp in range(0x110000) if unicodedata.category(chr(cp)) == cat)
    print(f"       {cat}  {human:<12} {n:>9,}")
print("     Cf (format) and Cn (unassigned) are left uncounted on purpose:")
print("     both move with the Unicode version, and two Pythons on one")
print("     machine are routinely built against different editions of the")
print("     table. Print unicodedata.unidata_version to see yours.")

print("\n3. SO A SPACE IS PRINTABLE AND A TAB IS NOT")
samples = [
    ("''", ""),
    ("' '", " "),
    ("'\\t'", TAB),
    ("'\\n'", NL),
    ("'\\u00a0' NO-BREAK SPACE", " "),
    ("'\\u3000' IDEOGRAPHIC SPACE", "　"),
]
print(f"     {'string':<28} {'isprintable()':<14} isspace()")
print("     " + "-" * 54)
for label, text in samples:
    print(f"     {label:<28} {str(text.isprintable()):<14} {text.isspace()}")
print()
print("     Printable and whitespace are not opposites. U+0020 is both --")
print("     it is the single exception written into the rule -- and every")
print("     other space character in Unicode is whitespace and not printable.")
print("     The empty string is printable for the same vacuous reason it is")
print("     not isspace(): no character in it is non-printable.")

print("\n4. string.printable IS NOT PRINTABLE")
parts = [
    ("digits", string.digits),
    ("ascii_letters", string.ascii_letters),
    ("punctuation", string.punctuation),
    ("whitespace", string.whitespace),
]
for name, value in parts:
    n_bad = sum(1 for c in value if not c.isprintable())
    print(f"     string.{name:<15} {len(value):>3} characters, {n_bad} not printable")
bad = [c for c in string.printable if not c.isprintable()]
print(f"     string.printable        {len(string.printable):>3} characters, {len(bad)} not printable")
print(f"     the five:               {' '.join(repr(c) for c in bad)}")
print(f"     string.printable.isprintable()  ->  {string.printable.isprintable()}")
print()
print("     Two different words, one spelling. string.printable is the")
print("     POSIX sense -- 'characters a terminal can handle' -- and it")
print("     includes the whitespace that moves the cursor. str.isprintable()")
print("     is the repr() sense, and repr() escapes exactly those five.")

print("\n5. str(bytes) IS THE QUIET ONE")
b = b"Zoot!"
print(f"     b                      {b!r:<12} len {len(b)}")
print(f"     str(b)                 {str(b)!r:<12} len {len(str(b))}   <- the repr, as text")
print(f"     str(b, 'utf-8')        {str(b, 'utf-8')!r:<12} len {len(str(b, 'utf-8'))}   <- a decode")
print(f"     b.decode()             {b.decode()!r:<12} len {len(b.decode())}")
print()
print("     Same function, two signatures, and the one with no encoding")
print("     silently gives you a string with 'b' and two quotes in it.")
print(f"     sys.flags.bytes_warning on this run: {sys.flags.bytes_warning}")
print("     Run the file again as `python3 -b` and that becomes 1, and")
print("     str(b) raises a BytesWarning. `-bb` makes it an error.")

print("\n6. !s, !r AND !a IN A FORMAT STRING")
one_third = Fraction(1, 3)
text = "¡kočka \U0001F638!"
rows = [
    ("f'{one_third}'", f"{one_third}"),
    ("f'{one_third!s}'", f"{one_third!s}"),
    ("f'{one_third!r}'", f"{one_third!r}"),
    ("f'{one_third = }'", f"{one_third = }"),
    ("f'{text!a}'", f"{text!a}"),
]
for label, produced in rows:
    print(f"     {label:<22} {produced}")
print()
print("     The default conversion is str(). The debug specifier '=' silently")
print("     switches it to repr(), which is the whole point of it: you asked")
print("     to see the value as a programmer, not as a reader.")

print("\n7. A CONTAINER ALWAYS USES repr() ON ITS ELEMENTS")
value = "a" + TAB + "b"
print(f"     print(value)     ->  {value}")
print(f"     print([value])   ->  {[value]}")
print()
print("     One tab, printed two ways in the same program. The first line")
print("     is str(): the tab is in the output and you can only see it by")
print("     the gap. The second is repr(), because a list has no way to")
print("     show you where one element ends -- so it escapes.")
print("     That is why wrapping a value in a list is the cheapest debugging")
print("     trick in Python, and why 'printable' had to be defined in terms")
print("     of repr() rather than in terms of ink.")
