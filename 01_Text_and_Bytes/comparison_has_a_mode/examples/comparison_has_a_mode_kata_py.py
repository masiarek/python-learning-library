"""Kata answers: eight questions, and no two of the three answers agree.

Every line below is the answer to a prediction on the lesson page. The point of
the set is that rows 1-3 and rows 4-5 are the SAME pair asked three ways and two
ways, and the answers do not agree -- which is the page's claim, made checkable.

Why lower() and casefold() differ at all is a separate lesson and not repeated
here; this kata is about which of the three you called.
"""

import locale
import re

NUL = chr(0)
SHARP = "straße"
CHEROKEE = "ꭰ"
DOTLESS = "ı"


def matches(pattern, text):
    """re.IGNORECASE, asked as a yes/no over the whole string."""
    return re.fullmatch(re.escape(pattern), text, re.IGNORECASE) is not None


rows = [
    ("1", "'straße'.lower() == 'STRASSE'.lower()",
     SHARP.lower() == "STRASSE".lower(),
     "lower() has no 1-to-2 mapping: 'ß' stays 'ß'"),
    ("2", "'straße'.casefold() == 'STRASSE'.casefold()",
     SHARP.casefold() == "STRASSE".casefold(),
     "casefold() folds 'ß' to 'ss', so both sides become 'strasse'"),
    ("3", "re.fullmatch('straße', 'STRASSE', re.I)",
     matches(SHARP, "STRASSE"),
     "re.IGNORECASE has no 1-to-2 mapping either -- it agrees with lower()"),
    ("4", "'ı'.casefold() == 'I'.casefold()",
     DOTLESS.casefold() == "I".casefold(),
     "dotless i is a different letter; folding keeps them apart"),
    ("5", "re.fullmatch('ı', 'I', re.I)",
     matches(DOTLESS, "I"),
     "...and here re.IGNORECASE disagrees with casefold() instead"),
    ("6", "'ꭰ'.casefold().isupper()",
     CHEROKEE.casefold().isupper(),
     "Cherokee folds UPWARD -- the fold of a small letter is a capital"),
    ("7", "'admin' == 'admin' + chr(0)",
     "admin" == "admin" + NUL,
     "ordinal: a NUL is a character, so the strings differ"),
]

print("PREDICTIONS")
print(f"     {'#':<3}{'expression':<44}{'answer':>8}   why")
print("     " + "-" * 96)
for num, expr, value, why in rows:
    print(f"     {num:<3}{expr:<44}{value!s:>8}   {why}")

print("\n8    locale.strxfrm('admin' + chr(0))")
locale.setlocale(locale.LC_COLLATE, "C")
try:
    outcome = repr(locale.strxfrm("admin" + NUL))
except ValueError as exc:
    outcome = type(exc).__name__
print(f"     -> {outcome}")
print("     Not equal, and not unequal either. The linguistic API refuses a")
print("     string it cannot represent rather than quietly dropping the NUL.")

print("\nTHE FOLLOW-UP: WHY 3 AND 5 GO OPPOSITE WAYS")
print("   Three case-insensitive answers, and no two of them agree on both pairs:\n")
print(f"     {'pair':<22}{'lower':>8}{'casefold':>10}{'re.I':>7}")
for label, a, b in [("straße / STRASSE", SHARP, "STRASSE"), ("ı / I", DOTLESS, "I")]:
    print(f"     {label:<22}{a.lower() == b.lower()!s:>8}"
          f"{a.casefold() == b.casefold()!s:>10}{matches(a, b)!s:>7}")
print("\n     casefold() implements Unicode case folding, which is defined for")
print("     caseless MATCHING: it expands 'ß' and it deliberately leaves the")
print("     Turkish letters apart. re.IGNORECASE is built from a table of")
print("     single-character equivalences, so it can pair 'ı' with 'I' -- one")
print("     code point for one -- and cannot pair 'ß' with 'ss' at all.")
print("     Neither is a bug. They answer different questions, and the only")
print("     mistake available is not knowing which one you called.")
