# Roadmap

**Level:** reference · for anyone adding a page

Status of every page, and the order things are planned in. A **stub** has a permanent URL and an outline but no runnable example yet; see [CONTRIBUTING](CONTRIBUTING.md) for what it takes to graduate one.

**Companion page, added 2026-09-07.** This one tracks the pages that *exist*; [TODO.md](TODO.md) ranks what to write next, built from the questions Adam asked while reading the Python docs — each one routed to the page that answers it, half-answers it, or does not exist yet. Nothing on that page has been through the gates that back a lesson, and it says so at the top.

## Chapter 1 — Text and bytes

| Lesson | Status | Notes |
|---|---|---|
| [`str` is not `bytes`](01_Text_and_Bytes/str_is_not_bytes/README.md) | written | |
| [String literals](01_Text_and_Bytes/string_literals/README.md) | written, 2026-09-07 | nine prefixes and the eight combinations that do not exist, five spellings of one code point, `\x` fixed at two digits against greedy octal in the same grammar, and the unrecognised escape that is kept — which is why `'\bfoo\b'` as a regex matches nothing and raises nothing; the Rust and C columns are a dated table, not examples (rustc 1.98.0, clang 21.0.0) — three answers to "where does an escape stop", and Rust's raw string is the *stronger* one |
| [Encode and decode](01_Text_and_Bytes/encode_and_decode/README.md) | written | covers the `errors=` policies including `surrogateescape` |
| [Making a `bytes` object](01_Text_and_Bytes/making_a_bytes_object/README.md) | written, 2026-09-07 | the four-job constructor; the other-language table is dated and measured locally, not an example — CI here is Python-only |
| [`bytearray` is the mutable one](01_Text_and_Bytes/bytearray_is_mutable/README.md) | written, 2026-09-07 | the mutable half of the binary pair, and why there is no literal; the six-language table was run locally (rustc 1.98.0, go1.25.5, Swift 6.3.3, Node 20.20.2, clang 21.0.0) and is dated, not an example — CI here is Python-only. Java, C# and ABAP are prose |
| [Opening a file](01_Text_and_Bytes/opening_a_file/README.md) | **stub** | next up — needs a locale-independent way to show the default |
| [Counting characters](01_Text_and_Bytes/counting_characters/README.md) | written | |
| [Is it a letter?](01_Text_and_Bytes/is_it_a_letter/README.md) | written, 2026-09-06 | the twelve `is*` predicates; the Rust column is a dated table, not an example — `is_alphabetic` is the Alphabetic *property* where `isalpha` is the `L*` *categories* |
| [`repr` is not `str`](01_Text_and_Bytes/repr_is_not_str/README.md) | written, 2026-09-07 | the documented `isprintable()` rule checked over the whole code space with zero disagreements, `string.printable.isprintable()` being `False` by design, and `str(b'Zoot!')`; the Rust column is a dated table, not an example — Rust's `Debug` escapes exactly what Python calls non-printable on all seven samples, and its `is_printable` is private |
| [What ends a line](01_Text_and_Bytes/what_ends_a_line/README.md) | written, 2026-09-07 | ten boundaries scanned out of the whole code space, and the Bidi_Class B rule that predicts them; the cross-language ladder is a dated table, not an example — Java and .NET 6+ rows are from their specs, since there is no JDK on this machine |
| [`strip` is a set, not a prefix](01_Text_and_Bytes/strip_is_a_set/README.md) | written, 2026-09-07 | the three differences from `removeprefix` (repeat/once, set/string, both silent), the file-extension case where one filename in four survives, and the 29 code points `strip()` removes with no argument; the Rust column is a dated table, not an example — `trim_start_matches` takes a *pattern*, so the accident is not available, and `trim()` disagrees with `strip()` on `U+001C`–`U+001F` |
| [The format mini-language](01_Text_and_Bytes/the_format_mini_language/README.md) | written, 2026-09-07 | four doors onto one nine-slot grammar, the mix of numbering styles that raises, `-0` from a number that is not negative and the `z` option that fixes it, the `n` type that mutates process-global locale state, and `%` as a separate language kept alive by `bytes`; the Rust column is a dated table, not an example — same spec string, same bytes, and `format!` is a macro so runtime templates do not compile |
| [Normalization](01_Text_and_Bytes/normalization/README.md) | **stub** | |
| [Sorting is not comparing](01_Text_and_Bytes/sorting_is_not_comparing/README.md) | written | |
| [Standard in, standard out, and pipes](01_Text_and_Bytes/stdin_stdout_and_pipes/README.md) | **stub** | the example has to run under a pipe to show the effect |
| [Filenames are not text](01_Text_and_Bytes/filenames_are_not_text/README.md) | written, 2026-09-06 | the example touches no disk on purpose; APFS refuses invalid UTF-8 and is normalization-*insensitive*, not normalizing — both measured against Linux, both in a dated table rather than an answer key |
| [What kind of file is this?](01_Text_and_Bytes/what_kind_of_file_is_this/README.md) | written, 2026-09-07 | five APIs, five questions; `imghdr` and `sndhdr` were removed in 3.13 so the byte-reading answer is now hand-rolled. The version split and the `PermissionError` that `pathlib` swallows are dated tables, not keys — the key is byte-identical on macOS 3.14 and python:3.11/3.12/3.13/3.14-slim |
| [The codecs registry](01_Text_and_Bytes/the_codecs_registry/README.md) | written, 2026-09-07 | the three things in `codecs` that are not a second spelling of `str.encode`: the `_is_text_encoding` flag behind the non-text codecs, the stateful incremental pair, and the ninth error handler. The chunked-decode bug and its silent `errors='replace'` version are both in the key; so is the encoder twin, where a per-chunk `utf-16` encode leaves a `U+FEFF` in the data with no exception anywhere. The base64/zlib split is keyed on the round-trip check only, because what a decoder does with the malformed chunked form changes at 3.13 — the key itself is byte-identical on python:3.11/3.12/3.13/3.14-slim |

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
