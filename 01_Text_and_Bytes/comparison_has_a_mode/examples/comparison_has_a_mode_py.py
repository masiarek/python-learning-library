"""Python has four string-comparison modes and a name for none of them.

.NET makes you pass a StringComparison to every string API. Python picks one
for you, silently, and it is the ordinal one: compare code points left to
right, stop at the first difference. This program names the four modes Python
actually has, measures where they disagree, and ends on the one case where all
four are wrong together.

Nothing here depends on an installed locale. The one linguistic API in the
stdlib -- locale.strxfrm -- is exercised under the C locale on purpose, and the
program reports what that gives back rather than an order that would differ
between two machines.
"""

import locale
import re
import unicodedata

# Two ways to write one letter. Named rather than pasted, so that the source
# says which is which where a rendered 'é' could not.
E_PRE = "é"        # LATIN SMALL LETTER E WITH ACUTE -- one code point
E_DEC = "é"       # 'e' + COMBINING ACUTE ACCENT    -- two code points

# Four spellings of one word: each 'é' independently written either way.
SPELLINGS = {
    "A": "r" + E_PRE + "sum" + E_PRE,
    "B": "r" + E_PRE + "sum" + E_DEC,
    "C": "r" + E_DEC + "sum" + E_PRE,
    "D": "r" + E_DEC + "sum" + E_DEC,
}
LABELS = list(SPELLINGS)


def code_points(s):
    return " ".join(f"{ord(ch):04X}" for ch in s)


print("1. == IS ORDINAL -- PYTHON JUST NEVER SAYS THE WORD")
print("   Ordinal means: compare code points, left to right, first difference")
print("   wins. No alphabet, no locale, no case table, no normalization.\n")
left, right = SPELLINGS["A"], SPELLINGS["D"]
first_diff = next(i for i in range(len(left)) if left[i] != right[i])
print(f"     the two strings print as        {left} and {right}")
print(f"     left == right                   {left == right}")
print(f"     len(left), len(right)           {len(left)}, {len(right)}")
print(f"     first differing position        {first_diff}")
print(f"     the two code points there       U+{ord(left[first_diff]):04X} and U+{ord(right[first_diff]):04X}")
print("\n     That is the whole rule. Every str comparison in Python obeys it,")
print("     and none of them takes an argument that could change it.")

print("\n2. FOUR SPELLINGS OF ONE WORD")
print("   To a reader these are the same word, four times:\n")
for label in LABELS:
    print(f"     {label}   {SPELLINGS[label]}")
print("\n   To Python they are four different values:\n")
for label in LABELS:
    s = SPELLINGS[label]
    print(f"     {label}   len {len(s)}   {len(s.encode('utf-8')):>2} bytes   {code_points(s)}")

print("\n   Every pair, under ==:\n")
print(" " * 8 + "".join(f"{label:>7}" for label in LABELS))
for row in LABELS:
    cells = "".join(f"{SPELLINGS[row] == SPELLINGS[col]!s:>7}" for col in LABELS)
    print(f"     {row}  {cells}")
distinct = len(set(SPELLINGS.values()))
print(f"\n     {distinct} distinct values, so all 6 pairs are False. One word, four keys:")
print(f"     len(set(...)) is {distinct}, and a dict built from them has {distinct} entries.")

print("\n3. WHERE find() PUTS YOU")
print("   find() is ordinal too, so a needle matches one spelling and not the")
print("   other -- and the offset it returns moves with a letter you did not")
print("   search for.\n")
NEEDLES = [
    ("'e'", "e"),
    ("'e' with acute, precomposed", E_PRE),
    ("'e' then U+0301", E_DEC),
    ("'sum'", "sum"),
]
print("     " + f"{'needle':<29}" + "".join(f"{label:>5}" for label in LABELS))
for name, needle in NEEDLES:
    cells = "".join(f"{SPELLINGS[label].find(needle):>5}" for label in LABELS)
    print(f"     {name:<29}{cells}")
print("\n     Read the last row first: 'sum' is pure ASCII and appears in all")
print("     four, at index 2 in two of them and index 3 in the other two. The")
print("     accent is nowhere near the needle and it still moved the answer,")
print("     because a code point earlier in the string was written as two.")
print("\n     Rows one and three are the same four numbers, which is the")
print("     other half of it: in B, C and D the 'e' you find by searching for")
print("     a bare 'e' IS the front of the accented letter. 'e' is not in A at")
print("     all, and in D it is found at an index inside a letter:\n")
d = SPELLINGS["D"]
cut = d.find("e") + 1
print(f"     D.find('e')          {d.find('e')}")
print(f"     D[:{cut}] and D[{cut}:]      {ascii(d[:cut])} and {ascii(d[cut:])}")
print(f"     D.replace('e', 'a')  {d.replace('e', 'a')!r}   = {ascii(d.replace('e', 'a'))}")
print(f"     A.replace('e', 'a')  {SPELLINGS['A'].replace('e', 'a')!r}   = {ascii(SPELLINGS['A'].replace('e', 'a'))}")
print("\n     Slicing there leaves a combining accent stranded at the head of")
print("     the tail, and replacing 'e' with 'a' carries both accents onto the")
print("     'a'. In A the same call changes nothing: there is no 'e' in A.")

