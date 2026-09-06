# Opening a file

**Level:** 101 → 201 · for Python programmers

> **Stub — an outline, not a lesson.** There is no runnable example behind this page yet, so nothing on it has been through [the check that backs every other claim in this library](../../CONTRIBUTING.md). The bullets below are the questions the finished page has to answer.

**One line:** `open(path)` picks an encoding for you, the choice depends on the machine, and naming `encoding=` explicitly is the single highest-value habit in this chapter.

- What does `open(path)` actually use when you say nothing? (`locale.getencoding()`, and why the answer differs between macOS, Ubuntu and Windows.)
- Why is `encoding="utf-8"` the right default to type every time, and what is `PYTHONUTF8=1` / UTF-8 mode?
- What does `newline=` do, and why does the default rewrite `\r\n` on the way in?
- When is `"rb"` the correct answer instead of an encoding — and how does that change `len()`?
- [PEP 686 ↗](https://peps.python.org/pep-0686/) makes UTF-8 mode the default. What breaks, and when?
- `EncodingWarning` and `-X warn_default_encoding`: how to find every unnamed `open()` in a codebase.

## See also

- [Encode and decode](../encode_and_decode/README.md)
- [Locale and `LC_CTYPE` ↗](https://masiarek.github.io/encodings-learning-library/06_Terminal/locale_and_lc_ctype/index.html)
