"""A slice never raises. An index does. Same brackets, two contracts.

The spine is the invariant s[:n] + s[n:] == s, which holds for EVERY integer n
-- negative, past the end, larger than the machine's word. It is tested here
rather than asserted, because "never raises" is a claim about all inputs and
the only honest way to show it is to try a lot of them.
"""

import sys
import unicodedata

S = "Monty"
PAD = 4  # how far past each end of S to test


def outcome(fn):
    """Run fn; return its repr, or the name of the exception type it raised."""
    try:
        return repr(fn())
    except Exception as exc:  # the TYPE is the answer; the message is not API
        return type(exc).__name__


print("1. THE INVARIANT, TESTED RATHER THAN ASSERTED")
print(f"     s = {S!r}   len {len(S)}")
print()
print("     For every n, cutting the string in two at n and gluing it back")
print("     together returns the original. Including n past both ends.")
print()
print(f"     {'n':>5}   {'s[:n]':<9} {'s[n:]':<9} {'joined':<9} == s")
print("     " + "-" * 52)
lo, hi = -(len(S) + PAD), len(S) + PAD
for n in range(lo, hi + 1):
    head, tail = S[:n], S[n:]
    marker = "  <- past the end" if n >= len(S) else ""
    marker = "  <- past the start" if n <= -len(S) else marker
    print(f"     {n:>5}   {head!r:<9} {tail!r:<9} {head + tail!r:<9} {head + tail == S}{marker}")
print()
print(f"     {hi - lo + 1} values of n, {hi - lo + 1} times True, zero exceptions.")

print("\n2. THE SWEEP: SEVEN STRINGS, AND NUMBERS NO MACHINE CAN INDEX WITH")
CORPUS = [
    ("empty", ""),
    ("one character", "M"),
    ("ASCII", "Monty"),
    ("Polish", "Łódź"),
    ("e + combining acute", "café"),
    ("regional indicators", "\U0001F1F5\U0001F1F1"),
    ("a whole sentence", "zażółć gęślą jaźń"),
]
tested = failures = 0
for _, text in CORPUS:
    for n in range(-(len(text) + 8), len(text) + 9):
        tested += 1
        if text[:n] + text[n:] != text:
            failures += 1
print(f"     {len(CORPUS)} strings x every n from -(len+8) to len+8")
print(f"     {tested} values of n tested, {failures} failures")
print()
BIG = 10**30
print("     And n does not have to fit in a machine word:")
print(f"       s[:10**30]                {S[:BIG]!r}")
print(f"       s[10**30:]                {S[BIG:]!r}")
print(f"       s[-10**30:]               {S[-BIG:]!r}")
print(f"       s[:10**30] + s[10**30:]   {S[:BIG] + S[BIG:]!r}   == s: {S[:BIG] + S[BIG:] == S}")
print("     A slice of ten-to-the-thirty is not an error. It is 'Monty'.")

print("\n3. THE SAME BRACKETS, TWO CONTRACTS")
print("     s[n] and s[n:n+1] look like the same question asked twice.")
print("     They are not. One of them is allowed to fail.")
print()
print(f"     {'n':>5}   {'s[n]':<12} s[n:n+1]")
print("     " + "-" * 44)
raised = 0
for n in range(lo, hi + 1):
    got = outcome(lambda n=n: S[n])
    raised += got == "IndexError"
    note = "  <- the two disagree" if n == -1 else ""
    print(f"     {n:>5}   {got:<12} {S[n:n + 1]!r:<10}{note}".rstrip())
print()
print(f"     s[n]     raised on {raised} of {hi - lo + 1} values")
print(f"     s[n:n+1] raised on 0 of {hi - lo + 1}, and returned '' at every n where")
print("              s[n] raised. One row goes the other way, and it is not a")
print("              third contract -- it is section 5's arithmetic again:")
print(f"                s[-1]     {S[-1]!r}")
print(f"                s[-1:0]   {S[-1:0]!r}     n + 1 is 0, and 0 as a STOP means")
print("                          position zero, not 'the end'. The slice asks for")
print("                          everything from the last character up to the")
print("                          first, which is nothing.")
print()
print("     The bracket is one syntax over two protocols. What goes inside")
print("     decides which:")
print(f"       s[1]     passes an {type(1).__name__} to __getitem__")
print(f"       s[1:3]   passes a {type(slice(1, 3)).__name__} to __getitem__ -- a real object")
print(f"       s.__getitem__(slice(1, 100))   {S.__getitem__(slice(1, 100))!r}")
print(f"       s.__getitem__(100)             {outcome(lambda: S.__getitem__(100))}")
print(f"       s[10**30]                      {outcome(lambda: S[BIG])}")
print("     Both failures are IndexError; neither slice is.")

