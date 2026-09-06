# Filenames are not text

**Level:** 301 · deep dive

> **Stub — an outline, not a lesson.** There is no runnable example behind this page yet, so nothing on it has been through [the check that backs every other claim in this library](../../CONTRIBUTING.md). The bullets below are the questions the finished page has to answer.

**One line:** A POSIX filename is a bag of bytes with two forbidden values, which is not the same thing as a string — and `surrogateescape` is the trick that lets Python pretend otherwise without losing data.

- What is actually legal in a POSIX filename? (Anything but `/` and `NUL` — including bytes that are not valid UTF-8 in any encoding.)
- How does `os.listdir()` return a name that cannot be decoded, without raising?
- `os.fsencode()` / `os.fsdecode()` and `sys.getfilesystemencoding()` — the round trip that is guaranteed.
- Passing a `bytes` path to `open()`: when it is the only correct option.
- Why `pathlib.Path` is a `str` underneath, and what that costs on a filesystem that disagrees.
- The macOS wrinkle: HFS+/APFS normalize names, so the name you wrote is not always the name you read back.

## See also

- [Encode and decode](../encode_and_decode/README.md) — `surrogateescape` in isolation
- [Normalization](../normalization/README.md) — the macOS half of the problem
