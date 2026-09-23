# `if x` calls a method

**Level:** 201 · for Python programmers

> **Stub — an outline, not a lesson.** There is no runnable example behind this page yet, so nothing on it has been through [the check that backs every other claim in this library](../../CONTRIBUTING.md). The bullets below are the questions the finished page has to answer.

**One line:** `if x:` calls `x.__bool__()`, falls back to `x.__len__()`, and takes the answer to be `True` when the class defines neither — so every empty container is false, an object of a class you wrote is true until you say otherwise, and `if result:` on a function that returns `0` or `[]` on success is a bug that never raises.

## What the finished page has to answer

- The rule, measured on the built-ins: `0`, `0.0`, `''`, `b''`, `[]`, `{}`, `set()`, `range(0)`, `None` false; everything else true, including `'0'`, `' '` and `[0]`.
- A class with neither method is always true, so a `Metres(0)` object passes `if m:`; a class with `__len__` is false when empty; `__bool__` must return a `bool`, and returning anything else is `TypeError`.
- `if x is not None` against `if x`, and the function that returns `0` on success.
- `and` and `or` return an operand, not a `bool`, so `x or default` replaces a legitimate `0` and `''`, and `all([])` is `True`.
- `datetime.time(0)` was false before 3.5, dated, as the one case the core team reversed.
- Where the rule reaches: `while x`, `not x`, `filter(None, xs)`, and a comprehension's `if`.

## See also

- [`is` is not `==`](../../04_Names_and_Objects/is_is_not_equals/README.md): why `None` is tested with `is`
- [Truth value testing ↗](https://docs.python.org/3/library/stdtypes.html#truth-value-testing) in the library reference, and [`object.__bool__` ↗](https://docs.python.org/3/reference/datamodel.html#object.__bool__)
- [`if` expressions ↗](https://masiarek.github.io/rust-learning-library/25_Control_Flow/if_expressions/index.html) in the Rust library, where `if` takes a `bool` and nothing else
