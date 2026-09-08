"""Kata: nine expressions from the leftovers drawer, and the two that answer a name nobody wrote."""

import string


def outcome(fn):
    """The value, or the exception TYPE -- never the message, which is not API."""
    try:
        return repr(fn())
    except Exception as exc:
        return type(exc).__name__


CASES = [
    ("string.capwords('x-ray results')",
     lambda: string.capwords("x-ray results"),
     "splits on whitespace, so 'ray' is not a word"),
    ("'x-ray results'.title()",
     lambda: "x-ray results".title(),
     "a hyphen is uncased, so it starts a word"),
    ("string.capwords('  spaced   out  ')",
     lambda: string.capwords("  spaced   out  "),
     "rebuilt by split()+join(): the spacing is gone"),
    ("'\\u0663' in string.digits",
     lambda: "٣" in string.digits,
     "the constant is ASCII; '٣'.isdigit() is True"),
    ("'\\xa0Zoot'.strip(string.whitespace)",
     lambda: "\xa0Zoot".strip(string.whitespace),
     "6 characters in the constant, 29 in str.isspace()"),
    ("len(string.printable)",
     lambda: len(string.printable),
     "ASCII 0x20-0x7E is 95, plus five controls"),
    ("string.Template('cost: $100').substitute()",
     lambda: string.Template("cost: $100").substitute(),
     "an identifier cannot begin with a digit"),
    ("string.Template('$café').substitute(caf='X')",
     lambda: string.Template("$café").substitute(caf="X"),
     "the placeholder is 'caf'; the 'e-acute' is literal"),
    ("'{0.__class__.__name__}'.format(3)",
     lambda: "{0.__class__.__name__}".format(3),
     "a field name walks attributes -- that is the point"),
]

header = f"     {'expression':<45} {'answer':<16} why"
print(header)
print("     " + "-" * 95)
for source, fn, why in CASES:
    print(f"     {source:<45} {outcome(fn):<16} {why}")

print()
print("     THE TWO THAT ANSWER A NAME NOBODY WROTE")
print("     Lines 7 and 8 are the same grammar seen from both sides.")
template = string.Template("$café")
# Hoisted: a nested same-type quote inside an f-string expression is a
# SyntaxError before 3.12 (PEP 701), and the floor here is 3.11.
ids_call = "Template('$café').get_identifiers()"
valid_call = "Template('cost: $100').is_valid()"
print(f"       {ids_call:<36} -> {template.get_identifiers()}")
print(f"       {valid_call:<36} -> {string.Template('cost: $100').is_valid()}")
print("     One asked for 'café' and got 'caf'; the other never meant")
print("     to have a placeholder and has a malformed one. Neither is")
print("     visible in the template as you read it, and both are")
print("     answerable before you run anything -- which is what those")
print("     two 3.11 methods are for.")

print()
print("     WHY LINE 9 IS THE WHOLE ARGUMENT FOR Template")
print("     A dot in a field name walks an attribute, so a template")
print("     that came from outside your program reads whatever the")
print("     object can reach:")
for tpl in ["{0.__class__.__name__}", "{0.numerator}", "{0.real}"]:
    call = f"{tpl}.format(3)"
    print(f"       {call:<38} -> {tpl.format(3)!r}")
print("     Template has no dot. '$name.password' substitutes 'name'")
print("     and leaves nine literal characters, which is the entire")
print("     security argument for a syntax that can do nothing else.")

print()
print("     THE CONSTANT-VERSUS-METHOD PAIR")
print("     Lines 4 and 5 are one question asked twice:")
checks = [("٣", "digits", "isdigit"), ("\xa0", "whitespace", "isspace")]
for ch, const, method in checks:
    in_const = ch in getattr(string, const)
    print(f"       U+{ord(ch):04X}  in string.{const:<11} {in_const!s:<6} "
          f"str.{method}()  {getattr(ch, method)()}")
print("     Both constants say no and both methods say yes. Neither is")
print("     wrong: a constant is a fixed ASCII list and a method is a")
print("     lookup in the Unicode table. For a validator, pick the one")
print("     whose promise you can state out loud.")
