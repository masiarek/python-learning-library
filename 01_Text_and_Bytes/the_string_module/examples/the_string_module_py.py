"""The `string` module is a leftovers drawer. Four things are in it, and one is a fossil."""

import re
import string
import unicodedata

# A fake secret, defined here so section 5 has something to steal out of
# this module. It is not a credential; it is the payload of the demo.
DATABASE_PASSWORD = "hunter2"


def escaped(s):
    """repr() without the quotes, and with the space made visible too."""
    return repr(s)[1:-1].replace(" ", "\\x20")


def wrapped(names, per_line, indent):
    """Join names into lines of `per_line`, indented, for a narrow column."""
    return f"\n{' ' * indent}".join(
        " ".join(names[i:i + per_line]) for i in range(0, len(names), per_line)
    )


print("1. THE WHOLE DRAWER")
public = [n for n in dir(string) if not n.startswith("_")]
constants = [n for n in public if not callable(getattr(string, n))]
callables = [n for n in public if n not in constants]
print(f"     The string module has {len(public)} public names, and that is all of it:")
print(f"       {len(constants)} constants  {wrapped(constants, 3, 20)}")
print(f"       {len(callables)} callables  {wrapped(callables, 3, 20)}")
print()
print("     Not one of them does something to a string that a str method")
print("     does not do better. That is the shape of a module which used")
print("     to hold the string functions, back when str had no methods to")
print("     hold them itself.")

print("\n2. THE CONSTANTS ARE AN ASCII TABLE, WRITTEN SIDEWAYS")
for name in ["ascii_lowercase", "ascii_uppercase", "ascii_letters",
             "digits", "hexdigits", "octdigits", "punctuation", "whitespace"]:
    value = getattr(string, name)
    print(f"     {name:<16} {len(value):>3}  {escaped(value)}")
parts = [string.digits, string.ascii_lowercase, string.ascii_uppercase,
         string.punctuation, string.whitespace]
print(f"     {'printable':<16} {len(string.printable):>3}  = digits + ascii_lowercase "
      f"+ ascii_uppercase")
print(f"     {'':<21} + punctuation + whitespace")
print(f"     {'':<21} -> that concatenation IS string.printable: "
      f"{''.join(parts) == string.printable}")
print()
print("     Sort those 100 characters by code point and the drawer turns")
print("     into the ASCII chart, with every boundary computed, not typed:")
print()
owners = [("whitespace", string.whitespace), ("digits", string.digits),
          ("ascii_uppercase", string.ascii_uppercase),
          ("ascii_lowercase", string.ascii_lowercase),
          ("punctuation", string.punctuation)]


def owner_of(ch):
    for label, members in owners:
        if ch in members:
            return label
    return "?"


runs = []
for cp in sorted(ord(c) for c in string.printable):
    label = owner_of(chr(cp))
    if runs and runs[-1][2] == label and runs[-1][1] == cp - 1:
        runs[-1][1] = cp
    else:
        runs.append([cp, cp, label])
print(f"     {'code points':<13} {'n':>3}  {'constant':<16} the characters")
print("     " + "-" * 66)
for lo, hi, label in runs:
    span = f"{lo:02X}-{hi:02X}" if lo != hi else f"{lo:02X}"
    chars = escaped("".join(chr(c) for c in range(lo, hi + 1)))
    print(f"     {span:<13} {hi - lo + 1:>3}  {label:<16} {chars}")
print()
print("     Four runs of punctuation, and they are exactly the gaps left")
print("     between the digit block and the two letter blocks. Those two")
print("     blocks start 0x20 apart, which is why ASCII case is one bit")
print("     and not a lookup:")
one_bit = all(chr(ord(u) | 0x20) == low
              for u, low in zip(string.ascii_uppercase, string.ascii_lowercase))
print(f"       ord('a') - ord('A') = {ord('a') - ord('A')} = 0x{ord('a') - ord('A'):02X}")
print(f"       chr(ord(c) | 0x20) lowercases all 26 of them: {one_bit}")

print("\n3. ASCII-ONLY BY DEFINITION -- WHICH IS THE ONLY REASON TO USE THEM")
print("     A constant is a membership test against a fixed list. The")
print("     methods that replaced them ask the Unicode table instead, and")
print("     the two answers part company on the first non-ASCII character:")
print()
print(f"     {'':<30} {'in the constant':<17} what Unicode says")
print("     " + "-" * 66)
rows = [
    ("'\\u0663' ARABIC-INDIC 3", 0x0663, "string.digits",
     lambda c: f"isdigit() {c.isdigit()}"),
    ("'\\xa0'   NO-BREAK SPACE", 0x00A0, "string.whitespace",
     lambda c: f"isspace() {c.isspace()}"),
    ("'\\u2019' RIGHT QUOTE", 0x2019, "string.punctuation",
     lambda c: f"category {unicodedata.category(c)}"),
    ("'\\u0141' L WITH STROKE", 0x0141, "string.ascii_letters",
     lambda c: f"isalpha() {c.isalpha()}"),
]
for label, cp, constant, verdict in rows:
    ch = chr(cp)
    print(f"     {label:<30} {str(ch in getattr(string, constant.split('.')[1])):<17} "
          f"{verdict(ch)}")
