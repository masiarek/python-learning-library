"""Lowercasing is case CONVERSION. Case-insensitivity is case FOLDING. Different operations."""

import string
import sys

MAX = sys.maxunicode + 1


def cps(s):
    """A string as its code points, so a combining mark cannot hide in the margin."""
    return " ".join("U+%04X" % ord(c) for c in s)


print("1. THE CLAIM, IN ONE PAIR OF WORDS")
print("     Two spellings of one German word. A reader calls them the same word.")
print()
print(f"     'straße'   len {len('straße')}")
print(f"     'STRASSE'  len {len('STRASSE')}")
print()
for left, right in [("straße", "STRASSE")]:
    print(f"     lower()     {left.lower()!r:<12} vs {right.lower()!r:<12} equal = {left.lower() == right.lower()}")
    print(f"     upper()     {left.upper()!r:<12} vs {right.upper()!r:<12} equal = {left.upper() == right.upper()}")
    print(f"     casefold()  {left.casefold()!r:<12} vs {right.casefold()!r:<12} equal = {left.casefold() == right.casefold()}")
print()
print("     lower() is the folklore fix for case-insensitive comparison and it")
print("     is the one that fails. casefold() is the operation Unicode defines")
print("     for the question 'is this the same word ignoring case'.")

print("\n2. THE CHARACTERS THAT DO IT")
print(f"     {'code point':<11} {'char':<5} {'lower()':<8} {'upper()':<8} {'casefold()':<11} why")
print("     " + "-" * 82)
rows = [
    ("ß", "no capital of its own to come back from"),
    ("ẞ", "the capital added in 2008; lower stops at ß"),
    ("ſ", "long s -- already lowercase, so lower() is a no-op"),
    ("µ", "MICRO SIGN; folding sends it to Greek small mu"),
    ("ς", "final sigma; folding erases the positional form"),
]
for ch, why in rows:
    print(f"     {cps(ch):<11} {ch!r:<5} {ch.lower()!r:<8} {ch.upper()!r:<8} {ch.casefold()!r:<11} {why}")
print()
folding_differs = sum(1 for cp in range(MAX) if chr(cp).casefold() != chr(cp).lower())
print(f"     Checked over all {MAX:,} code points: {folding_differs} of them have a")
print("     casefold() that is not their lower(). Every one is a character where")
print("     'lowercase both sides and compare' gives the wrong answer.")

print("\n3. A STRING CAN GET LONGER WHEN YOU CHANGE ITS CASE")
grow = {}
for op in ("upper", "lower", "casefold", "title"):
    grow[op] = [(cp, getattr(chr(cp), op)()) for cp in range(MAX) if len(getattr(chr(cp), op)()) != 1]
print("     method        code points mapping to more than one character   longest")
print("     " + "-" * 70)
for op in ("upper", "lower", "casefold", "title"):
    longest = max((len(r) for _, r in grow[op]), default=1)
    print(f"     {op + '()':<14}{len(grow[op]):>10}{longest:>44}")
print()
shorter = [op for op in grow if any(len(r) < 1 for _, r in grow[op])]
print("     Nothing ever gets shorter: methods with a code point mapping to")
print(f"     zero characters = {len(shorter)}.")
print()
print("     One character in, three characters out:")
for cp, out in sorted(grow["upper"], key=lambda t: (-len(t[1]), t[0]))[:3]:
    print(f"       {chr(cp)!r} ({cps(chr(cp))})  .upper()  ->  {out!r}  ({cps(out)})")
print()
print("     And exactly one code point in the whole table grows under lower():")
for cp, out in grow["lower"]:
    print(f"       {chr(cp)!r} ({cps(chr(cp))})  .lower()  ->  {out!r}  ({cps(out)})")
print("     -- the Turkish dotted capital I, which section 5 comes back to.")

