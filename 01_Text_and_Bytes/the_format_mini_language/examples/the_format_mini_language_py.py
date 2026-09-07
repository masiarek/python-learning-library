"""One grammar, four doors -- and a fifth spelling that is a different language."""

import locale

# Pinned rather than inherited: section 5 is about a locale, and a page whose
# output depends on which locales a machine happens to have is not a lesson.
locale.setlocale(locale.LC_NUMERIC, "C")


class Celsius:
    """A type with its own format spec -- which is what datetime does."""

    def __init__(self, deg):
        self.deg = deg

    def __str__(self):
        return f"{self.deg}C"

    def __repr__(self):
        return f"Celsius({self.deg})"

    def __format__(self, spec):
        if spec.endswith("F"):
            return format(self.deg * 9 / 5 + 32, spec[:-1] or ".1f") + "F"
        return format(str(self), spec)


print("1. FOUR DOORS, ONE GRAMMAR")
value = 3.14159
spec = "*^+12.3f"
print(f"     the spec:  {spec!r}")
print(f"     f-string             f'{{value:{spec}}}'          {value:*^+12.3f}")
print(f"     str.format           '{{:{spec}}}'.format(value)  {('{:' + spec + '}').format(value)}")
print(f"     format() builtin     format(value, {spec!r})    {format(value, spec)}")
print(f"     __format__ directly  value.__format__({spec!r})  {value.__format__(spec)}")
print()
print("     All four are the same call. f-strings and str.format both compile")
print("     down to format(), which calls the object's own __format__ with the")
print("     text after the colon -- so the spec is not parsed by the language.")
print("     It is a string handed to a type, and the type may mean anything by it:")
temp = Celsius(100)
for label, produced, note in [
    ("f'{temp}'", f"{temp}", "str(), no spec"),
    ("f'{temp:F}'", f"{temp:F}", "this type's OWN spec language"),
    ("f'{temp:>8}'", f"{temp:>8}", "falls back to the standard one"),
    ("f'{temp!r}'", f"{temp!r}", "conversion happens BEFORE __format__"),
]:
    print(f"       {label:<14} {produced:<14} <- {note}")

print("\n2. THE NINE SLOTS")
print("     [[fill]align][sign][z][#][0][width][grouping][.precision][type]")
print()
rows = [
    ("fill + align", "'*^12'", format(42, "*^12")),
    ("align only", "'<8'", format(42, "<8") + "|"),
    ("sign: always", "'+d'", format(42, "+d")),
    ("sign: space", "' d'", format(42, " d") + "|"),
    ("alt form + zero pad", "'#010b'", format(255, "#010b")),
    ("width", "'8'", format(42, "8") + "|"),
    ("grouping: comma", "',d'", format(1234567, ",d")),
    ("grouping: underscore", "'_d'", format(1234567, "_d")),
    ("grouping in binary", "'_b'", format(255, "_b")),
    ("precision on a float", "'.3f'", format(3.14159, ".3f")),
    ("precision on a str", "'.3'", format("truncated", ".3")),
    ("type: hex, exp, pct", "'x' 'e' '%'", f"{255:x} {1234.0:e} {0.25:%}"),
    ("all of it", "'+08,d'", format(42, "+08,d")),
]
print(f"     {'slot':<22} {'spec':<14} result")
print("     " + "-" * 54)
for label, sp, out in rows:
    print(f"     {label:<22} {sp:<14} {out}")
print()
print("     Two that surprise people: '0' before the width is not padding with")
print("     the fill character, it is a separate flag that means 'pad after the")
print("     sign' -- which is why '+08,d' puts the zeros between + and 42. And")
print("     .precision on a str is a TRUNCATION, not a rounding.")

print("\n3. NUMBERING: AUTOMATIC, MANUAL, AND THE MIX THAT RAISES")
a, b = "spam", "eggs"
print(f"     automatic   '{{}} and {{}}'        -> {'{} and {}'.format(a, b)}")
print(f"     manual      '{{0}} and {{1}}'      -> {'{0} and {1}'.format(a, b)}")
print(f"     reordered   '{{1}} and {{0}}'      -> {'{1} and {0}'.format(a, b)}")
print(f"     reused      '{{0}} and {{0}}'      -> {'{0} and {0}'.format(a, b)}")
print(f"     by name     '{{x}} and {{y}}'      -> {'{x} and {y}'.format(x=a, y=b)}")
print(f"     attribute   '{{0.deg}}'          -> {'{0.deg}'.format(Celsius(100))}")
print(f"     item        '{{0[1]}}'           -> {'{0[1]}'.format([a, b])}")
try:
    "{} and {0}".format(a, b)
    mixed = "no error"
except ValueError as exc:
    mixed = type(exc).__name__
