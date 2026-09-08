"""Answer key: eight expressions over one word held as both types.

Every answer is printed, never typed. The exceptions print as
type(exc).__name__ on purpose -- CPython rewords the message after it between
releases, and this file's output is compared byte for byte.
"""

TEXT = "Łódź"
DATA = TEXT.encode("utf-8")


def evaluate(source):
    """(type name, repr) of `source`, or ('raises', the exception's type name)."""
    try:
        value = eval(source, {"TEXT": TEXT, "DATA": DATA})
    except Exception as exc:  # noqa: BLE001 -- the kata is about which one
        return "raises", type(exc).__name__
    return type(value).__name__, repr(value)


EXPRESSIONS = [
    ("len(TEXT)", "characters, and the word has four"),
    ("len(DATA)", "bytes, and UTF-8 spent two on each of Ł ó ź"),
    ("DATA[0]", "indexing bytes gives a NUMBER"),
    ("DATA[0:1]", "slicing bytes gives bytes -- the only way back to one byte"),
    ("TEXT == DATA", "the quiet one"),
    ("TEXT[0] + DATA[0:1]", "the loud one"),
    ("b'x'.startswith('x')", "even the method arguments are typed"),
    ("DATA.decode() == TEXT", "the round trip is exact"),
]

print("     TEXT = 'Łódź'          DATA = TEXT.encode('utf-8')")
print()
print(f"     {'expression':<24} {'type':<8} {'value':<10} note")
print("     " + "-" * 76)
for source, note in EXPRESSIONS:
    kind, value = evaluate(source)
    print(f"     {source:<24} {kind:<8} {value:<10} {note}")

print()
print("     Two of the eight raise. The other six hand back a value, and")
print("     one of those six is wrong -- which is the whole lesson.")

print()
print("     WHICH IS THE DANGEROUS ONE?")
print("     Not the TypeErrors. An exception is a bug that has already been")
print("     found. It is line 5: TEXT == DATA is False, always, for every")
print("     text and every bytes -- and False is a perfectly good answer that")
print("     a program will act on. A str is never equal to a bytes, however")
print("     identical the two look on screen.")
print()
print(f"     TEXT == DATA                 {TEXT == DATA}")
print(f"     TEXT == DATA.decode()        {TEXT == DATA.decode()}   <- what you meant")
print(f"     TEXT.encode() == DATA        {TEXT.encode() == DATA}   <- or this")
print()
print("     The fix is not a cast. It is deciding, at the boundary where the")
print("     value arrived, which of the two types this program holds it in.")
