# `zip` stops at the shortest

**Level:** 201 · for Python programmers

> **Stub — an outline, not a lesson.** There is no runnable example behind this page yet, so nothing on it has been through [the check that backs every other claim in this library](../../CONTRIBUTING.md). The bullets below are the questions the finished page has to answer.

**One line:** `zip` ends when any of its inputs ends and raises nothing, so pairing a hundred names with ninety-nine scores drops one row in silence; `strict=True` raises instead, `itertools.zip_longest` pads, and when an input is an iterator the dropped element has already been consumed from it.

## What the finished page has to answer

- The default, measured on two lists of different lengths, and `dict(zip(keys, values))` coming back one entry short with no error.
- `zip(*args, strict=True)`, since 3.10, and the `ValueError` it raises, named by type on the page.
- `itertools.zip_longest(fillvalue=…)`, and why a fill value of `None` is ambiguous when `None` is data.
- Which element is lost when one input is an iterator: `zip` pulls from its inputs left to right, so it has already taken the next item from the longer one before it learns that the shorter one ended, and that item is gone. Measured with `list(it)` afterwards, the way [An iterator is used up](../an_iterator_is_used_up/README.md) does.
- `zip(*rows)` as a transpose, and what a ragged row does to it.
- `map(f, a, b)` follows the same rule, and `enumerate` cannot be short because it makes its own counter.

## See also

- [An iterator is used up](../an_iterator_is_used_up/README.md): why `zip` itself lists only once
- [`zip` ↗](https://docs.python.org/3/library/functions.html#zip) and [`itertools.zip_longest` ↗](https://docs.python.org/3/library/itertools.html#itertools.zip_longest) in the Python docs, and [PEP 618 ↗](https://peps.python.org/pep-0618/) for `strict`
- [`zip` and `enumerate` ↗](https://masiarek.github.io/rust-learning-library/24_Iterators/zip_and_enumerate/index.html) in the Rust library, where `zip` also stops at the shorter and there is no `strict`
