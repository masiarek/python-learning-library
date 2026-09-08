"""The translation table is a dict of ordinals, and that explains everything else."""

from collections import defaultdict

print("1. THE TABLE IS A DICT OF INTEGERS")
two = str.maketrans("abc", "xyz")
print(f"     str.maketrans('abc', 'xyz')      {two}")
print(f"     type                             {type(two).__name__}")
print()
print("     97 is ord('a') and 120 is ord('x'). Both sides are ordinals:")
print("     the two-argument form never stores a character at all.")
print()
print("     Written out by hand, the same table is:")
print("       {ord('a'): ord('x'), ord('b'): ord('y'), ord('c'): ord('z')}")
print("     That is the whole reason maketrans exists.")
print()
print("     Three ways to build one, and what each returns:")
three = str.maketrans("abc", "xyz", "Q!")
mapping = str.maketrans({"a": "HELLO", "b": None, 99: "z"})
print(f"       maketrans('abc', 'xyz')         {two}")
print(f"       maketrans('abc', 'xyz', 'Q!')   {three}")
print(f"       maketrans({{'a': 'HELLO', ...}})   {mapping}")
print()
print("     The third argument is not a third feature: it adds the same")
print("     keys with None as the value. And the one-argument form is the")
print("     only one that keeps values as strings -- it is barely a")
print("     conversion, it just turns any str keys into their ordinals.")

print("\n2. A VALUE MAY BE A STRING OF ANY LENGTH, OR None")
src = "a-b-c"
rows = [
    ("one char  ", {ord("a"): "A"}),
    ("many chars", {ord("a"): "ALPHA"}),
    ("empty str ", {ord("a"): ""}),
    ("None      ", {ord("a"): None}),
    ("an ordinal", {ord("a"): 0x41}),
]
print(f"     {'value':<12} {'table':<28} {src!r} becomes")
print("     " + "-" * 62)
for label, table in rows:
    print(f"     {label:<12} {str(table):<28} {src.translate(table)!r}")
print()
both = {ord("a"): "ALPHA", ord("-"): None}
print(f"     Expand and delete in the same call: {both}")
print(f"       {src!r}.translate(...)  ->  {src.translate(both)!r}")
print()
print("     No other str method does both in one call. replace() can")
print("     grow a string, and replace('x', '') can shrink one, but a")
print("     call handles exactly one pattern. Here 'a' grew to five")
print("     characters and '-' vanished, in one walk over the input.")

print("\n3. ONE PASS, WHICH IS WHAT CHAINED replace() IS NOT")
print("     Swap two characters. It cannot be done with replace at all:")
pair = "ab"
print(f"       {pair!r}.replace('a', 'b').replace('b', 'a')   "
      f"{pair.replace('a', 'b').replace('b', 'a')!r}")
print(f"       {pair!r}.translate(maketrans('ab', 'ba'))      "
      f"{pair.translate(str.maketrans('ab', 'ba'))!r}")
print()
print("     The first call's output is the second call's input, so every")
print("     'a' becomes 'b' and then every 'b' -- including the new ones --")
print("     becomes 'a'. Shift three letters by one and all three collapse:")
shift = "abc"
chained = shift.replace("a", "b").replace("b", "c").replace("c", "d")
bcd = shift.translate(str.maketrans("abc", "bcd"))
print(f"       {repr(shift) + ' through three replaces':<40} {chained!r}")
print(f"       {repr(shift) + '.translate(maketrans(abc, bcd))':<40} {bcd!r}")
print()
print("     The real-world shape of this is HTML escaping:")
raw = "<a>&"
wrong = raw.replace("<", "&lt;").replace("&", "&amp;")
right = raw.replace("&", "&amp;").replace("<", "&lt;")
escape_table = {ord("&"): "&amp;", ord("<"): "&lt;", ord(">"): "&gt;"}
print(f"       raw                              {raw!r}")
print(f"       .replace('<',..).replace('&',..) {wrong!r}   <- doubly escaped")
print(f"       .replace('&',..).replace('<',..) {right!r}")
print(f"       .translate(table)                {raw.translate(escape_table)!r}")
print()
print("     Two replaces, two answers, and only one order is right. The")
print("     stdlib's own html.escape does it with chained replaces and")
print("     carries a comment on the first line saying it must go first.")
print("     With a table there is no first line: no character is ever")
print("     looked at twice, so there is no order to get wrong.")