print("\n4. THREE CASE-INSENSITIVE ANSWERS, AND NO TWO OF THEM AGREE")
print("   .NET spells this OrdinalIgnoreCase and gives you exactly one.")
print("   Python has three, spelled as unrelated APIs, and picking one is")
print("   picking a mode. WHY lower() and casefold() differ is its own page;")
print("   this table is only about how far apart the three answers land.\n")
PAIRS = [
    ("STRASSE", "stra\u00dfe", "German sharp s"),
    ("\u03a3", "\u03c2", "Greek final sigma"),
    ("K", "k", "KELVIN SIGN U+212A"),
    ("I", "\u0131", "Turkish dotless i"),
    ("\uab70", "\u13a0", "Cherokee A, both cases"),
]
print(f"     {'left':<11}{'right':<10}{'==':>7}{'lower':>8}{'casefold':>10}{'re.I':>7}   what it is")
for a, b, what in PAIRS:
    hit = re.fullmatch(re.escape(a), b, re.IGNORECASE) is not None
    print(f"     {a!r:<11}{b!r:<10}{a == b!s:>7}{a.lower() == b.lower()!s:>8}"
          f"{a.casefold() == b.casefold()!s:>10}{hit!s:>7}   {what}")
print("\n     Two rows carry the lesson. re.IGNORECASE will not match STRASSE")
print("     against stra\u00dfe, which casefold() does -- it has no one-to-two")
print("     mappings, so on that row it sides with lower(). And it WILL match")
print("     'I' against Turkish dotless '\u0131', which casefold() refuses,")
print("     because those are two different letters -- so on that row it sides")
print("     with neither. Three APIs, three questions, and nothing at the call")
print("     site says which one you asked.")
cherokee = "\uab70"
print("\n     One more pair, because it shows casefold() is a mapping in its")
print("     own right rather than a thorough lower():\n")
print(f"       {cherokee!r}.lower()     {cherokee.lower()!r}   (already lowercase, so nothing to do)")
print(f"       {cherokee!r}.casefold()  {cherokee.casefold()!r}   ({unicodedata.name(cherokee.casefold())})")
print("\n     The fold of a Cherokee small letter is a CAPITAL. Whatever")
print("     casefold() is, it is not lower() with more entries.")

print("\n5. THE LINGUISTIC MODE, AND HOW LITTLE OF IT PYTHON HAS")
print("   .NET's default is culture-sensitive. Python's only stdlib door to")
print("   that is locale.strxfrm, which asks the C library for a sort key.\n")
locale.setlocale(locale.LC_COLLATE, "C")
sample = SPELLINGS["A"]
print(f"     locale.strxfrm({sample!r})")
print(f"       -> {locale.strxfrm(sample)!r}")
print(f"       identical to the input?  {locale.strxfrm(sample) == sample}")
print("\n     Under the C locale there are no rules to apply, so the linguistic")
print("     API hands back the ordinal answer -- silently, with no error and no")
print("     flag. That is the state a container, a cron job and a CI runner all")
print("     start in. It is also process-global state, and not thread-safe.")

print("\n6. THE NUL CHARACTER, WHERE THE MODES DISAGREE MOST")
print("   A NUL inside a string is the case that separates the three modes")
print("   furthest, because a comparison that ignores it will call two")
print("   different strings equal. Here is what Python does with three")
print("   strings that differ by nothing else.\n")
NUL = chr(0)
TRIO = ["admin", "admin" + NUL, "ad" + NUL + "min"]
for s in TRIO:
    roundtrips = s.encode("utf-8").decode("utf-8") == s
    print(f"     {s!r:<13} len {len(s)}   utf-8 {s.encode('utf-8')!r:<14} "
          f"decodes back unchanged: {roundtrips}")
print(f"\n     TRIO[0] == TRIO[1]     {TRIO[0] == TRIO[1]}")
print(f"     TRIO[0] == TRIO[2]     {TRIO[0] == TRIO[2]}")
print(f"     len(set(TRIO))         {len(set(TRIO))}")
print(f"     distinct hashes        {len({hash(s) for s in TRIO})}")
print(f"     'admin' in TRIO[2]     {'admin' in TRIO[2]}")
print("\n     Ordinal says three different strings, and that is the right")
print("     answer: NUL is a character like any other, it encodes to one")
print("     ordinary byte, and UTF-8 round-trips it without complaint.")
print("\n     Now hand the same three to the linguistic API:\n")
for s in TRIO:
    try:
        outcome = repr(locale.strxfrm(s))
    except ValueError as exc:
        outcome = f"{type(exc).__name__}: {exc}"
    print(f"     locale.strxfrm on {s!r:<13} -> {outcome}")
print("\n     Python does not ignore the NUL, and it does not compare it")
print("     either. It refuses the string. That is a third possible behaviour,")
print("     and it is the one worth having: the two strings are not equal, and")
print("     the call that cannot say so fails instead of guessing.")

print("\n7. SO WHICH MODE FIXES THE FOUR SPELLINGS? NONE OF THEM.")
print("   Count the distinct values the four collapse to under each mode.")
print("   1 would mean all four finally agree.\n")
words = list(SPELLINGS.values())
MODES = [
    ("== (ordinal)", lambda s: s),
    ("lower()", str.lower),
    ("casefold()", str.casefold),
    ("locale.strxfrm, C locale", locale.strxfrm),
    ("NFC", lambda s: unicodedata.normalize("NFC", s)),
    ("NFD", lambda s: unicodedata.normalize("NFD", s)),
    ("NFC then casefold()", lambda s: unicodedata.normalize("NFC", s).casefold()),
]
for name, fn in MODES:
    print(f"     {name:<26} {len({fn(w) for w in words})}")
print("\n     Every comparison mode says four. Every normal form says one.")
print("     Comparison mode was never the question here: the four spellings")
print("     are four different strings, and no way of comparing four different")
print("     strings makes them one. Normalization is the fix, and it belongs")
print("     on the way in, once, at the boundary -- not in the comparison.")
