# `finally` can overwrite the return

**Level:** 301 · for Python programmers

> **Stub — an outline, not a lesson.** There is no runnable example behind this page yet, so nothing on it has been through [the check that backs every other claim in this library](../../CONTRIBUTING.md). The bullets below are the questions the finished page has to answer.

**One line:** A `return`, `break` or `continue` inside `finally` runs after the `try` block's own `return` and after any exception in flight, and replaces both — so a `return` in `finally` silently discards the exception, 3.14 warns about the shape at compile time, and a `finally` that raises buries the original exception behind the new one.

## What the finished page has to answer

- `try: return 1` / `finally: return 2` returns `2`, measured; and the same shape with an exception in the `try`, where the exception vanishes without a trace.
- PEP 765: since 3.14 the compiler emits a `SyntaxWarning` for `return`, `break` and `continue` in a `finally` block. The example has to compile that function from a string under `warnings.catch_warnings`, because a warning on stderr is not part of the key and a page should not depend on which release printed it.
- A `finally` that raises: the new exception carries the old one as `__context__`, which [`except Exception` is not `except:`](../except_exception_is_not_except/README.md) section 6 explains, and the traceback shows both.
- What `finally` is for, which is releasing, not deciding: closing, unlocking, restoring. `with` as the spelling that cannot return, and `contextlib.ExitStack` for several at once.
- The generator's `finally`, which runs when the generator is closed and possibly never, which [A generator runs when you ask](../../06_Iteration/a_generator_runs_when_asked/README.md) owns.

## See also

- [`except Exception` is not `except:`](../except_exception_is_not_except/README.md): section 7, `else` and `finally` on the normal path
- [The `try` statement ↗](https://docs.python.org/3/reference/compound_stmts.html#the-try-statement) in the language reference, [PEP 765 ↗](https://peps.python.org/pep-0765/), and [`contextlib` ↗](https://docs.python.org/3/library/contextlib.html)
- [`Drop` and RAII ↗](https://masiarek.github.io/rust-learning-library/12_Traits/drop_and_raii/index.html) in the Rust library: the `finally` that cannot return anything
