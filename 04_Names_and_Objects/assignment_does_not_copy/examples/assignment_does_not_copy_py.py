"""Assignment binds a name to an object. It never copies the object."""

import copy

# Every statement below is run through exec() and every expression through
# eval(), so the label printed IS the code that ran. An exception prints its
# type name only: the message is not API.
NS = {"copy": copy}


def do(stmt):
    """Run a statement and print it; print the exception type if it raised."""
    try:
        exec(stmt, NS)
        print(f"     {stmt}")
    except Exception as exc:
        print(f"     {stmt:<30} {type(exc).__name__}")


def ask(expr, note=""):
    """Evaluate an expression and print it beside its value."""
    try:
        val = repr(eval(expr, NS))
    except Exception as exc:
        val = type(exc).__name__
    print(f"     {expr:<30} {val:<36} {note}".rstrip())


print("1. TWO NAMES, ONE LIST")
do("a = [1, 2]")
do("b = a")
do("b.append(3)")
ask("a", "the change made through b is visible through a")
ask("a is b", "because there is one list, with two names")

print("\n2. REBINDING IS NOT MUTATING")
do("b = b + [4]")
ask("a", "unchanged: + built a new list")
ask("b", "and b now names that new list")
ask("a is b")
do("n = 1")
do("m = n")
do("m += 1")
ask("n", "an int cannot change, so two names never trap you")

print("\n3. THE GRID THAT IS ONE ROW, THREE TIMES")
do("grid = [[0] * 3] * 3")
do("grid[0][0] = 1")
ask("grid", "every row changed")
ask("grid[0] is grid[1]", "* repeated the reference, not the row")
do("rows = [[0] * 3 for _ in range(3)]")
do("rows[0][0] = 1")
ask("rows", "the comprehension ran [0] * 3 three times")
ask("rows[0] is rows[1]")

print("\n4. A COPY IS ONE LEVEL DEEP")
do("a = [[1], [2]]")
do("b = a[:]")
ask("a is b", "the outer list is new")
ask("a[0] is b[0]", "the inner lists are the same ones")
do("b[0].append(9)")
ask("a", "so a changed through the copy")
print()
print("     Every way of copying a list is shallow, except one:")
for expr in ["a[:]", "list(a)", "a.copy()", "copy.copy(a)", "sorted(a)", "(a * 2)", "[*a]"]:
    ask(f"{expr}[0] is a[0]")
ask("copy.deepcopy(a)[0] is a[0]", "deepcopy is the one that copies the inside")
print()
do("d = {'k': [1]}")
do("e = dict(d)")
do("e['k'].append(2)")
ask("d", "dict(d) and d.copy() are shallow too")

print("\n5. A CALL IS AN ASSIGNMENT")
do("def grow(lst): lst.append(0)")
do("def regrow(lst): lst = lst + [0]")
do("data = [1]")
do("grow(data)")
ask("data", "the parameter named the caller's list, and mutated it")
do("regrow(data)")
ask("data", "the parameter was rebound; the caller's name was not")

print("\n6. AN IMMUTABLE CONTAINER, WITH MUTABLE CONTENTS")
do("t = ([], 'x')")
do("t[0].append(1)")
ask("t", "the tuple did not change: it holds the same list, which did")
do("t[1] = 'y'")
ask("hash(t)", "and a tuple holding a list cannot be a dict key")
