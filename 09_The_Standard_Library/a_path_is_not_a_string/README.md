# A `Path` is not a string

**Level:** 201 · for Python programmers

> **Stub — an outline, not a lesson.** There is no runnable example behind this page yet, so nothing on it has been through [the check that backs every other claim in this library](../../CONTRIBUTING.md). The bullets below are the questions the finished page has to answer.

**One line:** `pathlib.Path` is an object with `/` for joining and methods that touch the disk, not a `str` with extra methods — so `path + '.bak'` is a `TypeError`, `Path('a') / 'b'` is the join, `str(p)` is the way to a string and `os.fspath()` the polite one, `p.suffix` is the last dot only, and `Path('..').resolve()` asks the filesystem while `Path('a/../b')` never does.

## What the finished page has to answer

- Pure paths against concrete ones: which methods are string arithmetic, `parent`, `name`, `stem`, `suffix`, `with_suffix`, and which touch the disk, `exists`, `resolve`, `glob`, `read_text`.
- `suffix` on `archive.tar.gz`, and `suffixes`.
- `resolve()` follows symlinks and `absolute()` does not, and why `a/../b` is not `b` on a filesystem with links; the example has to build its own tree under `tempfile` and print relative paths only, because an absolute path is never the same on two machines.
- `read_text()` without `encoding=` makes the same bet [Opening a file](../../01_Text_and_Bytes/opening_a_file/README.md) describes.
- `glob()` returns a generator, so it is [used up](../../06_Iteration/an_iterator_is_used_up/README.md) after one loop.
- Where a `Path` is accepted: anything that calls `os.fspath()`, which is `open`, the `os` module and `subprocess`, and where it is not: a `str` method, `json.dumps`, a `+`.
- `PureWindowsPath` from macOS, for reading a path that came from somewhere else, and the bytes path, which [Filenames are not text](../../01_Text_and_Bytes/filenames_are_not_text/README.md) owns.

## See also

- [Filenames are not text](../../01_Text_and_Bytes/filenames_are_not_text/README.md) and [Opening a file](../../01_Text_and_Bytes/opening_a_file/README.md)
- [`pathlib` ↗](https://docs.python.org/3/library/pathlib.html) in the library reference
- [The Rust library's files chapter ↗](https://masiarek.github.io/rust-learning-library/04_Files/index.html), where a `Path` is not a string either, and not even valid UTF-8