print("\n4. THE TABLE ONLY HAS TO ANSWER __getitem__")
print("     translate() indexes the table with an int and catches")
print("     LookupError. Nothing else is required -- not dict, not even")
print("     a mapping.")
print()


class Redact(dict):
    """Anything not listed becomes '#'."""

    def __missing__(self, ordinal):
        return "#"


class KeepOnly(dict):
    """Anything not listed is deleted."""

    def __missing__(self, ordinal):
        return None


class OnlyGetItem:
    """Not a dict, not a Mapping. One method."""

    def __getitem__(self, ordinal):
        if ordinal == ord("a"):
            return "AAA"
        raise LookupError(ordinal)


keep = KeepOnly({ord(c): c for c in "0123456789-"})
card = "4111-1111 1111 1111 (Visa)"
digits_only = defaultdict(lambda: "", {ord(c): c for c in "0123456789"})
list_table = [chr(i) for i in range(128)]
list_table[ord("a")] = "AAA"

samples = [
    ("dict subclass, __missing__ -> '#'", "ab1 2c", Redact({ord(" "): " "})),
    ("dict subclass, __missing__ -> None", card, keep),
    ("defaultdict(lambda: '')", card, digits_only),
    ("a class with only __getitem__", "abc", OnlyGetItem()),
    ("a 128-element list", "abc", list_table),
]
for label, text, table in samples:
    print(f"     {label:<36} {text!r}")
    print(f"     {'':<36} -> {text.translate(table)!r}")
print()
print("     The second and third do the same job two ways: keep a listed")
print("     alphabet, drop everything else, in one pass and with no regex.")
print("     That is the shape __missing__ is for -- 'map everything I did")
print("     not list to X' is one method, not a loop over the code space.")
print()
print("     A LookupError from the table means 'leave this character")
print("     alone'. KeyError and IndexError are both LookupError, so both")
print("     mean identity; anything else propagates:")


class Raises:
    def __init__(self, exc):
        self.exc = exc

    def __getitem__(self, ordinal):
        raise self.exc(ordinal)


for exc in (KeyError, IndexError, LookupError, ValueError):
    try:
        got = repr("abc".translate(Raises(exc)))
    except Exception as caught:  # noqa: BLE001 - the point is which type escapes
        got = f"raised {type(caught).__name__}"
    subclass = "LookupError" if issubclass(exc, LookupError) else "-"
    print(f"       __getitem__ raises {exc.__name__:<12} {subclass:<12} {got}")
print()
print("     And that is why a str is a legal table and a silent no-op:")
print(f"       'abc'.translate('xyz')     {'abc'.translate('xyz')!r}")
print("     'xyz'[97] raises IndexError, which means 'leave it alone',")
print("     three times. No error, no change, no warning.")
print(f"       'abc'.translate('x' * 200) {'abc'.translate('x' * 200)!r}")
print("     Same call, longer string, and now the indexes land.")

print("\n5. WHAT THE TABLE MAY NOT RETURN")
print("     A value is an int, a str, or None. Two failures, by type:")


class Returns:
    def __init__(self, value):
        self.value = value

    def __getitem__(self, ordinal):
        return self.value


bad = [("a float", 3.5), ("a list", ["x"]), ("0x110000", 0x110000), ("-1", -1)]
for label, value in bad:
    try:
        "a".translate(Returns(value))
        outcome = "no error"
    except Exception as caught:  # noqa: BLE001 - the type is the answer
        outcome = type(caught).__name__
    print(f"       value {label:<10} {outcome}")
