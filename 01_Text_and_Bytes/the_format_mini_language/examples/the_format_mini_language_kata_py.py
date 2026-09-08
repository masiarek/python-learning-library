"""Answer key: nine slots, one per drill, then the spec read backwards.

Exceptions print as type(exc).__name__ -- CPython rewords the message after it
between releases and this output is compared byte for byte.
"""


def evaluate(source):
    try:
        return repr(eval(source, {}))
    except Exception as exc:  # noqa: BLE001 -- the kata is about which one
        return f"raises {type(exc).__name__}"


# One drill per slot of [[fill]align][sign][z][#][0][width][grouping][.precision][type]
DRILLS = [
    ("fill + align", "format(42, '*^12')", "the fill goes BEFORE the align"),
    ("sign", "format(42, '+d')", "'+' always, '-' only negatives, ' ' pads"),
    ("z", "format(-0.4, 'z.0f')", "PEP 682: coerce a negative zero, after rounding"),
    ("# alt + 0 pad", "format(255, '#010b')", "the 0b counts toward the ten"),
    ("0 before width", "format(42, '+08,d')", "NOT fill -- it means 'pad after the sign'"),
    ("width", "format(42, '8')", "a str would left-align in the same eight"),
    ("grouping", "format(1234567, '_d')", "',' and '_' are Python's own, and fixed"),
    (".precision on a float", "format(3.14159, '.3f')", "three places, rounded"),
    (".precision on a str", "format('truncated', '.3')", "a TRUNCATION, not a rounding"),
]

print("     the grammar:  [[fill]align][sign][z][#][0][width][grouping][.precision][type]")
print()
print(f"     {'slot':<22} {'call':<28} {'result':<15} note")
print("     " + "-" * 104)
for slot, source, note in DRILLS:
    print(f"     {slot:<22} {source:<28} {evaluate(source):<15} {note}")

print()
print("     THE TWO THAT ARE NOT WHAT THEY LOOK LIKE")
print("     '0' before the width is not 'fill with zeros' -- fill is the")
print("     separate FIRST slot. It is a flag meaning 'pad after the sign',")
print("     which is why the zeros land between the + and the 42:")
for source in ["format(42, '+08,d')", "format(42, '08,d')", "format(42, '0^8,d')"]:
    print(f"       {source:<24} {evaluate(source)}")
print("     The third one puts '0' in the FILL slot and '^' in the align")
print("     slot, so it is a different spec that happens to use the same")
print("     character.")
print()
print("     One consequence worth having met before it surprises you: with")
print("     grouping on, zero-padding rounds UP to a well-formed group,")
print("     because no group may begin with a separator. So three of these")
print("     nine widths come back one character longer than asked:")
for width in range(4, 13):
    got = format(42, f"0{width},d")
    flag = "  <- wider than the width" if len(got) > width else ""
    spec = f"'0{width},d'"
    print(f"       format(42, {spec:<9}) {got:<14} len {len(got):>2}{flag}")
print()
print("     And .precision on a str truncates. It does not round, it does")
print("     not warn, and it silently shortens data in a report:")
for source in ["format('truncated', '.3')", "format(3.14159, '.3')"]:
    print(f"       {source:<28} {evaluate(source)}")

print("\n     THE SPEC READ BACKWARDS")
print("     Given the output, write the spec. One answer each:")
WANTED = [
    (1234567, "1_234_567", "_d"),
    (255, "0b11111111", "#010b"),
    (3.14159, "***+3.142***", "*^+12.3f"),
    (42, "      42", "8"),
]
print(f"       {'value':<10} {'wanted':<15} {'spec':<12} {'got':<15} match")
print("       " + "-" * 62)
for value, wanted, spec in WANTED:
    got = format(value, spec)
    print(f"       {value!r:<10} {wanted + '|':<15} {spec!r:<12} {got + '|':<15} {got == wanted}")
print("       (the | marks the end of the field, so the padding is visible)")

print("\n     THE NUMBERING THAT RAISES")
NUMBERING = [
    ("'{} and {}'.format('spam', 'eggs')", "automatic: a counter"),
    ("'{1} and {0}'.format('spam', 'eggs')", "manual: reorder freely"),
    ("'{0} and {0}'.format('spam', 'eggs')", "manual: reuse freely"),
    ("'{} and {0}'.format('spam', 'eggs')", "mixed -- and this is the one"),
]
for source, note in NUMBERING:
    print(f"     {source:<40} {evaluate(source):<22} {note}")
print()
print("     Automatic numbering is a counter, so it can only count forwards.")
print("     The moment one field names its argument the counter has nothing")
print("     sensible to do, and Python refuses rather than guessing. Omitting")
print("     ALL the numbers is fine; omitting SOME of them is an error.")

print("\n     ROUNDING, AND THE MINUS SIGN THAT IS NOT A NEGATIVE NUMBER")
print(f"     {'value':>8}  {'.1f':>6} {'z.1f':>6} {'.0f':>6} {'z.0f':>6}")
print("     " + "-" * 42)
for value in [-0.0, -0.04, -0.4, 0.4, -1.5, 2.5, 3.5]:
    row = "  ".join(f"{format(value, spec):>6}" for spec in (".1f", "z.1f", ".0f", "z.0f"))
    print(f"     {value:>8}  {row}")
print()
print("     Rounding happens BEFORE the sign is chosen, so a number that is")
print("     merely small and negative prints as '-0'. In a column of results")
print("     that reads as a distinct value and it is not one -- and no")
print(f"     comparison will find it for you: -0.0 == 0.0 is {-0.0 == 0.0}.")
print("     The last two rows are a second surprise from the same column:")
print("     2.5 formats as 2 and 3.5 as 4. Formatting rounds half to even,")
print("     like round(), and not the way you were taught at school.")

print("\n     THE FOUR DOORS ARE ONE CALL")
SPEC, VALUE = "*^+12.3f", 3.14159
doors = [
    ("f-string", f"{VALUE:*^+12.3f}"),
    ("str.format", "{:*^+12.3f}".format(VALUE)),
    ("format() builtin", format(VALUE, SPEC)),
    ("__format__ direct", VALUE.__format__(SPEC)),
]
for name, result in doors:
    print(f"     {name:<20} {result!r}")
print(f"     all four identical: {len({r for _, r in doors}) == 1}")
print("     f-strings and str.format both compile down to format(), which")
print("     hands the text after the colon to the object's own __format__.")
print("     So the spec is not parsed by the language -- it is a string")
print("     handed to a type, and the type may mean anything by it. That is")
print("     why f'{now:%Y-%m-%d}' works without Python knowing what %Y is.")
