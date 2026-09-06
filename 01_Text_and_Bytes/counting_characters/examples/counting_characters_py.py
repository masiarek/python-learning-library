"""How long is a string? There are at least four answers, and wc knows three."""

import unicodedata

SAMPLES = [
    ("plain ASCII",        "cafe"),
    ("NFC - one char",     "café"),          # é as U+00E9
    ("NFD - two chars",    "café"),         # e + COMBINING ACUTE
    ("Polish",             "Zażółć"),
    ("emoji",              "\U0001F600"),
    ("flag",               "\U0001F1F5\U0001F1F1"),   # two regional indicators
    ("family",             "\U0001F468‍\U0001F469‍\U0001F467"),
]

print("1. FOUR ANSWERS TO 'HOW LONG IS THIS?'")
print(f"     {'sample':<18} {'len()':>6} {'utf-8':>6} {'utf-16':>7} {'graphemes':>10}")
print(f"     {'':<18} {'points':>6} {'bytes':>6} {'units':>7} {'(human)':>10}")
print("     " + "-" * 52)
for label, text in SAMPLES:
    points = len(text)
    utf8 = len(text.encode("utf-8"))
    utf16 = len(text.encode("utf-16-le")) // 2
    # A crude grapheme count: a new cluster starts at any character that is not
    # a combining mark, not a ZWJ, and not preceded by a ZWJ. Real segmentation
    # is UAX #29 and needs a library; this is enough to show the gap exists.
    clusters, prev_zwj = 0, False
    for ch in text:
        combining = unicodedata.combining(ch) != 0
        zwj = ch == "‍"
        if not combining and not zwj and not prev_zwj:
            clusters += 1
        prev_zwj = zwj
    print(f"     {label:<18} {points:>6} {utf8:>6} {utf16:>7} {clusters:>10}")

print("\n     Read the 'family' row: one thing on your screen, five code points,")
print("     eighteen UTF-8 bytes. Every column is a legitimate answer to a")
print("     different question, and len() only ever answers one of them.")

print("\n2. THE TRAP THAT LOOKS LIKE A BUG")
nfc, nfd = "café", "café"
print(f"     nfc = {nfc!r}   len = {len(nfc)}")
print(f"     nfd = {nfd!r}   len = {len(nfd)}")
print(f"     they print identically:      {nfc} == {nfd}")
print(f"     nfc == nfd                   {nfc == nfd}")
print(f"     after normalize('NFC', ...)  {unicodedata.normalize('NFC', nfc) == unicodedata.normalize('NFC', nfd)}")
print("\n     Two strings that look the same, print the same, and compare False.")
print("     Normalize before comparing text that came from somewhere else.")

print("\n3. WHAT wc COUNTS, AND WHICH len() MATCHES IT")
text = "Zażółć gęślą jaźń\n"
raw = text.encode("utf-8")
print(f"     text  = {text!r}")
print(f"     bytes = {len(raw)}   <- wc -c   len(text.encode('utf-8'))")
print(f"     chars = {len(text)}   <- wc -m   len(text)")
print(f"     words = {len(text.split())}    <- wc -w   len(text.split())")
print(f"     lines = {text.count(chr(10))}    <- wc -l   counts NEWLINES, not lines")
print("\n     wc -c and wc -m differ by 9 here, and a wc that only reads bytes")
print("     cannot tell you the second number at all.")

print("\n4. THE LINE COUNT IS A NEWLINE COUNT")
for label, sample in [("with trailing \\n", "a\nb\n"), ("without", "a\nb")]:
    print(f"     {label:<18} {sample!r:<10} count('\\n') = {sample.count(chr(10))}"
          f"   but there are {len(sample.splitlines())} lines")
print("\n     Without a trailing newline both wc -l and count(chr(10)) say 1 where a")
print("     person says 2 -- they agree because they are the same rule. splitlines()")
print("     is the one that answers the question a person actually asked.")

print("\n5. str.split() IS NOT A WORD DEFINITION")
for sample in ["one  two", "hyphen-ated", "don't", "łódź łódź"]:
    print(f"     {sample!r:<26} -> {len(sample.split()):>2} {sample.split()}")
print("\n     The last one holds a NO-BREAK SPACE (U+00A0). str.split() treats it")
print("     as whitespace, so Python says two words; a tool splitting on ASCII")
print("     space alone would say one. 'Word' is a policy, not a fact.")
