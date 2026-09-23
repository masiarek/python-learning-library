# A warning is not an exception

**Level:** 201 · for Python programmers

> **Stub — an outline, not a lesson.** There is no runnable example behind this page yet, so nothing on it has been through [the check that backs every other claim in this library](../../CONTRIBUTING.md). The bullets below are the questions the finished page has to answer.

**One line:** `warnings.warn()` prints once per location and returns, so a `DeprecationWarning` your code triggers is shown only when the triggering line is in `__main__`, is hidden when it is in an imported module, and becomes an exception only under `-W error` — which is why a deprecation nobody saw becomes a crash on the next release.

## What the finished page has to answer

- The default filter table, measured by triggering each category: `DeprecationWarning` shown in `__main__` and ignored elsewhere since 3.7 (PEP 565), `PendingDeprecationWarning`, `ImportWarning` and `ResourceWarning` ignored everywhere, `UserWarning` shown.
- Once per location: the second identical warning from the same line is not printed, and what the registry that decides that is.
- `-W error::DeprecationWarning`, `PYTHONWARNINGS`, and `warnings.simplefilter('error')` in a test run, which is the one place the library's readers should turn every warning into a failure. `unittest` already raises the default level when it runs.
- `stacklevel=2`, and why a library that warns without it points the reader at its own source instead of at the caller.
- `warnings.catch_warnings(record=True)` to test that a warning happens, and why that is the only honest way to key one.
- The compile-time warnings: `SyntaxWarning` for `assert (x, 'msg')` and for `x is 1`, which [`assert` disappears under `-O`](../../10_Testing/assert_disappears_under_dash_o/README.md) and [`is` is not `==`](../../04_Names_and_Objects/is_is_not_equals/README.md) each meet once.
- The standard library's own schedule: a deprecation lives at least two releases before removal (PEP 387), so the warning is the only notice you get.

## See also

- [`except Exception` is not `except:`](../except_exception_is_not_except/README.md): what a warning would be if it were raised
- [`warnings` ↗](https://docs.python.org/3/library/warnings.html) in the library reference, [`-W` ↗](https://docs.python.org/3/using/cmdline.html#cmdoption-W), [PEP 565 ↗](https://peps.python.org/pep-0565/) and [PEP 387 ↗](https://peps.python.org/pep-0387/)
