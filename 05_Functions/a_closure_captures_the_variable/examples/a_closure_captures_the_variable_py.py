"""A closure holds the variable, not the value it had when the closure was made."""

import functools

# Every statement below is run through exec() and every expression through
# eval(), so the label printed IS the code that ran. An exception prints its
# type name only: the message is not API.
NS = {"functools": functools}


def do(stmt):
    """Run a statement and print it; print the exception type if it raised."""
    try:
        exec(stmt, NS)
        for line in stmt.splitlines():
            print(f"     {line}")
    except Exception as exc:
        first, *rest = stmt.splitlines()
        print(f"     {first:<44} {type(exc).__name__}")
        for line in rest:
            print(f"     {line}")


def ask(expr, note=""):
    """Evaluate an expression and print it beside its value."""
    try:
        val = repr(eval(expr, NS))
    except Exception as exc:
        val = type(exc).__name__
    print(f"     {expr:<44} {val:<18} {note}".rstrip())


print("1. THREE LAMBDAS, ONE VARIABLE")
do("fs = [lambda: i for i in range(3)]")
ask("[f() for f in fs]", "all three read i when called, and i ended at 2")

print("\n2. THE LOOKUP HAPPENS WHEN THE FUNCTION RUNS")
do("x = 1")
do("def f(): return x")
do("x = 2")
ask("f()", "f reads x now, not when def ran")
do("del x")
ask("f()", "and if x is gone by then, it fails now")

print("\n3. WHAT A CLOSURE HOLDS: A CELL, WHICH CAN BE SHARED")
do("def counter():\n    n = 0\n    def inc():\n        nonlocal n\n        n += 1\n        return n\n    def get():\n        return n\n    return inc, get")
do("inc, get = counter()")
ask("inc(), inc(), get()", "get sees what inc did: one cell")
ask("inc.__closure__[0] is get.__closure__[0]")
ask("get.__closure__[0].cell_contents", "the cell holds the current value")

print("\n4. THREE WAYS TO CAPTURE THE VALUE INSTEAD")
do("fs = [lambda i=i: i for i in range(3)]")
ask("[f() for f in fs]", "a default is computed once, when the lambda is made")
do("fs = [functools.partial(lambda i: i, i) for i in range(3)]")
ask("[f() for f in fs]", "partial stores the argument now")
do("def keep(i): return lambda: i")
do("fs = [keep(i) for i in range(3)]")
ask("[f() for f in fs]", "each call to keep is a new scope, so a new cell")

print("\n5. THE LOOP VARIABLE OUTLIVES THE LOOP")
do("for k in range(3): pass")
ask("k", "a for loop makes no scope of its own")
do("squares = [k * k for k in range(10)]")
ask("k", "a comprehension does: its k never leaked")

print("\n6. AND ASSIGNING TO THE NAME INSIDE MAKES IT LOCAL")
do("total = 0")
do("def bump(): total += 1")
ask("bump()", "the += made total local to bump, so the read finds nothing")
do("def bump():\n    global total\n    total += 1")
do("bump()")
ask("total")
