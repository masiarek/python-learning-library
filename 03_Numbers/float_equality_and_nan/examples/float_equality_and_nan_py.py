"""0.1 + 0.2 is not 0.3, a tolerance has to be relative, and NaN is not equal to itself."""

import math
import struct
import sys
from decimal import Decimal
from fractions import Fraction

nan = float("nan")

# Every row below is a string that is eval'd, so the label printed IS the code
# that ran. An exception prints its type name only: the message is not API.
NAMES = {"math": math, "struct": struct, "sys": sys, "nan": nan, "a": 1000.1 + 1000.2}


def result(expr):
    try:
        return repr(eval(expr, NAMES))
    except Exception as exc:  # the type is the answer
        return type(exc).__name__


def rows(table):
    got = [result(expr) for expr, _ in table]
    w1 = max(len(expr) for expr, _ in table)
    w2 = max(len(g) for g in got)
    for (expr, note), g in zip(table, got):
        line = f"     {expr:<{w1}}   {g:<{w2}}   {note}"
        print(line.rstrip())


def f32(x):
    """Round a double to the nearest 32-bit float, and hand it back as a double."""
    return struct.unpack(">f", struct.pack(">f", x))[0]


def bits32(x):
    return struct.pack(">f", x).hex()


def bits64(x):
    return struct.pack(">d", x).hex()


print("1. 0.1 + 0.2 IS NOT 0.3")
rows(
    [
        ("0.1 + 0.2", ""),
        ("0.1 + 0.2 == 0.3", ""),
        ("0.5 + 0.25 == 0.75", "halves and quarters are exact in binary"),
    ]
)
print()
print(f"     {'':<10} {'float.hex()':<23} 64 bits")
for label, value in (("0.1 + 0.2", 0.1 + 0.2), ("0.3", 0.3)):
    print(f"     {label:<10} {value.hex():<23} {bits64(value)}")
print()
print("     One step apart in the last hex digit. The exact values show why:")
for label, value in (("0.1", 0.1), ("0.2", 0.2), ("0.3", 0.3)):
    print(f"     {label}  is stored as {Decimal(value)}")
print("     0.1 and 0.2 are each stored a little high; 0.3 a little low.")
print(f"     math.nextafter(0.3, math.inf) == 0.1 + 0.2   {math.nextafter(0.3, math.inf) == 0.1 + 0.2}")

print("\n2. THE SAME SUMS IN 32 BITS")
print("     Python has no 32-bit float. struct.pack('>f', x) rounds a double")
print("     to the nearest one, which is enough to replay the arithmetic.")
print()
print(f"     {'question':<16}   {'left, 32 bits':<13}   {'right, 32 bits':<14}   {'in 32 bits':<10}   in 64 bits")
for x, y, want in ((0.1, 0.2, 0.3), (0.1, 0.6, 0.7)):
    fx, fy = f32(x), f32(y)
    exact = Fraction(fx) + Fraction(fy) == Fraction(fx + fy)
    assert exact  # so one rounding of fx + fy IS the 32-bit addition
    total, fwant = f32(fx + fy), f32(want)
    question = f"{x} + {y} == {want}"
    print(
        f"     {question:<16}   {bits32(total):<13}   {bits32(fwant):<14}   "
        f"{str(total == fwant):<10}   {x + y == want}"
    )
print()
print("     The first question is True in 32 bits and False in 64; the second")
print("     is the other way round. Neither width is the accurate one: each")
print("     rounds, and each gets lucky on different numbers. (For both pairs")
print("     the double sum of the two 32-bit values is exact -- the program")
print("     asserts it with Fraction -- so rounding that sum once to 32 bits")
print("     is exactly what 32-bit addition does.)")