print()
print("     An int value is a code point, so it must be one: the ceiling")
print("     is 0x110000 and there is no negative half of the code space.")
print("     maketrans has two of its own, both ValueError -- unequal")
print("     lengths in the two-argument form, and a str key that is not")
print("     exactly one character in the one-argument form.")
for label, call in [
    ("maketrans('ab', 'xyz')", lambda: str.maketrans("ab", "xyz")),
    ("maketrans({'ab': 'x'})", lambda: str.maketrans({"ab": "x"})),
]:
    try:
        call()
        outcome = "no error"
    except Exception as caught:  # noqa: BLE001 - the type is the answer
        outcome = type(caught).__name__
    print(f"       {label:<24} {outcome}")

print("\n6. ABOVE THE BMP: ONE KEY PER CODE POINT")
CLEF = "\U0001d11e"
text = f"x{CLEF}y"
halves = {0xD834: "HI", 0xDD1E: "LO"}
bmp_rows = [
    ("text", f"{text!r}   len {len(text)}"),
    ("U+1D11E as an ordinal", f"{ord(CLEF)}  (0x{ord(CLEF):X})"),
    ("translate({0x1D11E: 'CLEF'})", repr(text.translate({0x1D11E: "CLEF"}))),
    ("translate({0x1D11E: None})", repr(text.translate({0x1D11E: None}))),
    ("maketrans(CLEF, 'x')", str(str.maketrans(CLEF, "x"))),
]
for label, value in bmp_rows:
    print(f"     {label:<30} {value}")
print()
print(f"     {'keyed by the UTF-16 halves':<30} {halves}")
print(f"       -> {text.translate(halves)!r}   <- nothing happened")
print()
print("     A Python str is a sequence of code points, not of UTF-16 code")
print("     units, so an astral character is one key and one length-1")
print("     lookup. The surrogate ordinals 0xD834 and 0xDD1E are simply")
print("     not present in the string. In a language whose char is 16")
print("     bits this same substitution is two lookups and a pair to keep")
print("     together.")

print("\n7. bytes.translate IS A DIFFERENT METHOD")
bt = bytes.maketrans(b"abc", b"xyz")
print(f"     bytes.maketrans(b'abc', b'xyz')  {type(bt).__name__}, len {len(bt)}")
print(f"     bytes 95..100 of it              {bt[95:101]!r}")
print()
print("     Not a dict of the three keys you asked for: a 256-byte")
print("     lookup table, every byte value pre-filled with itself and")
print("     three of them overwritten. Byte 97 now holds 120.")
print()
print(f"     b'abcd'.translate(bt)            {b'abcd'.translate(bt)!r}")
print(f"     b'abcd'.translate(bt, b'd')      {b'abcd'.translate(bt, b'd')!r}")
print(f"     b'abcd'.translate(None, b'bd')   {b'abcd'.translate(None, b'bd')!r}")
print()
print("     Deletion is a second positional argument, not a None value,")
print("     because a byte table has no room for one. And the table can")
print("     be None on its own, which makes the call pure deletion --")
print("     a spelling str.translate does not have.")
print()
print("     The two signatures side by side:")
print("       str  .translate(table)                 table[ordinal] -> int|str|None")
print("       bytes.translate(table, delete=b'')     a 256-byte sequence, or None")
print()
for label, call in [
    ("b'a'.translate(bytes(255))", lambda: b"a".translate(bytes(255))),
    ("b'a'.translate({97: b'X'})", lambda: b"a".translate({97: b"X"})),
    ("'a'.translate(bytes(256))", lambda: "a".translate(bytes(256))),
]:
    try:
        outcome = repr(call())
    except Exception as caught:  # noqa: BLE001 - the type is the answer
        outcome = type(caught).__name__
    print(f"       {label:<28} {outcome}")
print()
print("     A dict is not a bytes-like object, and 255 is not 256. The")
print("     last row is the one that surprises: bytes(256) is a valid")
print("     table for bytes and a legal, useless one for str -- 256 zero")
print("     bytes indexed at 97 gives 0, so every ASCII character maps to")
print("     the null character instead of raising.")
