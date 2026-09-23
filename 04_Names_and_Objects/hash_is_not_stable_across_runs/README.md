# `hash()` is not stable across runs

**Level:** 301 · for Python programmers

> **Stub — an outline, not a lesson.** There is no runnable example behind this page yet, so nothing on it has been through [the check that backs every other claim in this library](../../CONTRIBUTING.md). The bullets below are the questions the finished page has to answer.

**One line:** A `str` or `bytes` object hashes differently in every process unless `PYTHONHASHSEED` pins the seed, so a set of strings iterates in a different order on every run, while `hash(1)` is `1`, `hash(-1)` is `-2`, and `hash(1) == hash(1.0) == hash(True)` — the numbers chapter's rule with a security fix on top.

## What the finished page has to answer

- Why the seed exists: hash flooding, the 2011 attack that made a web server compute for minutes on one crafted request, and PEP 456's answer, a keyed SipHash with a key chosen at start-up. Which types it covers, `str`, `bytes` and `datetime`, and which it does not.
- What it changes and what it leaves alone. A `dict` iterates in insertion order, so it is unaffected; a `set` iterates in table order, so `set('abc')` prints differently from one run to the next. The example has to spawn child interpreters with `PYTHONHASHSEED=0` and `=1` to show the two orders side by side, because a single process cannot see its own seed change.
- Why `hash(-1)` is `-2`: the C function returns `-1` to signal an error, so the value is displaced by one. Why `hash(2**61)` is `1`: integers hash modulo `2**61 - 1`. Why `hash(1) == hash(1.0) == hash(True) == hash(Fraction(1))`, which [Comparing an `int` with a `float`](../../03_Numbers/comparing_int_and_float/README.md) needs for a dict to work.
- Where it bites: a doctest or an answer key that prints a set of strings, a JSON file written from a set, a "stable" ordering that held on one machine. This library's own runner would catch the first case, and the page should say how.
- The contract with `__eq__`, which the classes chapter will own: equal objects must hash equal, and an object whose hash changes while it is in a set is lost.

## See also

- [Comparing an `int` with a `float`](../../03_Numbers/comparing_int_and_float/README.md): section 6, equal numbers are one dict key
- [`hash()` ↗](https://docs.python.org/3/library/functions.html#hash) and [`PYTHONHASHSEED` ↗](https://docs.python.org/3/using/cmdline.html#envvar-PYTHONHASHSEED) in the Python docs, and [PEP 456 ↗](https://peps.python.org/pep-0456/)