print("\n3. A TOLERANCE HAS TO BE RELATIVE")
d64 = 0.2 - (0.1 + 0.1)
d32 = f32(0.2) - f32(f32(0.1) + f32(0.1))
print(f"     0.2 - (0.1 + 0.1)   is {d64!r} in 64 bits, and {d32!r} in 32")
print("     A difference of exactly zero passes any tolerance, and == too.")
print("     To test a tolerance, the two sides have to differ:")
print()
rows(
    [
        ("sys.float_info.epsilon", "the gap between 1.0 and the next double"),
        ("math.ulp(2000.3)", "the gap near 2000"),
        ("math.ulp(2000.3) / sys.float_info.epsilon", ""),
    ]
)
print()
print("     a = 1000.1 + 1000.2")
rows(
    [
        ("a", ""),
        ("a == 2000.3", ""),
        ("a - 2000.3 == math.ulp(2000.3)", "one gap apart: the next double up"),
        ("abs(a - 2000.3) <= sys.float_info.epsilon", "no two doubles near 2000 are that close"),
        ("math.isclose(a, 2000.3)", "rel_tol=1e-09 scales with the numbers"),
        ("math.isclose(1e-20, 0.0)", "abs_tol defaults to 0.0"),
        ("math.isclose(1e-20, 0.0, abs_tol=1e-12)", "near zero, say what close means"),
    ]
)

print("\n4. EQUALITY IS NOT THE BITS")
zeros_equal = 0.0 == -0.0
print(f"     0.0 == -0.0   {zeros_equal}   and the bits are {bits64(0.0)} and {bits64(-0.0)}")
print("     nan = float('nan')")
print()
rows(
    [
        ("nan == nan", "every comparison with NaN is False..."),
        ("nan != nan", "...except !=, which is its negation"),
        ("nan < 1.0 or nan >= 1.0", "not less, not greater-or-equal"),
        ("math.isnan(nan)", "the test that works"),
    ]
)
print()
print("     Containers ask 'is it the same object?' before they ask ==:")
rows(
    [
        ("[nan] == [nan]", "one object, twice: equal"),
        ("nan in [nan]", ""),
        ("{nan: 'x'}.get(nan)", ""),
        ("[float('nan')] == [float('nan')]", "two objects: == decides, and says no"),
        ("{float('nan'): 'x'}.get(float('nan'))", ""),
        ("math.nan is math.nan", "a module constant is one object..."),
        ("[math.nan] == [math.nan]", "...so this list compares equal"),
    ]
)

print("\n5. WITH A NaN IN IT, THE ORDER OF THE ARGUMENTS DECIDES")
rows(
    [
        ("max(nan, 1.0)", "asks 1.0 > nan: False, so nan stays"),
        ("max(1.0, nan)", "asks nan > 1.0: False, so 1.0 stays"),
        ("min(nan, 1.0)", ""),
        ("min(1.0, nan)", ""),
        ("sorted([3.0, nan, 1.0, 2.0])", "not sorted, and no error"),
    ]
)

print("\n6. SOMETIMES PYTHON RAISES WHERE IEEE 754 GIVES A VALUE")
rows(
    [
        ("math.sqrt(-42.0)", "IEEE 754 says NaN"),
        ("1.0 / 0.0", "IEEE 754 says inf"),
        ("1.0 % 0.0", "C's fmod says NaN"),
        ("math.log(0.0)", "IEEE 754 says -inf"),
        ("1e308 ** 2", "C's pow says inf"),
    ]
)
print()
print("     ...and sometimes it hands the value back:")
rows(
    [
        ("1e308 * 1e308", "the same number as 1e308 ** 2, and no error"),
        ("1e308 * 10", ""),
        ("math.inf - math.inf", ""),
        ("math.inf * 0", ""),
        ("math.isfinite(1e308 * 10)", "the check to make before trusting a result"),
    ]
)
print()
z = (-42.0) ** 0.5
neg = -42.0 ** 0.5
print(f"     (-42.0) ** 0.5    a {type(z).__name__}, imaginary part {z.imag:.6f}")
print(f"     -42.0 ** 0.5      {neg:.6f}   ** binds tighter than the minus: -(42.0 ** 0.5)")
