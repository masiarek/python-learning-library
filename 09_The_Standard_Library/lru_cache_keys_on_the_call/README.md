# `lru_cache` keys on the call

**Level:** 301 · for Python programmers

> **Stub — an outline, not a lesson.** There is no runnable example behind this page yet, so nothing on it has been through [the check that backs every other claim in this library](../../CONTRIBUTING.md). The bullets below are the questions the finished page has to answer.

**One line:** `functools.lru_cache` stores a result under a key built from the call as written — positional and keyword arguments, by hash and `==` — so `f(1)` and `f(x=1)` are two entries, `f(1)` and `f(1.0)` are one, an unhashable argument is a `TypeError` at call time, a method's cache keeps every `self` alive for as long as the cache lives, and the same result object is handed back to every caller.

## What the finished page has to answer

- `cache_info()` after a sequence of calls, showing hits, misses and size; `cache_clear()`; `maxsize=None`, which is `functools.cache`; `typed=True`.
- Keyword order: `f(a=1, b=2)` and `f(b=2, a=1)` are two entries, measured.
- The hashing rule, which is [Defining `__eq__` deletes `__hash__`](../../07_Classes_and_the_Data_Model/defining_eq_deletes_hash/README.md): a list argument raises, and equal numbers of different types share an entry.
- The shared result: a cached function that returns a list returns the *same* list to every caller, and one caller's `append` is everyone's, which is [Assignment does not copy](../../04_Names_and_Objects/assignment_does_not_copy/README.md) at a distance.
- Methods: the cache is on the class, keyed by `self`, so instances never die while it is populated; `functools.cached_property` as the per-instance alternative.
- `fib` under `lru_cache` against `fib` with a `memo={}` default, which [A default is computed once](../../05_Functions/a_default_is_computed_once/README.md) shows, and the recursion limit the recursive version meets first.
- What the cache does across threads, which the [concurrency library ↗](https://masiarek.github.io/concurrency-learning-library/) owns.

## See also

- [Defining `__eq__` deletes `__hash__`](../../07_Classes_and_the_Data_Model/defining_eq_deletes_hash/README.md), [Assignment does not copy](../../04_Names_and_Objects/assignment_does_not_copy/README.md) and [A default is computed once](../../05_Functions/a_default_is_computed_once/README.md)
- [`functools.lru_cache` ↗](https://docs.python.org/3/library/functools.html#functools.lru_cache) and [`cached_property` ↗](https://docs.python.org/3/library/functools.html#functools.cached_property) in the library reference
