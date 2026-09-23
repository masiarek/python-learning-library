"""except Exception leaves Ctrl-C and sys.exit() alone; a bare except swallows them."""

import sys

# Every statement below is run through exec() and every expression through
# eval(), so the label printed IS the code that ran. A statement that lets an
# exception escape prints its type name beside its first line: the message is
# not API. BaseException is caught here on purpose -- this page is about the
# exceptions that `except Exception` does not catch.
NS = {"sys": sys}


def do(stmt):
    """Run a statement and print it; print the escaping exception's type, if any."""
    lines = stmt.splitlines()
    try:
        exec(stmt, NS)
        for line in lines:
            print(f"     {line}")
    except BaseException as exc:
        print(f"     {lines[0]:<48} escaped: {type(exc).__name__}")
        for line in lines[1:]:
            print(f"     {line}")


def ask(expr, note=""):
    """Evaluate an expression and print it beside its value."""
    try:
        val = repr(eval(expr, NS))
    except BaseException as exc:
        val = type(exc).__name__
    print(f"     {expr:<48} {val:<32} {note}".rstrip())


print("1. THE TREE HAS A ROOT ABOVE Exception")
ask("[c.__name__ for c in ValueError.__mro__]")
ask("[c.__name__ for c in KeyboardInterrupt.__mro__]", "no Exception on the way up")
ask("issubclass(KeyboardInterrupt, Exception)")
ask("issubclass(SystemExit, Exception)", "sys.exit() raises this one")
ask("issubclass(GeneratorExit, Exception)", "and a closed generator gets this one")

print("\n2. except Exception LETS Ctrl-C THROUGH; A BARE except DOES NOT")
do("try:\n    raise KeyboardInterrupt\nexcept Exception:\n    outcome = 'caught'")
do("try:\n    raise KeyboardInterrupt\nexcept:\n    outcome = 'a bare except caught it'")
ask("outcome")
do("try:\n    raise KeyboardInterrupt\nexcept BaseException:\n    outcome = 'so does BaseException, by name'")
ask("outcome")

print("\n3. sys.exit() IS AN EXCEPTION, AND A BARE except CANCELS THE EXIT")
do("try:\n    sys.exit(3)\nexcept SystemExit as e:\n    code = e.code")
ask("code", "sys.exit() raised; nothing exited")
do("try:\n    sys.exit(3)\nexcept:\n    swallowed = True")
ask("swallowed", "the program that meant to stop is still running")

print("\n4. THE FIRST MATCHING CLAUSE WINS")
do("try:\n    int('x')\nexcept Exception:\n    handler = 'Exception'\nexcept ValueError:\n    handler = 'ValueError'")
ask("handler", "the specific clause below it can never run")
ask("issubclass(ValueError, Exception)", "because this is true")

print("\n5. THE as-NAME IS DELETED WHEN THE BLOCK ENDS")
do("try:\n    1 / 0\nexcept ZeroDivisionError as err:\n    kind = type(err).__name__")
ask("kind")
ask("err", "unbound: the block deleted it on the way out")
do("try:\n    1 / 0\nexcept ZeroDivisionError as err:\n    saved = err")
ask("type(saved).__name__", "keep it by binding another name")

print("\n6. AN EXCEPTION IS AN OBJECT, AND raise from IS A LINK")
do("try:\n    try:\n        {}['k']\n    except KeyError as e:\n        raise ValueError('bad config') from e\nexcept ValueError as v:\n    chain = (type(v).__name__, type(v.__cause__).__name__)")
ask("chain", "from e: the cause is on the new exception")
do("try:\n    try:\n        {}['k']\n    except KeyError:\n        int('x')\nexcept ValueError as v:\n    ctx = (type(v.__context__).__name__, v.__cause__)")
ask("ctx", "raised while handling: linked as __context__, not __cause__")
do("try:\n    try:\n        {}['k']\n    except KeyError:\n        raise ValueError('bad config') from None\nexcept ValueError as v:\n    hidden = (v.__context__ is not None, v.__suppress_context__)")
ask("hidden", "from None keeps the context and hides it from the traceback")

print("\n7. else RUNS WHEN NOTHING WAS RAISED; finally RUNS REGARDLESS")
do("def probe(text):\n    log = []\n    try:\n        log.append(int(text))\n    except ValueError:\n        log.append('except')\n    else:\n        log.append('else')\n    finally:\n        log.append('finally')\n    return log")
ask("probe('1')")
ask("probe('x')")

print("\n8. A GROUP IS CAUGHT IN PIECES, AND NOT BY A PLAIN except")
do("try:\n    raise ExceptionGroup('two', [ValueError('a'), TypeError('b')])\nexcept* ValueError as eg:\n    got_v = [type(e).__name__ for e in eg.exceptions]\nexcept* TypeError as eg:\n    got_t = [type(e).__name__ for e in eg.exceptions]")
ask("got_v, got_t", "each except* clause got its slice of the group")
do("try:\n    raise ExceptionGroup('one', [ValueError('a')])\nexcept ValueError:\n    pass")
ask("issubclass(ExceptionGroup, ValueError)", "a group is not any of its members")