print("\n4. WHY A SLICE CANNOT FAIL: slice.indices() IS THE CLAMPING RULE")
print("     Every slice runs its bounds through this first. It takes the")
print("     length and returns start, stop and step already in range.")
print()
print(f"     {'written':<14} {'the slice object':<26} {'.indices(5)':<16} result")
print("     " + "-" * 72)
SPELLINGS = [
    ("s[:3]", slice(None, 3)),
    ("s[3:]", slice(3, None)),
    ("s[1:100]", slice(1, 100)),
    ("s[100:]", slice(100, None)),
    ("s[-100:]", slice(-100, None)),
    ("s[:-1]", slice(None, -1)),
    ("s[:-0]", slice(None, -0)),
    ("s[::2]", slice(None, None, 2)),
    ("s[::-1]", slice(None, None, -1)),
]
for written, sl in SPELLINGS:
    print(f"     {written:<14} {sl!r:<26} {str(sl.indices(len(S))):<16} {S[sl]!r}")
print()
print("     Nothing in that column is out of range, because clamping happened")
print("     before the string was touched. 100 became 5. -100 became 0.")

print("\n5. NEGATIVE INDICES, AND THE -0 ASYMMETRY")
print("     A negative index counts back from the end. len(s) is added to it,")
print("     once, and then the ordinary rules apply.")
print()
for n in (-1, -2, -5, -6):
    print(f"       s[{n}]  -> {outcome(lambda n=n: S[n]):<12} (len + n = {len(S) + n})")
print()
print("     So s[-1] is the last character. And yet:")
print(f"       s[:-1]   {S[:-1]!r}    everything but the last")
print(f"       s[:-0]   {S[:-0]!r}         empty")
print()
print("     Not an inconsistency in slicing -- an arithmetic fact that never")
print("     reaches it. The minus is gone before the slice exists:")
print(f"       -0 == 0            {-0 == 0}")
print(f"       repr(slice(None, -0))   {slice(None, -0)!r}")
print("     The slice object itself has no memory of the sign. Which means")
print("     'drop the last n characters' as s[:-n] is a bug waiting for n = 0,")
print("     and s[:len(s) - n] is the version that survives it.")

print("\n6. THE THIRD SLOT")
STEPS = [
    ("s[::2]", lambda: S[::2], "every second character"),
    ("s[1::2]", lambda: S[1::2], "offset by one"),
    ("s[::-1]", lambda: S[::-1], "the idiomatic reverse"),
    ("s[::-2]", lambda: S[::-2], "backwards, every second"),
    ("s[::10**30]", lambda: S[::10**30], "a step no machine can count to"),
    ("s[::0]", lambda: S[::0], "the one value that DOES raise"),
]
for written, fn, note in STEPS:
    print(f"       {written:<13} {outcome(fn):<12} {note}")
print()
print("     A step of zero is the single exception to 'a slice never raises',")
print("     and it is not about the bounds -- it is a ValueError, not an")
print("     IndexError, because no clamping can make a step of zero mean")
print("     anything. Every out-of-range bound is still fine, and so is every")
print("     other step:")
print(f"       s[100:-100:-1]   {S[100:-100:-1]!r}")
print(f"       s[::-10**30]     {S[::-10**30]!r}")
print("     (A non-integer in any of the three slots is a TypeError, but that")
print("     is the argument being the wrong kind of thing, not out of range.)")

