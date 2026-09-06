"""Why sorted() puts Polish surnames in the wrong order, and what a collation key is.

Nothing here depends on a locale being installed, on purpose: the one stdlib
answer (locale.strxfrm) needs a locale the machine may not have, so this program
REPORTS whether it is available rather than printing an order that would differ
between two computers.
"""

import locale
import unicodedata

NAMES = [
    "Zawadzki", "Ćwikła", "Adamczyk", "Żeromski", "Lewandowski",
    "Śliwa", "Nowak", "Łukasiewicz", "Cieślak", "Sikora",
]

# The Polish alphabet, in order. Every letter is its own letter -- Ł is not a
# decorated L, it sits between L and M.
POLISH = "aąbcćdeęfghijklłmnńoóprsśtuwyzźż"
RANK = {letter: i for i, letter in enumerate(POLISH)}


def polish_key(word):
    """A collation key: the word rewritten as the positions of its letters."""
    return [RANK.get(ch, len(POLISH)) for ch in word.lower()]


print("1. WHAT PYTHON DOES BY DEFAULT")
print("   sorted() compares code points, left to right.\n")
for name in sorted(NAMES):
    print(f"     {name}")

print("\n2. WHY -- the code point is the whole explanation")
for pair in [("L", "Ł"), ("Z", "Ż"), ("S", "Ś"), ("C", "Ć")]:
    base, accented = pair
    print(f"     ord({base!r}) = {ord(base):>5}   ord({accented!r}) = {ord(accented):>5}"
          f"   so {accented!r} > {base!r} is {accented > base}")
print(f"\n     Every Polish letter with a diacritic sits above U+00FF, and every")
print(f"     unaccented Latin letter sits below U+007B. So they ALL sort last.")

print("\n3. WHAT POLISH ACTUALLY WANTS")
print("   Ł belongs between L and M, not after Z.\n")
for name in sorted(NAMES, key=polish_key):
    print(f"     {name}")

print("\n4. THE SORT KEY IS THE IDEA")
print("   sorted(key=...) never compares the words -- it compares what the key")
print("   returns. Here is what the key makes of two of them:\n")
for name in ("Lewandowski", "Łukasiewicz"):
    head = polish_key(name)[:4]
    letters = " ".join(repr(c) for c in name[:4].lower())
    print(f"     {name:<14} {letters:<20} -> {head} ...")
print("\n     'l' is rank 14 and 'ł' is rank 15, so Lewandowski comes first --")
print("     decided by the second element, exactly as tuple comparison works.")

print("\n5. THE STDLIB ANSWER, AND WHY THIS PROGRAM CANNOT SHOW IT WORKING")
print("   locale.strxfrm() asks the C library for a collation key. The C library")
print("   knows the real rules -- but only for a locale that is INSTALLED, and")
print("   this program runs under LC_ALL=C so that its output is the same on")
print("   every machine. Under the C locale there are no rules to know:\n")
locale.setlocale(locale.LC_COLLATE, "C")
by_strxfrm = sorted(NAMES, key=locale.strxfrm)
print(f"     sorted(key=locale.strxfrm) == sorted()   {by_strxfrm == sorted(NAMES)}")
print(f"     first three: {by_strxfrm[:3]}")
print("\n     That True is the whole warning. Under the C locale strxfrm gives")
print("     back code-point order -- the wrong answer, silently, with the")
print("     correct API. A container, a cron job and a CI runner all default")
print("     to C or C.UTF-8, which is how 'it sorted fine on my laptop'")
print("     becomes a bug report from Warsaw. Check what you are running")
print("     under before trusting the call: locale -a | grep -i pl")

print("\n6. A THIRD ANSWER THAT IS ALMOST RIGHT")
print("   Stripping the diacritics sorts 'close enough' for a search box,")
print("   and is wrong for a phone book -- it cannot tell ź from ż.\n")
def strip_marks(word):
    decomposed = unicodedata.normalize("NFD", word.lower())
    return "".join(ch for ch in decomposed if not unicodedata.combining(ch))
for word in ("Łukasiewicz", "Żeromski", "Źróbek"):
    print(f"     {word:<14} -> {strip_marks(word)!r}")
print("\n     Note Ł survives: it is U+0141, a letter in its own right, with no")
print("     combining mark to strip. NFD does not decompose it.")
