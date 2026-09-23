# 08_Errors — an exception is an object, and `except` is a filter

**Level:** 201 → 301 · for Python programmers, especially ones coming from C, Rust or ABAP

Python's error handling is exceptions all the way down. A `for` loop ends on one, `sys.exit()` raises one, Ctrl-C arrives as one, and a generator is closed by one. That makes `except` a filter over a class tree rather than a list of error codes, and everything on these pages is about what the filter lets through, what it drops, and what it does to the object it caught: the name it binds and then deletes, the links one exception keeps to another, the `finally` that can replace the answer, the warning that is not raised at all, and the traceback the object carries with it.

| # | Lesson | The question it answers | Status |
|---|---|---|---|
| 1 | [`except Exception` is not `except:`](except_exception_is_not_except/README.md) | Why does my worker loop ignore Ctrl-C — and why did `sys.exit()` not exit? | written |
| 2 | [`finally` can overwrite the return](finally_can_overwrite_the_return/README.md) | Where did my exception go — and why does 3.14 warn about a `return` in `finally`? | stub |
| 3 | [A warning is not an exception](a_warning_is_not_an_exception/README.md) | Why did I never see the deprecation that just became a crash? | stub |
| 4 | [The traceback is on the object](the_traceback_is_on_the_object/README.md) | Why does `raise e` add a line that a bare `raise` does not — and which block of a chained traceback is the cause? | stub |

## Where this sits relative to the other libraries

The [Rust library's errors chapter ↗](https://masiarek.github.io/rust-learning-library/02_Errors/index.html) is the design that has no filter to get wrong: a `Result` is a value the compiler makes you look at, and [Keep going or stop ↗](https://masiarek.github.io/rust-learning-library/02_Errors/keep_going_or_stop/index.html) is the decision page 1's hierarchy encodes. Chapter 2's [Ctrl-C is a signal](../02_Projects_and_Environments/ctrl_c_is_a_signal/README.md) is where `KeyboardInterrupt` comes from, and the [Linux library's signals chapter ↗](https://masiarek.github.io/linux-learning-library/11_Signals/index.html) is where the signal comes from. Exception groups arrive from code that runs several things at once, which the [concurrency library ↗](https://masiarek.github.io/concurrency-learning-library/) owns, starting with [a failure nobody is waiting for ↗](https://masiarek.github.io/concurrency-learning-library/01_Threads/a_failure_nobody_is_waiting_for/index.html). ABAP's `CX_ROOT` tree, `PREVIOUS` and `CLEANUP` are compared on page 1.
