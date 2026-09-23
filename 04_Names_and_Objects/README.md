# 04_Names_and_Objects — a name is a binding, not a box

**Level:** 201 → 301 · for Python programmers, especially ones coming from C, Rust or ABAP

Every assignment in Python points a name at an object and copies nothing. C copies the bytes, ABAP copies the value and Rust moves the ownership; Python does none of those, and almost every surprise in this chapter is that one rule meeting an object that can change: a second name that sees the change, a `+=` that changes the object for everyone who holds it, a "copy" that still shares its insides, and a comparison that answers a different question from the one you asked.

This is the first of the advanced chapters, and it goes first because the others stand on it. [A default argument is one object shared by every call](../05_Functions/a_default_is_computed_once/README.md), [a class attribute is one object shared by every instance](../07_Classes_and_the_Data_Model/a_class_attribute_is_shared/README.md), and [an iterator is one object that is used up](../06_Iteration/an_iterator_is_used_up/README.md).

| # | Lesson | The question it answers | Status |
|---|---|---|---|
| 1 | [Assignment does not copy](assignment_does_not_copy/README.md) | Why did a change made through `b` show up in `a` — and why is `[[0] * 3] * 3` one row three times? | written |
| 2 | [`+=` is not `+`](plus_equals_is_not_plus/README.md) | Why did `a += [2]` change a list I never touched — and why did `t[0] += [1]` both raise and happen? | written |
| 3 | [`is` is not `==`](is_is_not_equals/README.md) | Which of the two comparisons did I mean — and why is `int('257') is int('257')` a question about CPython, not Python? | stub |
| 4 | [`hash()` is not stable across runs](hash_is_not_stable_across_runs/README.md) | Why does my set of strings come out in a different order on every run — and why is `hash(-1)` `-2`? | stub |

## Where this sits relative to the other libraries

The [Rust library's ownership chapter ↗](https://masiarek.github.io/rust-learning-library/18_Ownership/index.html) is the model this chapter is measured against: [A name is not a place ↗](https://masiarek.github.io/rust-learning-library/18_Ownership/a_name_is_not_a_place/index.html) is the half the two languages share, and [Copy or move ↗](https://masiarek.github.io/rust-learning-library/18_Ownership/copy_or_move/index.html) is the fork Python does not have. The [concurrency library ↗](https://masiarek.github.io/concurrency-learning-library/) owns what happens when the two names are on two threads, starting with [the lost update ↗](https://masiarek.github.io/concurrency-learning-library/02_Shared_State/the_lost_update/index.html). Chapter 1's [`bytearray` is the mutable one](../01_Text_and_Bytes/bytearray_is_mutable/README.md) is this chapter's rule applied to the binary types, and it already carries a kata about `+=`.
