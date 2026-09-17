"""Kata: eight one-liners about float equality, and the one that depends on the order."""

import math

LINES = [
    ("0.5 + 0.25 == 0.75", "halves and quarters are exact in binary"),
    ("0.1 * 3 == 0.3", "0.30000000000000004 is the next double up"),
    ("math.isclose(0.1 * 3, 0.3)", "one gap apart, far inside rel_tol=1e-09"),
    ("math.isclose(1e-20, 0.0)", "relative to zero is zero; abs_tol is 0.0"),
    ("float('nan') in [float('nan')]", "two objects, so == decides, and says no"),
    ("min(float('nan'), 0.0)", "asks 0.0 < nan: False, so nan stays"),
    ("2.0 ** 1024", "** checks for overflow; * does not"),
    ("-0.0 == 0.0", "different bits, equal numbers"),
]


def result(expr):
    try:
        return repr(eval(expr, {"math": math}))
    except Exception as exc:  # the type is the answer
        return type(exc).__name__


got = [result(expr) for expr, _ in LINES]
w1 = max(len(expr) for expr, _ in LINES)
w2 = max(len(g) for g in got)
w3 = max(len(note) for _, note in LINES)
print(f"     {'expression':<{w1}}   {'result':<{w2}}   note")
print("     " + "-" * (w1 + w2 + w3 + 6))
for (expr, note), g in zip(LINES, got):
    print(f"     {expr:<{w1}}   {g:<{w2}}   {note}")

swapped = repr(min(0.0, float("nan")))
print()
print("     THE ONE THAT DEPENDS ON THE ORDER")
print(f"     Line 6. Swapped, min(0.0, float('nan')) is {swapped}. min() only")
print("     replaces its answer when a later argument compares less, and")
print("     every comparison against a NaN is False, so whichever argument")
print("     comes first is kept. A minimum should not depend on the order")
print("     it was asked in, and with a NaN in it, it does.")
print()
print("     THE TWO WHERE == WAS THE RIGHT TEST")
print("     Lines 1 and 8. 0.5, 0.25, 0.75 and both zeros are stored exactly,")
print("     so == compares the numbers you wrote. Line 2 is the same shape")
print("     as line 1 and is False, because 0.1 and 0.3 are not stored")
print("     exactly -- which is the whole reason line 3 exists.")
