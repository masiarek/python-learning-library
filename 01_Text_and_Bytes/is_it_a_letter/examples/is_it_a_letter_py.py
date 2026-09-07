"""Twelve predicates named is*, and the four different questions they ask."""

import unicodedata as ud

# Code points chosen so that every predicate disagrees with at least one other.
SAMPLES = [
    0x0041,   # LATIN CAPITAL LETTER A
    0x0141,   # LATIN CAPITAL LETTER L WITH STROKE  (Polish Ł)
    0x01C5,   # LATIN CAPITAL LETTER D WITH SMALL LETTER Z WITH CARON (titlecase)
    0x0345,   # COMBINING GREEK YPOGEGRAMMENI       (a mark, but Alphabetic)
    0x093E,   # DEVANAGARI VOWEL SIGN AA            (a mark, but Alphabetic)
    0x16EE,   # RUNIC ARLAUG SYMBOL                 (a number that is a letter)
    0x2167,   # ROMAN NUMERAL EIGHT
    0x00B2,   # SUPERSCRIPT TWO
    0x00BD,   # VULGAR FRACTION ONE HALF
    0x0663,   # ARABIC-INDIC DIGIT THREE
    0x4E00,   # CJK UNIFIED IDEOGRAPH-4E00          (one)
    0x005F,   # LOW LINE
]

PREDICATES = [m for m in dir(str) if m.startswith("is")]


print("1. TWELVE PREDICATES, AND WHAT THE EMPTY STRING DOES")
false_on_empty = [m for m in PREDICATES if not getattr("", m)()]
true_on_empty = [m for m in PREDICATES if getattr("", m)()]
print(f"     str has {len(PREDICATES)} methods whose name starts with 'is'.")
print(f"     False on '':  {' '.join(false_on_empty[:5])}")
print(f"                   {' '.join(false_on_empty[5:])}")
print(f"     True  on '':  {' '.join(true_on_empty)}")
print()
print(f"     The {len(false_on_empty)} say 'every character is X, and there is at least one'.")
print(f"     The {len(true_on_empty)} say 'no character is NOT X', which is vacuously true when")
print("     there are no characters. Same suffix, opposite empty-string rule.")

print("\n2. WHAT isalpha ACTUALLY ASKS")
print(f"     {'code point':<11} {'cat':<4} {'alpha':<6} {'numeric':<8} {'digit':<6} name")
print("     " + "-" * 76)
for cp in SAMPLES:
    ch = chr(cp)
    name = ud.name(ch)
    print(
        f"     U+{cp:04X}      {ud.category(ch):<4} "
        f"{str(ch.isalpha()):<6} {str(ch.isnumeric()):<8} {str(ch.isdigit()):<6} "
        f"{name}"
    )
print()
print("     isalpha() is exactly 'General_Category starts with L'. That is why")
print("     the two marks are False -- they are Mn and Mc, and a mark is not a")
print("     letter however alphabetic it looks -- and why U+4E00 is True: a CJK")
print("     ideograph is Lo, so it is a letter AND it has a numeric value.")

print("\n3. THREE KINDS OF NUMBER, NESTED")
print(f"     {'code point':<11} {'isdecimal':<10} {'isdigit':<8} {'isnumeric':<10} name")
print("     " + "-" * 68)
for cp in (0x0033, 0x0663, 0x00B2, 0x00BD, 0x2167, 0x4E00):
    ch = chr(cp)
    print(
        f"     U+{cp:04X}      {str(ch.isdecimal()):<10} {str(ch.isdigit()):<8} "
        f"{str(ch.isnumeric()):<10} {ud.name(ch)}"
    )
violations = sum(
    1
    for cp in range(0x110000)
    if (chr(cp).isdecimal() and not chr(cp).isdigit())
    or (chr(cp).isdigit() and not chr(cp).isnumeric())
)
print()
print("     Checked over every one of the 1,114,112 code points:")
print(f"     isdecimal implies isdigit implies isnumeric, violations = {violations}")
print("     isdecimal is 'you can build a base-10 number out of it' (Nd).")
print("     isdigit adds the ones with a digit VALUE but no positional use.")
print("     isnumeric adds everything with a numeric value at all -- halves,")
print("     Roman numerals, and the CJK ideograph for 'one'.")

print("\n4. isalnum IS THE UNION OF FOUR, NOT OF TWO")
for cp in (0x0041, 0x00BD, 0x005F):
    ch = chr(cp)
    union = ch.isalpha() or ch.isdecimal() or ch.isdigit() or ch.isnumeric()
    print(
        f"     U+{cp:04X}  isalnum={str(ch.isalnum()):<6} "
        f"alpha or decimal or digit or numeric = {union}"
    )
print()
print("     So U+00BD (one half) is 'alphanumeric' in Python. If you are")
print("     validating a username, isalnum() is almost never the rule you meant.")

print("\n5. isupper IGNORES EVERY UNCASED CHARACTER")
for s in ("ABC", "ABC1", "123", "ABC-DEF", "Ł", "ǅ"):
    print(
        f"     {s!r:<10} isupper={str(s.isupper()):<6} "
        f"islower={str(s.islower()):<6} istitle={s.istitle()}"
    )
print()
print("     'ABC1' is uppercase because the digit has no case to disagree with.")
print("     '123' is not, because there is no cased character to agree with it.")
print("     The rule is 'at least one cased character, and no cased character")
print("     is in the wrong case' -- not 'every character is uppercase'.")

print("\n6. NONE OF THESE IS all()")
for s in ("", "abc", "ab1"):
    every = all(c.isalpha() for c in s)
    print(f"     {s!r:<7} .isalpha() = {str(s.isalpha()):<6} all(c.isalpha()) = {every}")
print()
print("     They agree on every string except the empty one, where all() is")
print("     True by definition and isalpha() is False by decision. Translating")
print("     s.isalpha() into a language that only has per-character predicates")
print("     means writing the emptiness test back in by hand.")

print("\n7. bytes HAS EIGHT OF THE TWELVE, AND THEY ARE ASCII-ONLY")
byte_preds = [m for m in dir(bytes) if m.startswith("is")]
print(f"     bytes has {len(byte_preds)}: {' '.join(byte_preds)}")
print(f"     str-only:  {' '.join(sorted(set(PREDICATES) - set(byte_preds)))}")
print()
print(f"     {'text':<8} {'codec':<8} {'the bytes':<30} {'bytes':<8} str")
print("     " + "-" * 62)
for text, codec in (("Lodz", "utf-8"), ("Łódź", "utf-8"), ("Łódź", "cp1250")):
    raw = text.encode(codec)
    print(
        f"     {text!r:<8} {codec:<8} {raw!r:<30} "
        f"{str(raw.isalpha()):<8} {text.isalpha()}"
    )
print()
print("     The last column is str.isalpha() on the text those bytes decode to.")
print("     The four missing ones are the four that need the Unicode table:")
print("     isdecimal, isnumeric, isprintable, isidentifier. The eight that")
print("     remain answer only for ASCII, because a bytes object does not know")
print("     which table produced it -- so a Polish name is 'not alphabetic' in")
print("     every encoding, and the same call on the str it decodes to is True.")
