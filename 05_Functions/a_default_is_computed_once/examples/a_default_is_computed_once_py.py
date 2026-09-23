"""A default value is evaluated once, when def runs, and shared by every call."""

import itertools
from dataclasses import dataclass, field

# Every statement below is run through exec() and every expression through
# eval(), so the label printed IS the code that ran. An exception prints its
# type name only: the message is not API.
NS = {"dataclass": dataclass, "field": field, "count": itertools.count(1)}


def do(stmt):
    """Run a statement and print it; print the exception type if it raised."""
    try:
        exec(stmt, NS)
        for line in stmt.splitlines():
            print(f"     {line}")
    except Exception as exc:
        first, *rest = stmt.splitlines()
        print(f"     {first:<40} {type(exc).__name__}")
        for line in rest:
            print(f"     {line}")


def ask(expr, note=""):
    """Evaluate an expression and print it beside its value."""
    try:
        val = repr(eval(expr, NS))
    except Exception as exc:
        val = type(exc).__name__
    print(f"     {expr:<40} {val:<14} {note}".rstrip())


print("1. THE DEFAULT IS ONE OBJECT, MADE WHEN def RAN")
do("def add(item, acc=[]): acc.append(item); return acc")
ask("add(1)")
ask("add(2)", "the same list, still holding the first call's item")
ask("add(3)")
ask("add.__defaults__", "where the one list lives")
ask("add(4, [])", "a list you pass is yours; only the default is shared")
ask("add.__defaults__", "and the default did not change")

print("\n2. WHEN THE DEFAULT IS EVALUATED")
do("def stamp(n=next(count)): return n")
ask("stamp()")
ask("stamp()", "evaluated once, at def -- not once per call")
ask("next(count)", "the counter moved once, when def ran")

print("\n3. THE IDIOM: None MEANS 'MAKE A NEW ONE'")
do("def add2(item, acc=None):\n    if acc is None:\n        acc = []\n    acc.append(item)\n    return acc")
ask("add2(1)")
ask("add2(2)", "a fresh list per call")

print("\n4. A DEFAULT THAT CANNOT CHANGE IS SAFE")
do("def tally(item, seen=()): return seen + (item,)")
ask("tally(1)")
ask("tally(2)", "+ built a new tuple; the default is still ()")
ask("tally.__defaults__")

print("\n5. A DATACLASS REFUSES THE TRAP, AND NAMES THE FIX")
do("@dataclass\nclass Bag:\n    items: list = []")
do("@dataclass\nclass Bag:\n    items: list = field(default_factory=list)")
do("b1, b2 = Bag(), Bag()")
ask("b1.items is b2.items", "default_factory ran once per instance")

print("\n6. THE SAME FACT, USED ON PURPOSE")
do("fs = [lambda: i for i in range(3)]")
ask("[f() for f in fs]", "each lambda reads i when called, and i ended at 2")
do("fs = [lambda i=i: i for i in range(3)]")
ask("[f() for f in fs]", "a default is computed when the lambda is made")
do("def fib(n, memo={}):\n    if n < 2:\n        return n\n    if n not in memo:\n        memo[n] = fib(n - 1) + fib(n - 2)\n    return memo[n]")
ask("fib(30)")
ask("len(fib.__defaults__[0])", "the default is the cache, and it outlives the call")
