# A generator runs when you ask

**Level:** 201 → 301 · for Python programmers

> **Stub — an outline, not a lesson.** There is no runnable example behind this page yet, so nothing on it has been through [the check that backs every other claim in this library](../../CONTRIBUTING.md). The bullets below are the questions the finished page has to answer.

**One line:** Calling a generator function runs none of its body; each `next()` runs it as far as the next `yield` and suspends it there, so an exception inside surfaces at the consumer's `next()` rather than at the call, a `return` becomes `StopIteration`, and a `finally` runs when the generator is closed — which may be never.

## What the finished page has to answer

- Where the body's frame lives between calls, and what `gi_frame` and `gi_running` show. [An iterator is used up](../an_iterator_is_used_up/README.md) shows the laziness in one section; this page owns it.
- The traceback problem: a generator that raises on its first line raises at the consumer's `next()`, so the error points at the loop and the offending call is three frames up.
- What `return value` inside a generator does, where the value goes (`StopIteration.value`), and PEP 479: a bare `raise StopIteration` inside a generator is a `RuntimeError` since 3.7.
- The methods beyond `next()`: `send()`, `throw()`, `close()`, and `GeneratorExit`; `yield from` as delegation that forwards all three.
- `finally` and `with` inside a generator body: they run when the generator is closed, which happens at exhaustion, at an explicit `close()`, or at garbage collection, and the last of those is not a moment you can schedule.
- What laziness buys: a pipeline over a file that never holds more than one line, measured with `tracemalloc` as a dated table rather than a key, because allocation numbers differ by platform and release.
- Where the async version lives: the [concurrency library's async stream ↗](https://masiarek.github.io/concurrency-learning-library/06_Async/an_async_stream/index.html).

## See also

- [An iterator is used up](../an_iterator_is_used_up/README.md): the protocol a generator implements
- [Yield expressions ↗](https://docs.python.org/3/reference/expressions.html#yield-expressions) in the language reference, [PEP 255 ↗](https://peps.python.org/pep-0255/), [PEP 342 ↗](https://peps.python.org/pep-0342/) and [PEP 479 ↗](https://peps.python.org/pep-0479/)
- [Iterators are lazy ↗](https://masiarek.github.io/rust-learning-library/24_Iterators/iterators_are_lazy/index.html) in the Rust library, where the same laziness is a chain of adapters rather than a suspended frame
