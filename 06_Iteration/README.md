# 06_Iteration — lazy, and used up

**Level:** 201 → 301 · for Python programmers, especially ones coming from ABAP or C

A `for` loop in Python does not count; it asks. It calls `iter()` on whatever it was given and then `next()` until something raises `StopIteration`. Most of what surprises people about iteration follows from what that protocol leaves out: an iterator has no length, no position you can reset, no mark that says it is one and not a list, and no complaint when it is finished. It yields nothing, and the loop runs zero times. A generator, `zip`, `map` and an open file all obey it. The pages here are the places where that quietness costs something.

| # | Lesson | The question it answers | Status |
|---|---|---|---|
| 1 | [An iterator is used up](an_iterator_is_used_up/README.md) | Why did the second loop over my `zip` run zero times — and why did `4 in evens` move the position? | written |
| 2 | [A generator runs when you ask](a_generator_runs_when_asked/README.md) | Why did nothing happen when I called my generator — and why did its exception appear at the loop instead of the call? | stub |
| 3 | [`zip` stops at the shortest](zip_stops_at_the_shortest/README.md) | Why did pairing a hundred names with ninety-nine scores lose a row in silence — and which row? | stub |
| 4 | [`groupby` groups runs, not keys](groupby_groups_runs/README.md) | Why did `groupby` give me the same key three times — and why was my group empty by the time I read it? | stub |
| 5 | [Mutating what you iterate](mutating_what_you_iterate/README.md) | Why did removing from a list inside its loop skip every other match, when the same thing on a dict raised? | stub |

## Where this sits relative to the other libraries

The [Rust library's iterators chapter ↗](https://masiarek.github.io/rust-learning-library/24_Iterators/index.html) is the same protocol with ownership on top: consuming an iterator moves it, so "used up" is a compile error there and a silent zero here. The [concurrency library ↗](https://masiarek.github.io/concurrency-learning-library/) owns the asynchronous version, starting from [an async stream ↗](https://masiarek.github.io/concurrency-learning-library/06_Async/an_async_stream/index.html). Chapter 1's [Opening a file](../01_Text_and_Bytes/opening_a_file/README.md) already treats the file as an iterator over lines. ABAP has no iterator type; its internal tables are walked from the top every time, and the object that behaves like this chapter's iterators is a database cursor, which page 1 says in its bridge.
