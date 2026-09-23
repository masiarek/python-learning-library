"""An iterator is a position in a walk, not the collection: once at the end, it stays there."""

import io
import itertools

# Every statement below is run through exec() and every expression through
# eval(), so the label printed IS the code that ran. An exception prints its
# type name only: the message is not API.
NS = {"io": io, "itertools": itertools}


def do(stmt):
    """Run a statement and print it; print the exception type if it raised."""
    try:
        exec(stmt, NS)
        for line in stmt.splitlines():
            print(f"     {line}")
    except Exception as exc:
        first, *rest = stmt.splitlines()
        print(f"     {first:<38} {type(exc).__name__}")
        for line in rest:
            print(f"     {line}")


def ask(expr, note=""):
    """Evaluate an expression and print it beside its value."""
    try:
        val = repr(eval(expr, NS))
    except Exception as exc:
        val = type(exc).__name__
    print(f"     {expr:<38} {val:<26} {note}".rstrip())


print("1. A LIST CAN BE WALKED TWICE; ITS ITERATOR CANNOT")
do("nums = [1, 2, 3]")
ask("sum(nums), sum(nums)", "a list starts every walk at the beginning")
do("it = iter(nums)")
ask("sum(it), sum(it)", "the second sum found the iterator at its end")
do("it = iter(nums)")
ask("sum(it)")
ask("max(it)", "not a complaint about iterators: max of nothing")
ask("len(iter(nums))", "no length: the only way to count is to consume")

print("\n2. WHAT for DOES: iter() ONCE, THEN next() UNTIL StopIteration")
do("it = iter([10, 20])")
ask("next(it)")
ask("next(it)")
ask("next(it)", "the signal that the walk is over")
ask("next(it, 'done')", "a default instead of the exception")
ask("iter(it) is it", "an iterator's iter() is itself, so for cannot rewind it")
ask("iter(nums) is iter(nums)", "a list hands out a fresh iterator every time")

print("\n3. WHICH BUILT-INS HAND YOU AN ITERATOR")
do("pairs = zip('ab', [1, 2])")
ask("list(pairs)")
ask("list(pairs)", "zip is an iterator: used up")
do("squares = map(lambda n: n * n, [1, 2, 3])")
ask("list(squares), list(squares)", "so is map, and filter, reversed, enumerate")
do("evens = (n for n in range(10) if n % 2 == 0)")
ask("4 in evens", "in walked the generator as far as 4")
ask("list(evens)", "and left it there")
do("r = range(3)")
ask("list(r), list(r)", "range is a sequence, not an iterator")
do("d = {'a': 1}")
do("items = d.items()")
ask("list(items), list(items)", "a dict view is a view, not an iterator")

print("\n4. HALF-CONSUMED BY A SHORT-CIRCUIT")
do("it = iter([1, 2, 3, 4])")
ask("any(n > 1 for n in it)", "any() stopped at 2")
ask("list(it)", "the rest is still there, for whoever asks next")

print("\n5. A GENERATOR RUNS ONLY WHEN ASKED, AND ONLY ONCE")
do("def gen():\n    print('     (gen: started)')\n    yield 1\n    print('     (gen: resumed)')\n    yield 2\n    print('     (gen: finished)')")
do("g = gen()")
ask("next(g)", "nothing ran until this call")
ask("next(g)")
ask("next(g)", "the body ran to its end, then signalled")
ask("list(g)", "spent; gen() again is the only way back")

print("\n6. A FILE IS AN ITERATOR TOO")
do("f = io.StringIO('a\\nb\\n')")
ask("len(f.readlines())")
ask("len(f.readlines())", "at the end, like any iterator")
do("f.seek(0)")
ask("len(f.readlines())", "a file has seek(); an iterator in general does not")

print("\n7. WALKING TWICE ON PURPOSE")
do("it = iter([1, 2, 3])")
do("a, b = itertools.tee(it)")
ask("list(a), list(b)", "tee buffers what one side has seen and the other has not")
ask("list(it)", "and the original is spent either way")
do("saved = list(iter([1, 2, 3]))")
ask("sum(saved), sum(saved)", "or keep a list, which is what tee is doing quietly")
