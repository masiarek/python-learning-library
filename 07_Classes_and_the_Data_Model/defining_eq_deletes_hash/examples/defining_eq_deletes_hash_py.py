"""A class that defines __eq__ and not __hash__ becomes unhashable, on purpose."""

from dataclasses import dataclass

# Every statement below is run through exec() and every expression through
# eval(), so the label printed IS the code that ran. An exception prints its
# type name only: the message is not API.
NS = {"dataclass": dataclass}

POINT_EQ = (
    "class Point:\n"
    "    def __init__(self, x, y):\n"
    "        self.x, self.y = x, y\n"
    "    def __eq__(self, other):\n"
    "        return (self.x, self.y) == (other.x, other.y)"
)


def do(stmt):
    """Run a statement and print it; print the exception type if it raised."""
    try:
        exec(stmt, NS)
        for line in stmt.splitlines():
            print(f"     {line}")
    except Exception as exc:
        first, *rest = stmt.splitlines()
        print(f"     {first:<34} {type(exc).__name__}")
        for line in rest:
            print(f"     {line}")


def ask(expr, note=""):
    """Evaluate an expression and print it beside its value."""
    try:
        val = repr(eval(expr, NS))
    except Exception as exc:
        val = type(exc).__name__
    print(f"     {expr:<34} {val:<14} {note}".rstrip())


print("1. A CLASS WITH NEITHER METHOD: IDENTITY ANSWERS BOTH")
do("class Point:\n    def __init__(self, x, y):\n        self.x, self.y = x, y")
do("p, q = Point(1, 2), Point(1, 2)")
ask("p == q", "no __eq__, so == falls back to is")
ask("len({p, q})", "and each hashes by identity")

print("\n2. DEFINE __eq__, AND __hash__ IS GONE")
do(POINT_EQ)
do("p, q = Point(1, 2), Point(1, 2)")
ask("p == q")
ask("Point.__hash__", "defining __eq__ set __hash__ to None")
ask("hash(p)")
ask("{p, q}", "unhashable: no set member, no dict key")

print("\n3. WHY: EQUAL OBJECTS MUST HASH EQUAL")
do("class Bad(Point):\n    __hash__ = object.__hash__")
do("p, q = Bad(1, 2), Bad(1, 2)")
ask("p == q")
ask("len({p, q})", "equal, yet two members: the contract is broken")
ask("q in {p}", "a lookup for q looks where q's hash points")

print("\n4. THE FIX: HASH THE SAME FIELDS == COMPARES")
do(POINT_EQ + "\n    def __hash__(self):\n        return hash((self.x, self.y))")
do("p, q = Point(1, 2), Point(1, 2)")
ask("len({p, q})")
ask("q in {p}")
ask("{p: 'here'}[q]", "q finds p's entry: equal, and hashed alike")

print("\n5. CHANGE A KEY'S FIELDS, AND THE SET LOSES IT")
do("s = {p}")
do("p.x = 99")
ask("p in s", "the set looks where the new hash points; p is not there")
ask("p in list(s)", "a list uses ==, and finds it")
do("p.x = 1")
ask("p in s", "put the field back, and it is found again")

print("\n6. WHAT @dataclass DECIDES FOR YOU")
do("@dataclass\nclass D:\n    x: int\n    y: int")
ask("D(1, 2) == D(1, 2)")
ask("D.__hash__", "eq=True and not frozen: unhashable, on purpose")
do("@dataclass(frozen=True)\nclass F:\n    x: int\n    y: int")
ask("len({F(1, 2), F(1, 2)})", "frozen: the fields cannot change, so hashing them is safe")
do("@dataclass(eq=False)\nclass I:\n    x: int")
ask("I(1) == I(1)", "eq=False keeps identity for both")
ask("I.__hash__ is object.__hash__")

print("\n7. == IS TWO QUESTIONS, AND NotImplemented PASSES THE FIRST")
do("class Metres:\n    def __init__(self, v):\n        self.v = v\n    def __eq__(self, other):\n        if not isinstance(other, Metres):\n            return NotImplemented\n        return self.v == other.v")
ask("Metres(1) == Metres(1)")
ask("Metres(1) != Metres(1)", "__ne__ is derived from __eq__")
ask("Metres(1) == 1", "NotImplemented from both sides: falls back to is")
ask("1 == Metres(1)", "int declines first, then Metres is asked")
