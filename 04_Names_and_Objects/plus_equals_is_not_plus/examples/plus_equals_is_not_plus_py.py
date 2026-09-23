"""a += b asks a to change itself, and only falls back to a = a + b."""

# Every statement below is run through exec() and every expression through
# eval(), so the label printed IS the code that ran. An exception prints its
# type name only: the message is not API.
NS = {}


def do(stmt):
    """Run a statement and print it; print the exception type if it raised."""
    try:
        exec(stmt, NS)
        print(f"     {stmt}")
    except Exception as exc:
        print(f"     {stmt:<32} {type(exc).__name__}")


def ask(expr, note=""):
    """Evaluate an expression and print it beside its value."""
    try:
        val = repr(eval(expr, NS))
    except Exception as exc:
        val = type(exc).__name__
    print(f"     {expr:<32} {val:<16} {note}".rstrip())


print("1. ON A LIST, += CHANGES THE OBJECT")
do("a = [1]")
do("b = a")
do("a += [2]")
ask("b", "b saw it: += grew the one list in place")
ask("a is b")
do("a = a + [3]")
ask("b", "+ built a new list and bound a to it; b kept the old one")
ask("a is b")

print("\n2. ON A TUPLE, A STRING OR AN INT, += REBINDS")
do("t = (1,)")
do("u = t")
do("t += (2,)")
ask("u", "a tuple cannot change, so t was rebound")
ask("t is u")
do("s = 'ab'")
do("r = s")
do("s += 'c'")
ask("r")
do("n = 1")
do("m = n")
do("n += 1")
ask("m")

print("\n3. THE METHOD THAT DECIDES")
ask("hasattr(list, '__iadd__')", "list can change itself, so += calls this")
ask("hasattr(tuple, '__iadd__')", "no __iadd__: += falls back to __add__, then assigns")
ask("hasattr(str, '__iadd__')")
ask("hasattr(int, '__iadd__')")
ask("hasattr(bytearray, '__iadd__')", "the same split as list against tuple")
ask("hasattr(bytes, '__iadd__')")
do("a = [1]")
ask("a.__iadd__([2]) is a", "the in-place method returns the object it changed")

print("\n4. THE TUPLE TRAP: IT RAISES, AND IT ALSO HAPPENED")
do("t = ([], 'x')")
do("t[0] += [1]")
ask("t", "the list grew, then the store back into the tuple failed")
do("t2 = ([], 'x')")
do("t2[0] = t2[0] + [1]")
ask("t2", "with +, nothing had happened when the store failed")
do("t3 = ([], 'x')")
do("t3[0].extend([1])")
ask("t3", "no store into the tuple, so no error")

print("\n5. THROUGH AN INSTANCE, += ON A CLASS ATTRIBUTE")
do("class Counter: count = 0")
do("c = Counter()")
do("c.count += 1")
ask("Counter.count", "the read found the class attribute")
ask("vars(c)", "the store made an instance attribute")
do("class Log: lines = []")
do("lg = Log()")
do("lg.lines += ['a']")
ask("Log.lines", "a list: the read found the class's list and += grew it")
ask("vars(lg)", "and the store still made an instance attribute")
ask("lg.lines is Log.lines", "which names the same, now shared, list")

print("\n6. THE SAME SPLIT FOR *=")
do("a = [0]")
do("b = a")
do("a *= 2")
ask("b", "in place")
do("s = 'ab'")
do("r = s")
do("s *= 2")
ask("r", "rebound")