print("\n4. AND CASE IS NOT A PER-CHARACTER OPERATION AT ALL")
print("     Greek sigma has two lowercase forms. Which one you get depends on")
print("     where the letter sits in the word, so the whole string is the input.")
print()
print(f"     {'string':<9} {'.lower()':<10} {'per character':<15} {'same?':<7} code points of .lower()")
print("     " + "-" * 84)
for s in ["ΟΔΟΣ", "ΟΔΟΣ.", "ΣΟΦΟΣ", "ΑΣΑ", "Σ"]:
    whole = s.lower()
    piece = "".join(c.lower() for c in s)
    print(f"     {s:<9} {whole:<10} {piece:<15} {str(whole == piece):<7} {cps(whole)}")
print()
greek = range(0x0370, 0x0400)
disagree = sum(
    1
    for a in greek
    for b in greek
    if (chr(a) + chr(b)).lower() != chr(a).lower() + chr(b).lower()
)
print(f"     Over every two-character string from the Greek block, {disagree} of them")
print("     lower differently as a string than character by character. So")
print("     ''.join(c.lower() for c in s) is not a refactoring of s.lower().")
print()
print("     casefold() takes the other road and erases the distinction:")
for s in ["ΟΔΟΣ"]:
    print(f"       {s!r}.lower()     {s.lower()!r}   {cps(s.lower())}")
    print(f"       {s!r}.casefold()  {s.casefold()!r}   {cps(s.casefold())}")
print("     -- which is the point of folding: two spellings, one key.")

print("\n5. THE CONTEXT PYTHON DOES NOT TAKE: THE LANGUAGE")
print("     In Turkish, i and ı are two different letters, and so are İ and I.")
print("     Casing them correctly needs to know the text is Turkish. Python's")
print("     case methods take no such argument -- there is nowhere to say it:")
for call, fn in [("'I'.lower('tr')", lambda: "I".lower("tr")), ("str.upper('i', 'tr')", lambda: str.upper("i", "tr"))]:
    try:
        fn()
        verdict = "accepted"
    except Exception as exc:
        verdict = type(exc).__name__
    print(f"       {call:<24} -> {verdict}")
print()
print("     So the same four letters give the same answers on every machine,")
print("     in every locale, and none of them is the Turkish answer:")
print()
print(f"     {'char':<12} {'Python .lower()':<21} {'Python .upper()':<17} {'Turkish wants':<17} agrees?")
print("     " + "-" * 84)
TURKISH = {"I": ("ı", "I"), "i": ("i", "İ"), "İ": ("i", "İ"), "ı": ("ı", "I")}
for ch in ["I", "i", "İ", "ı"]:
    low, up = ch.lower(), ch.upper()
    t_low, t_up = TURKISH[ch]
    print(f"     {cps(ch):<12} {cps(low):<21} {cps(up):<17} {cps(t_low) + ' / ' + cps(t_up):<17} {(low, up) == (t_low, t_up)}")
print()
print("     The 'Turkish wants' column is written out by hand from the")
print("     conditional section of the Unicode data. Python implements the")
print("     UNconditional mappings and not the language-tailored ones, which")
print("     is a documented choice, not an omission -- and it is why 'I'.lower()")
print("     is 'i' here whatever LANG says.")
print()
print("     Note the shape of the failure. Uppercasing merges two Turkish")
print(f"     letters: 'ı'.upper() is {'ı'.upper()!r} and 'i'.upper() is {'i'.upper()!r}.")
print("     Lowercasing splits one into two code points:")
print(f"       'İ'.lower()     {'İ'.lower()!r}   {cps('İ'.lower())}   len {len('İ'.lower())}")
print(f"       'İ'.casefold()  {'İ'.casefold()!r}   {cps('İ'.casefold())}   len {len('İ'.casefold())}")
print(f"       'İstanbul'.casefold() == 'istanbul'.casefold()  ->  {'İstanbul'.casefold() == 'istanbul'.casefold()}")
print("     -- so casefold() does not rescue Turkish either. It is the right")
print("     answer to a question that is not about a specific language.")

