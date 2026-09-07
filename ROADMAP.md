# Roadmap

**Level:** reference · for anyone adding a page

Status of every page, and the order things are planned in. A **stub** has a permanent URL and an outline but no runnable example yet; see [CONTRIBUTING](CONTRIBUTING.md) for what it takes to graduate one.

## Chapter 1 — Text and bytes

| Lesson | Status | Notes |
|---|---|---|
| [`str` is not `bytes`](01_Text_and_Bytes/str_is_not_bytes/README.md) | written | |
| [Encode and decode](01_Text_and_Bytes/encode_and_decode/README.md) | written | covers the `errors=` policies including `surrogateescape` |
| [Making a `bytes` object](01_Text_and_Bytes/making_a_bytes_object/README.md) | written, 2026-09-07 | the four-job constructor; the other-language table is dated and measured locally, not an example — CI here is Python-only |
| [`bytearray` is the mutable one](01_Text_and_Bytes/bytearray_is_mutable/README.md) | written, 2026-09-07 | the mutable half of the binary pair, and why there is no literal; the six-language table was run locally (rustc 1.98.0, go1.25.5, Swift 6.3.3, Node 20.20.2, clang 21.0.0) and is dated, not an example — CI here is Python-only. Java, C# and ABAP are prose |
| [Opening a file](01_Text_and_Bytes/opening_a_file/README.md) | **stub** | next up — needs a locale-independent way to show the default |
| [Counting characters](01_Text_and_Bytes/counting_characters/README.md) | written | |
| [Is it a letter?](01_Text_and_Bytes/is_it_a_letter/README.md) | written, 2026-09-06 | the twelve `is*` predicates; the Rust column is a dated table, not an example — `is_alphabetic` is the Alphabetic *property* where `isalpha` is the `L*` *categories* |
| [Normalization](01_Text_and_Bytes/normalization/README.md) | **stub** | |
| [Sorting is not comparing](01_Text_and_Bytes/sorting_is_not_comparing/README.md) | written | |
| [Standard in, standard out, and pipes](01_Text_and_Bytes/stdin_stdout_and_pipes/README.md) | **stub** | the example has to run under a pipe to show the effect |
| [Filenames are not text](01_Text_and_Bytes/filenames_are_not_text/README.md) | written, 2026-09-06 | the example touches no disk on purpose; APFS refuses invalid UTF-8 and is normalization-*insensitive*, not normalizing — both measured against Linux, both in a dated table rather than an answer key |

## Chapter 2 — Projects and environments

| Lesson | Status | Notes |
|---|---|---|
| [`pyproject.toml`](02_Projects_and_Environments/pyproject_toml/README.md) | written | the standard tables, the `[tool.X]` rooms, workspaces, and `tomllib` |

Planned, and deliberately not yet folders: the virtual environment, `sys.path` and how an import finds a file, the lockfile, and [PEP 723 ↗](https://peps.python.org/pep-0723/) inline script metadata. See the [chapter page](02_Projects_and_Environments/README.md).

## Chapters after this one

Not yet folders, deliberately — a directory of empty stubs is clutter, and every folder name is a permanent URL. Named here so the shape is visible:

- **The data model** — `__len__`, `__eq__`, `__hash__`, and why `==` and `is` are different questions
- **Sequences and iteration** — iterators, generators, and the difference between lazy and eager
- **Functions** — arguments, closures, decorators, and the mutable-default trap
- **Errors** — exceptions as control flow, and what `except Exception` costs you
- **The standard library worth knowing** — `pathlib`, `dataclasses`, `collections`, `itertools`, `functools`
- **Testing** — and why a recorded-output check like this library's own is not a substitute for one

## Open questions

- **Where the boundary with the [encodings library ↗](https://masiarek.github.io/encodings-learning-library/) sits.** Its `04_Python` chapter has five stubs that overlap this one. The intended split is that it teaches *encodings* and this teaches *Python*; once chapter 1 here is finished, those stubs should probably point here rather than be written twice. Not yet done.
- **Whether a lesson may ever name a third-party library.** The rule is stdlib-only *examples*; [sorting](01_Text_and_Bytes/sorting_is_not_comparing/README.md) names PyICU in prose because omitting the correct production answer would be worse. That precedent should stay rare.
