"""Answer key: eight one-liners about a word that means two things."""

import string
import sys
from fractions import Fraction

EXPRESSIONS = [
    ("' '.isprintable()", "a space IS printable -- the one exception in the rule"),
    ("'\\t'.isprintable()", "a tab is not: repr() escapes it"),
    ("''.isprintable()", "vacuously true -- no character in it is non-printable"),
    ("'\\u00a0'.isprintable()", "NO-BREAK SPACE: whitespace, and not printable"),
    ("string.printable.isprintable()", "the constant is not printable, BY DESIGN"),
    ("len(str(b'Zoot!'))", "five bytes in, eight characters out"),
    ("len(str(b'Zoot!', 'utf-8'))", "the other signature, and the one you meant"),
    ("repr(Fraction(1, 3))", "what f'{x = }' shows you, and f'{x}' does not"),
]

print(f"     {'expression':<32} {'result':<17} note")
print("     " + "-" * 81)
for source, note in EXPRESSIONS:
    value = eval(source, {"string": string, "Fraction": Fraction})
    print(f"     {source:<32} {value!r:<17} {note}")

print()
print("     PRINTABLE HAS NOTHING TO DO WITH INK")
print("     str.isprintable() asks one question: would repr() escape this?")
print("     That is why a space passes and a tab does not, and why every")
print("     space character in Unicode EXCEPT U+0020 fails -- a")
print("     representation whose job is to be unambiguous cannot render")
print("     an invisible character as itself.")
print()
print("     string.printable is the OTHER word, the POSIX one: characters")
print("     a terminal can cope with, which includes the five that move a")
print("     cursor without drawing anything.")
five = [c for c in string.printable if not c.isprintable()]
print(f"     the five that separate them:  {' '.join(repr(c) for c in five)}")
print(f"     len(string.printable)         {len(string.printable)}")
print("     Two questions, one spelling, about twenty years apart.")

print("\n     THE QUIET ONE IS LINE 6")
b = b"Zoot!"
print(f"     b                  {b!r:<12} len {len(b)}")
print(f"     str(b)             {str(b)!r:<12} len {len(str(b))}   <- the repr, as text")
print(f"     str(b, 'utf-8')    {str(b, 'utf-8')!r:<12} len {len(str(b, 'utf-8'))}")
print(f"     b.decode()         {b.decode()!r:<12} len {len(b.decode())}")
print()
print("     Nothing raised. A five-byte object became an eight-character")
print("     string containing a 'b' and two quote marks, because str() with")
print("     no encoding falls back to repr(). It is a perfectly good str and")
print("     it will travel a long way before anything notices.")
print(f"     sys.flags.bytes_warning on this run: {sys.flags.bytes_warning}")
print("     Run any file with python3 -b and that becomes 1, and str(b)")
print("     raises a BytesWarning. -bb makes it an error. Python shipping a")
print("     command-line flag for one call is as close to an apology as a")
print("     language gets.")

print("\n     THE CHEAPEST DEBUGGING TRICK IN PYTHON")
value = "a\tb"
print(f"     print(value)     ->  {value}")
print(f"     print([value])   ->  {[value]}")
print()
print("     One tab, printed two ways in the same program, and nothing")
print("     about the string changed. A container has no way to show you")
print("     where one element ends, so it always uses repr() on what is")
print("     inside -- which is the practical reason 'printable' had to be")
print("     defined in terms of repr() in the first place.")
print()
one_third = Fraction(1, 3)
print(f"     f'{{x}}'      {one_third}")
print(f"     f'{{x!r}}'    {one_third!r}")
print(f"     f'{{x = }}'   {one_third = }")
print("     The debug specifier silently switches the conversion to repr().")
print("     Same expression, one equals sign, two different strings.")
