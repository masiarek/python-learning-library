# Standard in, standard out, and pipes

**Level:** 201 · for Python programmers

> **Stub — an outline, not a lesson.** There is no runnable example behind this page yet, so nothing on it has been through [the check that backs every other claim in this library](../../CONTRIBUTING.md). The bullets below are the questions the finished page has to answer.

**One line:** Your program's output encoding is not a property of your program — it is negotiated with whatever is on the other end of the pipe, and it changes when you add `| head`.

- Why does printing an emoji work in the terminal and raise `UnicodeEncodeError` in a cron job or a Docker build?
- `sys.stdout.encoding` — where it comes from, and why it is different when stdout is a pipe rather than a TTY.
- `PYTHONIOENCODING`, `sys.stdout.reconfigure(encoding=...)`, and which one to reach for.
- `sys.stdout.buffer` — writing bytes deliberately, for when the output is not text.
- Why `print()` to a closed pipe raises `BrokenPipeError`, and the standard way to handle `| head`.

## See also

- [Encode and decode](../encode_and_decode/README.md)
- [`printf` writes bytes ↗](https://masiarek.github.io/encodings-learning-library/06_Terminal/printf_writes_bytes/index.html) ↗
