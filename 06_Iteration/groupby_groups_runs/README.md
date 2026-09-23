# `groupby` groups runs, not keys

**Level:** 201 · for Python programmers, especially ones coming from SQL or ABAP

> **Stub — an outline, not a lesson.** There is no runnable example behind this page yet, so nothing on it has been through [the check that backs every other claim in this library](../../CONTRIBUTING.md). The bullets below are the questions the finished page has to answer.

**One line:** `itertools.groupby` starts a new group every time the key *changes*, so unsorted input hands you the same key several times, and the group it gives you is a window onto the same iterator as the outer loop — advance the outer loop and the group you were holding is empty.

## What the finished page has to answer

- The SQL intuition and why it is wrong here: `GROUP BY` collects a key from anywhere in the table, `groupby` behaves like `uniq -c` on a stream, and an unsorted input gives the key `'a'`, then `'b'`, then `'a'` again. Measured.
- Sort first, with the *same* key function, and why the stability of `sorted` makes the order inside each group predictable.
- The shared iterator: `[(k, list(g)) for k, g in groupby(data)]` works, and `list(groupby(data))` gives every group empty, because by the time you read a group the outer iterator has moved past it. Measured, with [An iterator is used up](../an_iterator_is_used_up/README.md) as the reason.
- When you want whole-input grouping instead: `collections.defaultdict(list)` and `collections.Counter`, which read everything once and keep it.
- `key=None`, and grouping on `str.lower` or `operator.itemgetter` as the two usual keys.

## See also

- [An iterator is used up](../an_iterator_is_used_up/README.md): why the group vanishes
- [Sorting is not comparing](../../01_Text_and_Bytes/sorting_is_not_comparing/README.md): the key function, and what sorting strings actually orders by
- [`itertools.groupby` ↗](https://docs.python.org/3/library/itertools.html#itertools.groupby) in the Python docs, whose first paragraph says this and is not read