print("\n7. s[::-1] REVERSES CODE POINTS, NOT CHARACTERS")
print("     The famous one-liner is correct for ASCII and wrong for a large")
print("     fraction of the world's text. Reversing a sequence is only")
print("     reversing a string when every element stands alone.")
print()
SAMPLES = [
    ("cafe + U+0301", "café"),
    ("precomposed", "café"),
    ("flag of Poland", "\U0001F1F5\U0001F1F1"),
    ("family", "\U0001F468‍\U0001F469‍\U0001F467‍\U0001F466"),
    ("Devanagari", "नमस्ते"),
]
for label, text in SAMPLES:
    rev = text[::-1]
    print(f"     {label}")
    print(f"       original  len {len(text)}   {text}   {text!r}")
    print(f"       reversed  len {len(rev)}   {rev}   {rev!r}")
    for name, seq in (("was", text), ("now", rev)):
        names = " ".join(f"U+{ord(c):04X}" for c in seq)
        print(f"       {name}       {names}")
    print()
print("     Read the first pair again. 'cafe' plus a COMBINING ACUTE ACCENT")
print("     renders as cafe-with-an-accent; reversed, the accent is now the")
print("     FIRST code point in the string, with nothing before it to sit on.")
print("     A combining mark attaches to what precedes it, and after a")
print("     reversal what precedes it is whatever came next in the sentence.")
print()
acute = "café"[-1]
print(f"     U+0301 category {unicodedata.category(acute)}, combining class "
      f"{unicodedata.combining(acute)}")
print("     Mn means 'mark, nonspacing': by definition it has no width of its")
print("     own and modifies its neighbour. Slicing does not know that.")
print()
print("     The flag is two REGIONAL INDICATOR letters, P and L, which a font")
print("     draws as one flag. Reversed they spell L then P -- not a country")
print("     code, so it renders as two letters and Poland is gone. The family")
print("     is four people joined by three ZERO WIDTH JOINERs; the joiners")
print("     survive the reversal and the order of the people does not.")
print()
print("     None of these raised. Every one of them is a different string that")
print("     the type system, the linter and the test suite all call a str.")

print("\n8. 'THE FIRST N CHARACTERS' IS NOT WHAT s[:n] GIVES YOU")
NFD = "café"
print(f"     s = {NFD!r}   which renders as {NFD} -- four characters to a reader")
print()
for n in range(1, len(NFD) + 1):
    points = " ".join(f"U+{ord(c):04X}" for c in NFD[:n])
    print(f"       s[:{n}]   {points:<36} renders as  {NFD[:n]}")
print()
print("     s[:4] is the 'first four characters' of a four-character word and")
print("     it is a different word. The accent was code point five.")
print()
FLAG = "\U0001F1F5\U0001F1F1"
FAM = "\U0001F468‍\U0001F469‍\U0001F467‍\U0001F466"
print(f"       flag[:1]     U+{ord(FLAG[0]):04X}                            half a flag")
print(f"       family[:2]   U+{ord(FAM[0]):04X} U+{ord(FAM[1]):04X}                     a man and a trailing joiner")
print()
print("     s[:n] is 'the first n code points', which is the right answer to a")
print("     question about storage and the wrong one to a question about text.")

print("\n9. bytes SLICES TO bytes; bytes INDEXES TO AN int")
DATA = "Łódź".encode()
print(f"     data = {DATA!r}   len {len(DATA)}")
print(f"       data[0]     {DATA[0]!r:<10} {type(DATA[0]).__name__}")
print(f"       data[0:1]   {DATA[0:1]!r:<10} {type(DATA[0:1]).__name__}")
print("     Two contracts again, and this time they differ in RETURN TYPE as")
print("     well as in failure mode.")
print()
print("     The invariant holds here too, over the same range:")
bytes_ok = all(DATA[:n] + DATA[n:] == DATA for n in range(-(len(DATA) + 8), len(DATA) + 9))
print(f"       data[:n] + data[n:] == data for every n:   {bytes_ok}")
print()
print(f"       data[::-1]            {DATA[::-1]!r}")
print(f"       data[::-1].decode()   {outcome(lambda: DATA[::-1].decode())}")
print("     Reversing bytes does not reverse text. It shreds the encoding,")
print("     and here it fails loudly -- which is the good case.")

if failures:  # the page's whole claim; refuse to record a key that contradicts it
    sys.exit("INVARIANT FAILED")