print()
space_points = sum(1 for cp in range(0x110000) if chr(cp).isspace())
print(f"     string.whitespace holds {len(string.whitespace)}; str.isspace() is True for "
      f"{space_points} code points.")
print("     So the two spellings of 'strip the whitespace' are not one:")
messy = "\xa0Zoot\x1c"
print(f"       {escaped(messy):<18}.strip()                  -> {messy.strip()!r}")
print(f"       {escaped(messy):<18}.strip(string.whitespace) -> "
      f"{messy.strip(string.whitespace)!r}")
print()
by_kind = {}
for ch in string.punctuation:
    by_kind.setdefault(unicodedata.category(ch)[0], []).append(ch)
print("     And 'punctuation' is a name from before the categories were:")
for initial in sorted(by_kind):
    kind = {"P": "punctuation", "S": "symbol"}[initial]
    print(f"       {initial}*  {len(by_kind[initial]):>2}  {kind:<12} "
          f"{escaped(''.join(by_kind[initial]))}")
print(f"     {len(by_kind['S'])} of the {len(string.punctuation)} are symbols, not punctuation, "
      f"by Unicode's own")
print("     accounting. The constant is not wrong about that -- it is")
print("     answering an older question: 'which ASCII characters are")
print("     neither letters nor digits nor space'.")

print("\n4. capwords() IS NOT title(), AND THE DIFFERENCE IS WHERE A WORD STARTS")
print("     The entire implementation, from Lib/string.py:")
print("       (sep or ' ').join(map(str.capitalize, s.split(sep)))")
print()
print(f"     {'input':<26} {'str.title()':<27} string.capwords()")
print("     " + "-" * 78)
for text in ["they're not the messiah", "x-ray results", "e.e. cummings",
             "3rd place", "o'brien", "  spaced   out  "]:
    print(f"     {text!r:<26} {text.title()!r:<27} {string.capwords(text)!r}")
print()
print("     title() starts a new word after every UNCASED character -- an")
print("     apostrophe, a hyphen, a digit, a dot -- which is why it")
print("     capitalises the 'r' of \"they're\". capwords() splits on")
print("     whitespace and nothing else, so it does not. Neither is a")
print("     title-caser: both lowercase the rest of every word, so 'IBM'")
print("     comes back 'Ibm' from either one.")
print()
print("     capwords() also rebuilds the string instead of editing it, so")
print("     with no separator it destroys the spacing it never read:")
for text, sep in [("  spaced   out  ", None), ("  spaced   out  ", " "),
                  ("a,b,,c", ",")]:
    result = string.capwords(text) if sep is None else string.capwords(text, sep)
    call = f"capwords({text!r}, {sep!r})"
    print(f"       {call:<36} -> {result!r}")
print("     With sep=None, split() collapses runs and drops the ends; with")
print("     an explicit separator it does neither. One call, two rules.")

print("\n5. Template IS THE SYNTAX THAT CANNOT REACH")


class User:
    def __init__(self, name, password):
        self.name = name
        self.password = password


brian = User("brian", "swordfish")
print("     A template that arrived from a user, a config file or a")
print("     database is a small program once you hand it to .format().")
print("     One object, four templates, one call each -- and this module")
print(f"     holds a global named DATABASE_PASSWORD, set to {DATABASE_PASSWORD!r}:")
print()
for tpl in ["{0.name}", "{0.password}", "{0.__class__.__name__}",
            "{0.__init__.__globals__[DATABASE_PASSWORD]}"]:
    print(f"       {tpl:<44} -> {tpl.format(brian)!r}")
print()
print("     A field name is a small expression language: a dot walks an")
print("     attribute, brackets index. Three hops from an object you")
print("     thought was harmless to a module global you never passed in.")
print()
print("     The same four names through Template, which has no dot:")
for tpl in ["$name", "$password", "$name.password", "$__class__"]:
    template = string.Template(tpl)
    try:
        got = repr(template.substitute(name="brian", password="swordfish"))
    except KeyError as exc:
        got = f"KeyError {exc.args[0]!r}"
    except ValueError as exc:
        got = type(exc).__name__
    print(f"       {tpl:<20} substitute -> {got}")
print()
print("     '$name.password' is 'brian' followed by nine literal")
print("     characters. The placeholder grammar ends at the identifier,")
print("     so there is nothing to reach with.")

