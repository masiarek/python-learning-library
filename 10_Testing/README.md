# 10_Testing — what a passing run proves

**Level:** 201 → 301 · for Python programmers, and for anyone adding a page here

A green run proves what the check compared, and nothing more. This library's own gate compares a program's output with a recorded key, which catches drift and cannot catch a key that was wrong on the day it was recorded, and [CONTRIBUTING](../CONTRIBUTING.md) says so. The pages here are three ways a check passes while the code is wrong: an `assert` the interpreter was told to delete, a recorded output nobody compared with the claim beside it, and a patch applied to a name that the code under test never reads.

| # | Lesson | The question it answers | Status |
|---|---|---|---|
| 1 | [`assert` disappears under `-O`](assert_disappears_under_dash_o/README.md) | Why did the withdrawal of `-5` go through in production when the `assert` stopped it on my machine? | written |
| 2 | [A recorded output is not a test](a_recorded_output_is_not_a_test/README.md) | What does this library's own gate prove, what can it not, and what do `unittest` and `doctest` add? | stub |
| 3 | [`patch` where it is looked up](patch_where_it_is_looked_up/README.md) | Why did patching `time.time` change nothing in the module I was testing? | stub |

## Where this sits relative to the other libraries

The [Rust library's testing chapter ↗](https://masiarek.github.io/rust-learning-library/28_Testing/index.html) is the comparison for all three pages: `assert!` against `debug_assert!` for page 1, doc tests for page 2, and a trait as the seam where page 3 reaches for `patch`. The gate this chapter measures itself against is [`tools/run_examples.py`](../tools/run_examples.py), described in [CONTRIBUTING](../CONTRIBUTING.md).
