# `logging` is a tree

**Level:** 201 → 301 · for Python programmers

> **Stub — an outline, not a lesson.** There is no runnable example behind this page yet, so nothing on it has been through [the check that backs every other claim in this library](../../CONTRIBUTING.md). The bullets below are the questions the finished page has to answer.

**One line:** Loggers are nodes in a tree named by dots, and a record travels from the logger it was made on up to the root and out through every handler on the way — so `basicConfig()` configures the root once and does nothing the second time, a handler added to both `app` and `app.db` prints each line twice, and a library that never configured anything still gets its warnings printed by the root's last-resort handler.

## What the finished page has to answer

- `getLogger('app.db').parent is getLogger('app')`, propagation, and the difference between a logger's level and a handler's level, measured with handlers that write to `io.StringIO` so the key holds the text.
- `basicConfig()` as a no-op once the root has a handler, `force=True`, and the trap of a module-level `logging.warning()` call configuring the root behind your back.
- The double line: one handler on the parent and one on the child, and `propagate = False`.
- `lastResort`: a `WARNING` from an unconfigured program still reaches stderr, and an `INFO` does not.
- `NullHandler` for a library, `getLogger(__name__)` for the tree to follow the packages, and `%(name)s` in the format to see it.
- `log.info('%s', x)` against `log.info(f'{x}')`: the first formats only if the record is emitted.
- `logging.exception()` inside an `except` block, and what it adds that `error()` does not, which is [The traceback is on the object](../../08_Errors/the_traceback_is_on_the_object/README.md).

## See also

- [Standard in, standard out, and pipes](../../01_Text_and_Bytes/stdin_stdout_and_pipes/README.md): where stderr goes
- [`logging` ↗](https://docs.python.org/3/library/logging.html) in the library reference and the [logging HOWTO ↗](https://docs.python.org/3/howto/logging.html)
- [The Rust library's observability chapter ↗](https://masiarek.github.io/rust-learning-library/21_Observability/index.html), where the tree is a `tracing` subscriber