print(f"     mixed       '{{}} and {{0}}'       -> {mixed}")
print()
print("     Automatic numbering is a counter, so it can only count forwards.")
print("     The moment one field names its argument, the counter has nothing")
print("     sensible to do, and Python refuses rather than guessing. That is")
print("     the fact the 'you may omit the numbers' changelog note leaves out.")
print("     Note also the item lookup: '{0[1]}' takes no quotes, so the key is")
print("     always a string unless it is all digits -- there is no way to write")
print("     a lookup by the integer 1 versus the string '1'.")

print("\n4. THE MINUS SIGN THAT IS NOT A NEGATIVE NUMBER")
print(f"     {'value':<12} {'.1f':>8} {'z.1f':>8} {'.0f':>8} {'z.0f':>8}")
print("     " + "-" * 48)
for v in (-0.0, -0.04, -0.4, 0.4, -1.5, 2.5, 3.5):
    print(f"     {v!r:<12} {format(v, '.1f'):>8} {format(v, 'z.1f'):>8}"
          f" {format(v, '.0f'):>8} {format(v, 'z.0f'):>8}")
print()
print("     Rounding happens before the sign is chosen, so a number that is")
print("     merely small and negative can print as '-0'. In a table of results")
print("     that reads as a distinct value, and it is not one. The 'z' option")
print("     (PEP 682, Python 3.11) coerces a negative zero to a positive one")
print("     AFTER rounding, which is the only place it can be fixed.")
print(f"     -0.0 == 0.0 is {-0.0 == 0.0}, so no comparison will find this for you.")
print("     The last two rows are a second surprise from the same column:")
print("     2.5 formats as 2 and 3.5 as 4. Formatting rounds half to even,")
print("     like round(), and not the way you were taught at school.")

print("\n5. GROUPING, AND THE ONE THAT ASKS THE OPERATING SYSTEM")
conv = locale.localeconv()
print(f"     under the C locale: thousands_sep={conv['thousands_sep']!r} "
      f"decimal_point={conv['decimal_point']!r} grouping={conv['grouping']}")
for sp in (",d", "_d", "n"):
    print(f"     format(1234567, {sp!r:<5}) -> {format(1234567, sp)}")
print()
print("     ',' and '_' are Python's own separators and mean the same thing on")
print("     every machine. 'n' means 'ask the locale', and under C the locale")
print("     has nothing to say -- which is why this line is boring on purpose.")
print("     Set LC_NUMERIC to a locale that groups, and the same call prints")
print("     1.234.567 or 1 234 567 instead.")
print("     The documented cost is unusual enough to be worth knowing: when")
print("     the separators are non-ASCII or longer than one byte, formatting")
print("     with 'n' TEMPORARILY CHANGES LC_CTYPE for the whole process --")
print("     and the docs say outright that this affects other threads.")
print("     A formatting call that mutates global state. Use ',' unless you")
print("     are deliberately rendering for a human in a known locale.")

print("\n6. format_map: THE MAPPING IS NOT COPIED")


class Default(dict):
    def __missing__(self, key):
        return "<" + key + ">"


template = "{name} was born in {country}"
data = Default(name="Guido")
print(f"     template          {template!r}")
print(f"     format_map(...)   {template.format_map(data)}")
try:
    out = template.format(**data)
except KeyError as exc:
    out = f"{type(exc).__name__}: {exc}"
print(f"     format(**data)    {out}")
print()
print("     format(**m) unpacks m into a fresh plain dict, so the subclass --")
print("     and its __missing__ -- is gone before formatting starts. format_map")
print("     passes the object itself, so the hook survives. That is the whole")
print("     difference, and it is why the useful version has its own method.")

print("\n7. % IS A DIFFERENT LANGUAGE, AND IT IS THE ONLY ONE THAT DOES bytes")
print(f"     '%s and %s' % (a, b)        {'%s and %s' % (a, b)}")
print(f"     '%(x)s' % dict(x=a)         {'%(x)s' % dict(x=a)}")
print(f"     '%.3f' % 3.14159            {'%.3f' % 3.14159}")
print(f"     '%r' % a                    {'%r' % a}")
for label, template_pct, args in [
    ("'%s' % (1, 2)", "%s", (1, 2)),
    ("'%s %s' % ('a',)", "%s %s", ("a",)),
    ("'%s' % (1,)", "%s", (1,)),
]:
    try:
        produced = template_pct % args
    except TypeError as exc:
        produced = type(exc).__name__
    print(f"     {label:<27} {produced}")
print()
print("     % is one operator with one right-hand operand. A tuple on the right")
print("     is not 'the arguments' -- it is the operand, and it gets unpacked,")
print("     which is why both arity mistakes above are TypeErrors rather than")
print("     the two different errors you would get from a function call.")
print()
raw = b"%s|%d" % (b"ab", 7)
print(f"     b'%s|%d' % (b'ab', 7)       {raw!r}   <- bytes, not str")
print("     str.format and f-strings do not exist on bytes. PEP 461 put % back")
print("     on bytes in 3.5 for exactly this: binary protocols with ASCII")
print("     headers, where the alternative was building the bytes by hand.")
print("     That is the reason the oldest of the four is not going anywhere.")