print("\n6. THERE IS A THIRD CASE, AND IT IS A CHARACTER")
print(f"     {'code point':<11} {'category':<9} {'the char':<10} {'.upper()':<10} {'.lower()':<10} .title()")
print("     " + "-" * 66)
for cp, cat in ((0x01C4, "Lu"), (0x01C5, "Lt"), (0x01C6, "Ll")):
    ch = chr(cp)
    print(f"     {cps(ch):<11} {cat:<9} {ch!r:<10} {ch.upper()!r:<10} {ch.lower()!r:<10} {ch.title()!r}")
print()
print("     U+01C5 is titlecase: not the uppercase form, not the lowercase")
print("     form, a third one. That is why case has three methods and not two.")

print("\n7. THREE ANSWERS TO 'TITLE CASE', DISAGREEING ON ONE LINE")
print(f"     {'input':<20} {'.title()':<21} {'string.capwords()':<21} .capitalize()")
print("     " + "-" * 84)
for s in ["o'brien and sons", "ǆenan o'brien", "DON'T PANIC", "hello   world"]:
    print(f"     {s!r:<20} {s.title()!r:<21} {string.capwords(s)!r:<21} {s.capitalize()!r}")
print()
print("     Read the first two columns against each other and neither wins.")
print("     .title() breaks after every uncased character, so the apostrophe")
print("     starts a new word: it gets O'Brien right and Don'T wrong, from the")
print("     same rule. capwords() splits on whitespace and capitalizes only the")
print("     first letter of each piece, so it gets Don't right and O'brien")
print("     wrong -- also from one rule. And capwords() rejoins with a single")
print("     space, so it edits text you did not ask it to edit.")
print()
print("     All three do handle the third case correctly: the leading ǆ becomes")
print(f"     the titlecase ǅ ({cps('ǆ'.title())}) and not the capital Ǆ ({cps('ǆ'.upper())}).")
print("     They agree about Unicode and disagree about what a word is.")

print("\n8. NONE OF THE CONVERSIONS IS REVERSIBLE")
print(f"     {'char':<6} {'.upper()':<9} {'then .lower()':<14} {'.lower()':<9} back where it started?")
print("     " + "-" * 68)
for ch in ["ß", "ﬁ", "ŉ", "ı", "ς", "µ", "ſ"]:
    print(f"     {ch!r:<6} {ch.upper()!r:<9} {ch.upper().lower()!r:<14} {ch.lower()!r:<9} {ch.upper().lower() == ch}")
print()
idem = [op for op in ("lower", "upper", "casefold") if any(getattr(getattr(chr(cp), op)(), op)() != getattr(chr(cp), op)() for cp in range(MAX))]
swap_fails = sum(1 for cp in range(MAX) if chr(cp).swapcase().swapcase() != chr(cp))
print("     Applying one twice changes nothing the second time -- methods that")
print(f"     are not idempotent over the whole table: {len(idem)}.")
print(f"     But swapcase() is not its own inverse: {swap_fails} code points do not")
print(f"     come back. {'ß'!r} -> {'ß'.swapcase()!r} -> {'ß'.swapcase().swapcase()!r}, and the ß is gone for good.")

print("\n9. WHAT TO USE")
print(f"     {'the question you are asking':<38} the method")
print("     " + "-" * 72)
for q, m in [
    ("is this the same word, ignoring case", "casefold() on both sides"),
    ("show this to a person, uppercased", "upper()"),
    ("show this to a person, lowercased", "lower()"),
    ("a heading, English, no apostrophes", "title() -- and read it after"),
    ("a person's name", "none of them; store what they typed"),
    ("an ASCII protocol token", "lower() is safe, the input is ASCII"),
]:
    print(f"     {q:<38} {m}")
print()
print("     The last two rows are the ones that save time. Case conversion is")
print("     for display; case folding is for comparison; and a name is neither,")
print("     because no rule in the table knows about McDonald or van der Berg.")
