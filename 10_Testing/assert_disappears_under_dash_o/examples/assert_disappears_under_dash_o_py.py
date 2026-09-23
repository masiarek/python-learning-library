"""assert is a debugging aid the interpreter can be told to delete; -O tells it to."""

import os
import subprocess
import sys


def run(code, *flags, env_extra=None, isolated=True):
    """Run `code` in a child interpreter; return (exit status, stdout, stderr).

    The child gets -I unless told otherwise, so nothing on this machine leaks
    into the answer key -- and -I is itself one of the page's rows, because
    isolated mode ignores every PYTHON* variable, PYTHONOPTIMIZE included.
    """
    env = dict(os.environ)
    if env_extra:
        env.update(env_extra)
    cmd = [sys.executable, *(["-I"] if isolated else []), *flags, "-c", code]
    proc = subprocess.run(cmd, capture_output=True, text=True, env=env)
    return proc.returncode, proc.stdout.strip(), proc.stderr


def row(label, result, note=""):
    status, out, err = result
    kinds = [k for k in ("AssertionError", "ValueError", "SyntaxWarning") if k in err]
    stderr = ", ".join(kinds) if kinds else "-"
    print(f"     {label:<22} exit {status}   stdout {out!r:<28} stderr {stderr:<16} {note}".rstrip())


print("1. THE SAME LINE, WITH AND WITHOUT -O")
code = "assert 1 == 2, 'math is broken'\nprint('reached the end')"
row("python3", run(code), "the assert fired and the program died")
row("python3 -O", run(code, "-O"), "the assert is not there")
row("PYTHONOPTIMIZE=1", run(code, env_extra={"PYTHONOPTIMIZE": "1"}, isolated=False), "the environment can switch it on for you")
row("PYTHONOPTIMIZE=1 -I", run(code, env_extra={"PYTHONOPTIMIZE": "1"}), "unless -I: isolated mode ignores PYTHON* variables")

print("\n2. WHAT -O REMOVES: assert, AND EVERY `if __debug__:` BLOCK")
code = "print(__debug__)\nif __debug__:\n    print('debug block')"
row("python3", run(code))
row("python3 -O", run(code, "-O"))

print("\n3. -OO ALSO REMOVES DOCSTRINGS")
code = "def f():\n    'the doc'\nprint(f.__doc__)"
row("python3 -O", run(code, "-O"), "still there")
row("python3 -OO", run(code, "-OO"), "gone: help() and doctest see None")

print("\n4. THE ASSERT THAT IS ALWAYS TRUE")
code = "assert (1 == 2, 'oops')\nprint('passed')"
row("python3", run(code), "a non-empty tuple is true; the compiler warns")

print("\n5. AN assert IS NOT VALIDATION")
by_assert = "def withdraw(amount):\n    assert amount > 0, 'amount must be positive'\n    return amount\nprint(withdraw(-5))"
by_raise = "def withdraw(amount):\n    if amount <= 0:\n        raise ValueError('amount must be positive')\n    return amount\nprint(withdraw(-5))"
row("assert, python3", run(by_assert))
row("assert, python3 -O", run(by_assert, "-O"), "the check went with the flag: -5 withdrawn")
row("raise, python3", run(by_raise))
row("raise, python3 -O", run(by_raise, "-O"), "an if and a raise are not optional")

print("\n6. unittest's assertEqual IS A METHOD, NOT THE STATEMENT")
code = "import unittest\ntry:\n    unittest.TestCase().assertEqual(1, 2)\nexcept AssertionError:\n    print('assertEqual still raises')"
row("python3 -O", run(code, "-O"), "so a test suite survives -O; its bare asserts do not")
