"""Answer key: eight literals, and where each escape stopped.

Escape processing happens at COMPILE time, so a literal that would warn cannot
be written in this file -- the warning would fire when the file is read, before
any of the kata ran, and it would fire on 3.12+ and not on 3.11. So the sources
are built at run time out of chr(92) and handed to eval(), exactly as the
lesson's own program does. That is also the only way to show an invalid escape
without this file containing one.

The table prints the source it evaluated rather than a hand-written copy of it,
so the 'written' column cannot drift from the value beside it.
"""

import re
import warnings

BS = chr(92)
warnings.simplefilter("ignore")


def literal(source):
    return eval(source, {})


CASES = [
    ("'" + BS + "xA1A'", BS + "x is exactly two digits, always"),
    ("'" + BS + "1010'", "octal is greedy: it took three"),
    ("'" + BS + "d'", "unknown escape -- the backslash is KEPT"),
    ("'" + BS + "b'", "known escape -- BACKSPACE, U+0008"),
    ("r'" + BS + "u0041'", "raw: not an escape at all"),
    ("b'" + BS + "u0041'", "bytes: a byte has no code point"),
    ("'spam' 'eggs'", "adjacent literals join at compile time"),
    ("'" + BS + "0'", "octal zero, not a special NUL escape"),
]

print(f"     {'written':<16} {'len':>3}  {'value':<18} why")
print("     " + "-" * 78)
for source, note in CASES:
    value = literal(source)
    print(f"     {source:<16} {len(value):>3}  {value!r:<18} {note}")

print()
print("     Two escapes, two widths, one grammar. Python has exactly one")
print("     fixed-width numeric escape and one greedy one, and the greedy")
print("     one is the one nobody writes on purpose. If you write octal at")
print("     all, write all three digits.")

print("\n     WHICH ONE BREAKS A REGULAR EXPRESSION?")
cooked = literal("'" + BS + "bfoo" + BS + "b'")
raw = literal("r'" + BS + "bfoo" + BS + "b'")
subject = "a foo b"
print(f"     pattern written  '{BS}bfoo{BS}b'   subject {subject!r}")
print(f"       cooked -> {cooked!r:<14} re.search -> {re.search(cooked, subject)}")
print(f"       raw    -> {raw!r:<14} re.search -> {re.search(raw, subject).span()}")
print()
print(f"     '{BS}d', '{BS}w', '{BS}s', '{BS}A' and '{BS}Z' all reach re intact --")
print("     purely because Python did not recognise them and left the")
print(f"     backslash alone. '{BS}b' is the exception, and it is the one")
print("     every real pattern uses: Python claims it for BACKSPACE, so the")
print("     cooked pattern asked for a backspace character on both sides of")
print("     'foo'. It found nothing and it raised nothing. That is the")
print("     actual reason regex patterns are written r'' -- not style, and")
print("     not about the backslashes you can see.")

print("\n     THE ONE THAT IS NOT A LITERAL AT ALL")
print("     Line 7. 'spam' 'eggs' is one string, joined by the COMPILER,")
print("     with no '+' and no run-time cost. The price is what a missing")
print("     comma does to a list:")
menu = ["spam", "eggs" "beans", "toast"]
print(f"     ['spam', 'eggs' 'beans', 'toast']  ->  {menu}")
print(f"     len is {len(menu)}, and nobody typed a concatenation. Not a syntax")
print("     error -- a shorter list. Linters look for it because the")
print("     language cannot.")

print("\n     FIVE SPELLINGS OF ONE CODE POINT")
SPELLINGS = [
    "'é'",
    "'" + BS + "xe9'",
    "'" + BS + "u00e9'",
    "'" + BS + "U000000e9'",
    "'" + BS + "N{LATIN SMALL LETTER E WITH ACUTE}'",
]
values = [literal(source) for source in SPELLINGS]
for source in SPELLINGS:
    print(f"     {source}")
print(f"     all five are the same one-character string: {len(set(values)) == 1}")
print("     U+00E9 is a sixth notation and it is NOT Python syntax -- it is")
print("     the Unicode standard NAMING the code point. Same number, three")
print("     jobs, and only two of the three are code.")
