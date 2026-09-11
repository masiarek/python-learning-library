# Standard in, standard out, and pipes

**Level:** 201 · for Python programmers

> **Stub — an outline, not a lesson.** There is no runnable example behind this page yet, so nothing on it has been through [the check that backs every other claim in this library](../../CONTRIBUTING.md). The bullets below are the questions the finished page has to answer.

**One line:** `sys.stdout` is a file Python opened for you before your code ran, and a pipe changes two things about it that a terminal does not: your output leaves in blocks instead of lines, and when the reader quits early — `| head` — the next write to reach the pipe raises `BrokenPipeError`.

## Which library answers which question

This outline used to open with encoding questions — why an emoji prints in a terminal and raises under `cron`, why `sys.stdout.encoding` differs down a pipe — and the encodings library had already measured them, with the opposite answer: on macOS and Linux a pipe changes `sys.stdout`'s buffering and never its encoding. So the split [Opening a file](../opening_a_file/README.md#which-library-answers-which-question) settled on 2026-09-08 was applied here on 2026-09-10: the sibling owns the codec, this page owns the call.

| The question | Where it is answered |
|---|---|
| Why does piping `print()` into `head` raise `BrokenPipeError`, and what is the standard way to handle it? | here, once this page is written |
| How do you write bytes to stdout on purpose, when the output is not text? | here, once this page is written |
| When does the output actually leave the process, and why does stderr overtake stdout into a pipe? | here, [Opening a file, section 4](../opening_a_file/README.md#who-decides-when-the-output-leaves) |
| **Which encoding does `sys.stdout` use, and does a pipe change it?** | the sibling, [A pipe is not a terminal ↗](https://masiarek.github.io/encodings-learning-library/06_Terminal/pipe_is_not_a_terminal/index.html) — on macOS and Linux, no: the environment decides (`PYTHONIOENCODING`, then UTF-8 Mode, then the locale), not the pipe |
| **When does `print()` raise `UnicodeEncodeError`?** | the sibling, [A pipe is not a terminal ↗](https://masiarek.github.io/encodings-learning-library/06_Terminal/pipe_is_not_a_terminal/index.html#in-python) — when stdout's codec cannot hold the character, on both roads or neither |
| **`PYTHONIOENCODING` or `sys.stdout.reconfigure(encoding=...)`, and which to reach for?** | the sibling's half, and not yet written there — [A pipe is not a terminal ↗](https://masiarek.github.io/encodings-learning-library/06_Terminal/pipe_is_not_a_terminal/index.html) measures where `PYTHONIOENCODING` sits in the order, not `reconfigure()` |

The `cron` version of the old question is folklore on every Python this library supports. Measured 2026-09-10 on the `python:3.11-slim` to `python:3.14-slim` images and on macOS 3.14.7: a job started with an empty environment, which is what `cron` gives it, gets UTF-8 Mode and prints an emoji. What raises is a stdout codec that cannot hold the character — UTF-8 Mode switched off under a C locale, or a legacy locale such as `en_US.ISO8859-1`.

## What the finished page has to answer

- Why `print()` to a closed pipe raises `BrokenPipeError`, and the standard way to handle `| head`. Measured 2026-09-10, not yet an example: the write inside `print()` raises first, and then the interpreter's own final flush of stdout fails again (`Exception ignored while flushing sys.stdout`, exit status 120) — so catching the first one is not the whole fix.
- `sys.stdout.buffer` — writing bytes deliberately, for when the output is not text.

## See also

- [Opening a file](../opening_a_file/README.md) — section 4: when your output leaves, and why stderr overtakes stdout into a pipe
- [Encode and decode](../encode_and_decode/README.md)
- [A pipe is not a terminal ↗](https://masiarek.github.io/encodings-learning-library/06_Terminal/pipe_is_not_a_terminal/index.html) — the encoding half, measured: a pipe moves `line_buffering` and nothing else
- [Locale and `LC_CTYPE` ↗](https://masiarek.github.io/encodings-learning-library/06_Terminal/locale_and_lc_ctype/index.html) — where `sys.stdout`'s encoding really comes from
- [`printf` writes bytes ↗](https://masiarek.github.io/encodings-learning-library/06_Terminal/printf_writes_bytes/index.html)
