# `is` is not `==`

**Level:** 201 · for Python programmers

> **Stub — an outline, not a lesson.** There is no runnable example behind this page yet, so nothing on it has been through [the check that backs every other claim in this library](../../CONTRIBUTING.md). The bullets below are the questions the finished page has to answer.

**One line:** `==` asks two objects whether they are equal, through a method either of them may define; `is` asks whether they are one object, and nothing can redefine it — so `x is None` is the right test, two equal lists are never `is`, and whether `int('257') is int('257')` is a fact about CPython's cache rather than about the language.

## What the finished page has to answer

- What `a == b` runs: `type(a).__eq__(a, b)`, then the reflected `type(b).__eq__(b, a)` when the first returns `NotImplemented`, then the identity fallback, which is why `1 == '1'` is `False` rather than an error while `1 < '1'` raises. [Comparing an `int` with a `float`](../../03_Numbers/comparing_int_and_float/README.md) already shows the `NotImplemented` step for numbers.
- What `a is b` runs: nothing you can override. [Defining `__eq__` deletes `__hash__`](../../07_Classes_and_the_Data_Model/defining_eq_deletes_hash/README.md) measures the `NotImplemented` step for a class of your own. Two names, one object. `id()` as the number behind it, and why printing an `id()` on a page would tie the answer key to one run.
- The singletons: `None`, `True`, `False`, `NotImplemented`, `Ellipsis`. Why `x is None` and `x == None` can differ for a class with its own `__eq__`, and why linters insist on `is`.
- The implementation detail people mistake for a rule: CPython keeps one object for each small integer and interns some strings, so `int('256') is int('256')` is `True` and `int('257') is int('257')` is `False` on the same machine. Measured and dated on the page, not keyed, because it is not a promise of the language.
- The warning: since 3.8, `x is 1` and `x is 'a'` raise a `SyntaxWarning`, because they ask a question whose answer depends on the interpreter.
- Where identity hides inside `==`: `in`, `list.index` and `list.count` test `is` before `==`, which is why `nan in [nan]` is `True` while `nan == nan` is `False`. [Float equality and NaN](../../03_Numbers/float_equality_and_nan/README.md) measures that case.

## See also

- [Assignment does not copy](../assignment_does_not_copy/README.md): where two names for one object come from
- [Comparison has a mode](../../01_Text_and_Bytes/comparison_has_a_mode/README.md): the four ways to compare two strings, none of which is `is`
- [Float equality and NaN](../../03_Numbers/float_equality_and_nan/README.md): identity first, inside a container
- [Comparison traits ↗](https://masiarek.github.io/rust-learning-library/12_Traits/comparison_traits/index.html) in the Rust library, where equality is a trait and identity is `std::ptr::eq`
- [Value comparisons ↗](https://docs.python.org/3/reference/expressions.html#value-comparisons) and [`is` ↗](https://docs.python.org/3/reference/expressions.html#is-not) in the language reference