print("\n6. substitute RAISES, safe_substitute NEVER DOES")
print(f"     {'template':<20} {'substitute()':<22} safe_substitute()")
print("     " + "-" * 66)
for tpl in ["$greeting $name", "cost: $100", "$$HOME", "${bad name}", "$"]:
    template = string.Template(tpl)
    try:
        strict = repr(template.substitute(greeting="Hi"))
    except KeyError as exc:
        strict = f"KeyError {exc.args[0]!r}"
    except ValueError as exc:
        strict = type(exc).__name__
    print(f"     {tpl!r:<20} {strict:<22} {template.safe_substitute(greeting='Hi')!r}")
print()
print("     'cost: $100' is the one that catches people. A price is an")
print("     invalid placeholder -- an identifier cannot begin with a digit")
print("     -- so substitute() raises on a template that was never trying")
print("     to have a placeholder in it. '$$' is the escape.")
print()
print("     Since 3.11 you can ask before you run, which is the honest way")
print("     to accept a template from somebody else:")
survey = string.Template("$greeting, $name! ${name}s cost $$5")
print(f"       t = Template({survey.template!r})")
print(f"       t.get_identifiers()  -> {survey.get_identifiers()}")
print(f"       t.is_valid()         -> {survey.is_valid()}")
print(f"       Template('$ oops').is_valid() -> {string.Template('$ oops').is_valid()}")

print("\n7. AND Template'S IDENTIFIERS ARE ASCII TOO, ON PURPOSE")
print(f"     Template.idpattern is {string.Template.idpattern!r}")
print()
for tpl, mapping in [("$café", {"caf": "X"}), ("$naïve", {"na": "Y"}),
                     ("$_x1", {"_x1": "Z"}), ("$Ω", {})]:
    template = string.Template(tpl)
    try:
        got = repr(template.substitute(mapping))
    except ValueError as exc:
        got = type(exc).__name__
    print(f"       {escaped(tpl):<12} identifiers {str(template.get_identifiers()):<10} "
          f"substitute -> {got}")
print()
print("     '$café' is the placeholder 'caf' followed by a literal 'é'.")
print("     It does not raise. It quietly substitutes a name that is a")
print("     prefix of the one you wrote.")
print()
print("     The (?a: in that pattern is doing real work. Matching [a-z]")
print("     case-insensitively without it lets three non-ASCII characters")
print("     in, because they case-fold onto ASCII letters:")
print()
plain = re.compile("[_a-z]", re.IGNORECASE)
ascii_only = re.compile("(?a:[_a-z])", re.IGNORECASE)
print(f"       {'':<7} {'':<28} {'[a-z]/i':<9} (?a:[a-z])/i")
for cp in [0x212A, 0x0131, 0x017F]:      # KELVIN SIGN, DOTLESS I, LONG S
    ch = chr(cp)
    print(f"       U+{cp:04X}  {unicodedata.name(ch):<28} "
          f"{bool(plain.match(ch))!s:<9} {bool(ascii_only.match(ch))}")

print("\n8. Formatter: THE HOOK, AND THE ONE METHOD WORTH KNOWING")
formatter = string.Formatter()
methods = [n for n in dir(formatter) if not n.startswith("_")]
print(f"     Formatter has {len(methods)} methods:")
print(f"       {wrapped(methods, 4, 7)}")
print(f"     Formatter().format('{{:*^9.3f}}', 3.14159) -> "
      f"{formatter.format('{:*^9.3f}', 3.14159)!r}")
print("     -- the same grammar, the same answer, in Python instead of C.")
print()
print("     parse() is the part that is not a reimplementation. It is the")
print("     public parser for the format grammar, and it will tell you")
print("     what a template wants without formatting anything:")
print()
survey_tpl = "{greeting}, {0:>8.2f} and {a[1]!r}!"
print(f"       Formatter().parse({survey_tpl!r})")
print(f"         {'literal':<12} {'field':<10} {'spec':<8} conv")
for literal, field, spec, conversion in formatter.parse(survey_tpl):
    print(f"         {literal!r:<12} {field!r:<10} {spec!r:<8} {conversion!r}")
print()
print("     And the reason to subclass it is section 5. Overriding one")
print("     method closes that hole, because get_field is exactly where")
print("     the dot and the brackets get interpreted:")
print()


class PlainNamesOnly(string.Formatter):
    def get_field(self, field_name, args, kwargs):
        if "." in field_name or "[" in field_name:
            raise ValueError("not a plain name")
        return super().get_field(field_name, args, kwargs)


safe = PlainNamesOnly()
for tpl in ["{who}", "{who!r:>10}", "{0.password}",
            "{0.__init__.__globals__[DATABASE_PASSWORD]}"]:
    try:
        got = repr(safe.format(tpl, brian, who="brian"))
    except ValueError as exc:
        got = f"ValueError: {exc.args[0]}"
    print(f"       {tpl:<44} -> {got}")
print()
print("     Five lines, and the whole attribute walk is gone. That you")
print("     have to write those five lines yourself is the argument for")
print("     reaching for Template instead.")
