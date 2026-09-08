"""Answer key: eight brackets over one word, and only one of them may fail."""


def outcome(source):
    """Evaluate; return the repr, or the name of the exception type raised."""
    try:
        # ascii(), not repr(): a zero-width combining mark inside a repr
        # renders one column narrower than it counts, which silently breaks
        # every aligned column after it.
        return ascii(eval(source, {}))
    except Exception as exc:  # the TYPE is the answer; the message is not API
        return type(exc).__name__


CALLS = [
    ("'Monty'[5]", "one past the end -- an index may fail, and does"),
    ("'Monty'[5:]", "the same 5, clamped to len, so there is nothing left"),
    ("'Monty'[100:200]", "both bounds clamped to 5; still not an error"),
    ("'Monty'[:-1]", "-1 becomes 4: everything but the last"),
    ("'Monty'[:-0]", "-0 IS 0, so this is [:0] and the minus never arrived"),
    ("'Monty'[-1:0]", "start 4, stop 0: from the last up to the first"),
    ("'Monty'[::0]", "no clamping can give a step of zero a meaning"),
    ("'cafe\\u0301'[::-1]", "reversed by code point, so the accent leads"),
]

print(f"     {'expression':<22} {'result':<14} why")
print("     " + "-" * 86)
for source, note in CALLS:
    print(f"     {source:<22} {outcome(source):<14} {note}")

print()
print("     TWO FAILURES, AND THEY ARE DIFFERENT KINDS")
print("       'Monty'[5]     IndexError    a POSITION the string does not have")
print("       'Monty'[::0]   ValueError    a STEP no length can make sense of")
print("     Everything between those two rows is a slice with an out-of-range")
print("     bound, and not one of them raised. That is the page in one table:")
print("     bounds are clamped, positions are checked, and the brackets look")
print("     identical from the outside.")

print()
print("     LINE 5 AND LINE 6 ARE THE SAME ARITHMETIC TWICE")
S = "Monty"
print(f"       s[-1]     {S[-1]!r}      a negative index counts back: len + (-1) = 4")
print(f"       s[:-0]    {S[:-0]!r}       but -0 == 0, so there is nothing to count back")
print(f"       s[-1:0]   {S[-1:0]!r}       start 4, stop 0 -- and 0 as a STOP is a")
print("                         position, not 'the end'")
print(f"       repr(slice(None, -0))   {slice(None, -0)!r}")
print("     The slice object never sees a minus sign in either case. Both are")
print("     arithmetic that finished before slicing began.")

print()
print("     AND THE INVARIANT, OVER EIGHT NUMBERS -- FIVE OF THEM OUT OF RANGE")
NUMBERS = [5, 100, 200, -1, 0, 1, -5, 10**30]
worst = [n for n in NUMBERS if S[:n] + S[n:] != S]
for n in NUMBERS:
    label = "10**30" if n == 10**30 else str(n)
    print(f"       n = {label:<8} s[:n] {S[:n]!r:<9} s[n:] {S[n:]!r:<9} joined == s: {S[:n] + S[n:] == S}")
print(f"     failures: {len(worst)}")
print("     (-0 is not on that list, because it cannot be: written into a")
print("      list literal it is 0, exactly as it is written into a slice.)")
refused = sum(outcome(f"'Monty'[{n}]") == "IndexError" for n in NUMBERS)
print(f"     {refused} of those {len(NUMBERS)} are numbers s[n] would refuse, and the")
print("     invariant does not care about any of them. It holds because")
print("     clamping happens before the cut, on both halves, and the two")
print("     clamped answers are always the two pieces of one string.")
