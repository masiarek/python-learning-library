# `defaultdict` creates on read

**Level:** 201 · for Python programmers

> **Stub — an outline, not a lesson.** There is no runnable example behind this page yet, so nothing on it has been through [the check that backs every other claim in this library](../../CONTRIBUTING.md). The bullets below are the questions the finished page has to answer.

**One line:** A `defaultdict` calls its factory on every *missing key you read*, so `if d[k]:` inserts `k`, `len(d)` grows during a loop that only looked, and `d.get(k)` does not trigger it at all — which is `__missing__`, and it makes `Counter`'s zero and `dict.setdefault`'s explicit spelling the two things to compare it with.

## What the finished page has to answer

- `d[k]` against `d.get(k)` against `k in d` on a missing key, measured with `len(d)` after each.
- `__missing__` as the hook, and a `dict` subclass with its own.
- `Counter[k]` returns `0` *without* inserting, which is the opposite decision made by the same module.
- `dict.setdefault(k, [])` as the one-line spelling, and why its default is evaluated on every call where `defaultdict(list)` calls the factory only on a miss.
- The grouping idiom, `defaultdict(list)` fed by a loop, against [`groupby`](../../06_Iteration/groupby_groups_runs/README.md), and the counting idiom against `Counter`.
- `dict.fromkeys(keys, [])` handing every key the one list, which [Assignment does not copy](../../04_Names_and_Objects/assignment_does_not_copy/README.md) measures.
- The neighbours: `OrderedDict` equality is order-sensitive where `dict` equality is not, and `popitem()` is last-in first-out.

## See also

- [Assignment does not copy](../../04_Names_and_Objects/assignment_does_not_copy/README.md) and [`groupby` groups runs, not keys](../../06_Iteration/groupby_groups_runs/README.md)
- [`collections.defaultdict` ↗](https://docs.python.org/3/library/collections.html#collections.defaultdict) in the library reference, and [`object.__missing__` ↗](https://docs.python.org/3/reference/datamodel.html#object.__missing__)
- [The `HashMap` ↗](https://masiarek.github.io/rust-learning-library/26_Collections/the_hashmap/index.html) in the Rust library, where `entry(k).or_insert(…)` is the explicit spelling of the same idea
