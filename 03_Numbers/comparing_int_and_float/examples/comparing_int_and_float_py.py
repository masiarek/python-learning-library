"""Python compares the numbers, not the types -- and the comparison is exact."""

import ctypes
import math
import struct
from decimal import Decimal
from fractions import Fraction

# Every row below is a string that is eval'd, so the label printed IS the code
# that ran. An exception prints its type name only: the message is not API.
NAMES = {
    "math": math,
    "ctypes": ctypes,
    "struct": struct,
    "Decimal": Decimal,
    "Fraction": Fraction,
    "n": 2**53 + 1,
}


def result(expr):
    try:
        return repr(eval(expr, NAMES))
    except Exception as exc:  # the type is the answer
        kind = type(exc)
        if kind.__module__ == "builtins":
            return kind.__name__
        return f"{kind.__module__}.{kind.__name__}"


def rows(table):
    got = [result(expr) for expr, _ in table]
    w1 = max(len(expr) for expr, _ in table)
    w2 = max(len(g) for g in got)
    for (expr, note), g in zip(table, got):
        line = f"     {expr:<{w1}}   {g:<{w2}}   {note}"
        print(line.rstrip())


print("1. MIXED NUMBERS COMPARE; A NUMBER AND A STRING DO NOT")
rows(
    [
        ("1 == 1.0", ""),
        ("7 < 7.5", ""),
        ("True == 1", "bool is a subclass of int"),
        ("True + True", ""),
        ("1 == '1'", "== across unrelated types is just False"),
        ("1 < '2'", "< across unrelated types refuses"),
    ],
)
print()
print("     Rust will not compile i32 < u16: it refuses to compare two")
print("     integer TYPES. Python has one int type, so that question cannot")
print("     be written here. The refusal it does have is between kinds of")
print("     value: ordering a number against a string.")

print("\n2. THE COMPARISON IS EXACT")
print(f"     n = 2**53 + 1 = {NAMES['n']}")
print()
rows(
    [
        ("float(n)", "the nearest double is one less"),
        ("n == float(n)", "compared exactly: they differ by 1"),
        ("float(n) == 2**53", "and that double IS 2**53"),
        ("float(n) == float(2**53)", "convert both first, and two ints collide"),
        ("n.__eq__(float(n))", "int's == does not know float"),
        ("float(n).__eq__(n)", "float's == does the exact work"),
    ],
)
print()
print("     Where the doubles run out, some ints have no double of their own:")
print(f"     {'n':<11} {'float(n)':<22} n == float(n)")
for k in range(-1, 4):
    m = 2**53 + k
    label = "2**53" if k == 0 else f"2**53 {'+' if k > 0 else '-'} {abs(k)}"
    print(f"     {label:<11} {float(m)!r:<22} {m == float(m)}")

print("\n3. PAST THE LARGEST DOUBLE, COMPARISON STILL WORKS")
rows(
    [
        ("10**400 > 1e308", ""),
        ("10**400 < math.inf", ""),
        ("float(10**400)", "the conversion cannot happen"),
    ],
)
print()
print("     The comparison never converted the int, so it has an answer")
print("     where the conversion has none.")

print("\n4. ARITHMETIC CONVERTS -- ONLY COMPARISON IS EXACT")
rows(
    [
        ("n + 0.0", "the int became a float first"),
        ("n + 0.0 == n", "adding zero changed the number"),
        ("10**400 + 0.0", "and past the largest double, it cannot"),
    ],
)

print("\n5. DECIMAL AND FRACTION FOLLOW THE SAME RULE")
top, bottom = (0.1).as_integer_ratio()
print(f"     The literal 0.1 holds {top} / {bottom}")
print("     -- (0.1).as_integer_ratio() -- which is not one tenth.")
print()
rows(
    [
        ("Decimal('0.1') == 0.1", "a tenth is not that double"),
        ("Decimal('0.1') < 0.1", "the double is a little MORE than a tenth"),
        ("Fraction(1, 10) == 0.1", ""),
        ("Fraction(0.1) == 0.1", "built from the double: the same number"),
        ("Decimal(0.1) == 0.1", "same again, in decimal"),
        ("Decimal('0.1') + 0.1", "compares with a float, refuses to add one"),
        ("Fraction(1, 10) + 0.1", "adds, and the answer is a float"),
    ],
)

print("\n6. EQUAL NUMBERS ARE ONE DICT KEY")
rows(
    [
        ("len({1, 1.0, True, Fraction(1), Decimal(1)})", "five types, one number"),
        ("{1: 'int', 1.0: 'float', True: 'bool'}", "first key kept, last value"),
        ("hash(0.5) == hash(Fraction(1, 2))", "equal, so they must hash equal"),
        ("{n: 'found'}.get(float(n))", "float(n) is 2**53, not n"),
        ("{2**53: 'found'}.get(float(n))", ""),
    ],
)
print()
print("     A dict needs equal keys to hash equal, so hash() is defined on")
print("     the numeric value, whatever type is holding it.")

print("\n7. A WIDTH HAS TO BE ASKED FOR")
print("     Rust's 300_i32 as i8 is 44: the top bits are dropped. A Python")
print("     int has no width to drop them from, so the width is yours to name:")
print()
rows(
    [
        ("(300 + 128) % 256 - 128", "arithmetic: wrap into -128..127"),
        ("ctypes.c_int8(300).value", "a C type truncates, as the cast does"),
        ("(300).to_bytes(1, 'big', signed=True)", "refuses, like i8::try_from"),
        ("struct.pack('b', 300)", "refuses too"),
        ("-1 < 1", "no unsigned type for -1 to become"),
    ],
)
