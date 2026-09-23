# A recorded output is not a test

**Level:** 201 → 301 · for Python programmers, and for anyone adding a page here

> **Stub — an outline, not a lesson.** There is no runnable example behind this page yet, so nothing on it has been through [the check that backs every other claim in this library](../../CONTRIBUTING.md). The bullets below are the questions the finished page has to answer.

**One line:** This library's own gate compares a program's output with a recorded key, which proves the output *changed* and never that it is *right* — a wrong number recorded on day one passes forever — so `unittest` and `doctest` are a different kind of check: each states the expected value before the run, and fails with a diff that says which side is which.

## What the finished page has to answer

- What the golden-file check catches, drift between releases and platforms, and what it cannot: [CONTRIBUTING](../../CONTRIBUTING.md) records two prose numbers that were wrong in this library's first lessons and were caught only by reading the key against the sentence.
- `unittest.TestCase` with `assertEqual`, the diff it prints for two unequal strings or lists, `subTest` for a table of cases, and `setUp`.
- `doctest`: the `>>>` examples in a docstring run as tests, and the trailing-comment snippets on these pages are almost that shape; `python -m doctest -v`.
- Running a suite from a program without the timing line: `Ran 3 tests in 0.001s` cannot be keyed, so the example needs a `TextTestRunner` writing to `io.StringIO` and prints the counts.
- `assert` inside a test, and what [`assert` disappears under `-O`](../assert_disappears_under_dash_o/README.md) says about it.
- What pytest adds, in a sentence, and why this library cannot run it.

## See also

- [`assert` disappears under `-O`](../assert_disappears_under_dash_o/README.md)
- [CONTRIBUTING](../../CONTRIBUTING.md) and [`tools/run_examples.py`](../../tools/run_examples.py): the gate this page is about
- [`unittest` ↗](https://docs.python.org/3/library/unittest.html) and [`doctest` ↗](https://docs.python.org/3/library/doctest.html) in the library reference
- [What a test asserts ↗](https://masiarek.github.io/rust-learning-library/28_Testing/what_a_test_asserts/index.html) and [Doc tests ↗](https://masiarek.github.io/rust-learning-library/28_Testing/doc_tests/index.html) in the Rust library
