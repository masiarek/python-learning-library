# Python — Learning Library

A runnable learning library about Python. One idea per page, every claim backed by a stdlib-only program that runs and is checked against its recorded output in CI.

**Read it as a website:** <https://masiarek.github.io/python-learning-library/>

<!-- --8<-- [start:body] -->

## What this is

One folder per idea. Each holds a page that makes a claim and an `examples/` program that proves it. The programs import nothing but the standard library, so any page runs with the `python3` you already have — and CI runs every one of them on both Ubuntu and macOS, comparing the output against a recorded answer key. A page cannot quietly go stale, because the build fails when its program stops printing what the page says it prints.

It begins with **text and bytes** rather than with syntax. That is where a wrong mental model survives longest before failing, and where it fails on someone else's data rather than yours — and it is the part of Python that differs most sharply from C, ABAP and Rust, which makes it the best place to start cross-referencing the sibling libraries.

## Start

- **[Start here](00_Start_Here/README.md)** — what this is, and a four-question diagnostic
- **[Chapter 1 — Text and bytes](01_Text_and_Bytes/README.md)** — the type boundary, encoding, counting, sorting
- **[Chapter 2 — Projects and environments](02_Projects_and_Environments/README.md)** — the project file, and the interpreter that runs it
- **[The crosswalk](CROSSWALK.md)** — the same ideas in Rust, C and ABAP, one table per question
- **[Roadmap](ROADMAP.md)** — what is written, what is a stub, what is next
- **[What to write next](TODO.md)** — the questions backlog, ranked, and the five pages worth writing first

## The written lessons

| Lesson | The question |
|---|---|
| [`str` is not `bytes`](01_Text_and_Bytes/str_is_not_bytes/README.md) | Which type am I holding, and why won't Python mix them? |
| [Encode and decode](01_Text_and_Bytes/encode_and_decode/README.md) | Which direction is which, and what does `errors=` throw away? |
| [Making a `bytes` object](01_Text_and_Bytes/making_a_bytes_object/README.md) | Why is `bytes(5)` five zero bytes and `bytes([5])` one? |
| [`bytearray` is the mutable one](01_Text_and_Bytes/bytearray_is_mutable/README.md) | Which of the two binary types can I write into, and what does mutability cost? |
| [Counting characters](01_Text_and_Bytes/counting_characters/README.md) | How long is this string — and which of the four answers did you want? |
| [Is it a letter?](01_Text_and_Bytes/is_it_a_letter/README.md) | What do `isalpha`, `isdigit` and the other ten actually test? |
| [`repr` is not `str`](01_Text_and_Bytes/repr_is_not_str/README.md) | Why is a space "printable" and a tab not — and what did `str(b'x')` just do? |
| [What ends a line](01_Text_and_Bytes/what_ends_a_line/README.md) | Which characters count as a line break — and why do I get three different answers? |
| [`strip` is a set, not a prefix](01_Text_and_Bytes/strip_is_a_set/README.md) | Why did `lstrip('Arthur: ')` eat three more characters than I asked for? |
| [The format mini-language](01_Text_and_Bytes/the_format_mini_language/README.md) | Is `f'{x:>8}'` the same grammar as `'{:>8}'.format(x)` — and where does `%` fit? |
| [Sorting is not comparing](01_Text_and_Bytes/sorting_is_not_comparing/README.md) | Why does `sorted()` put `Łukasiewicz` after `Zawadzki`? |
| [Filenames are not text](01_Text_and_Bytes/filenames_are_not_text/README.md) | What is actually allowed in a filename, and why can't I print one? |
| [`pyproject.toml`](02_Projects_and_Environments/pyproject_toml/README.md) | What is this file, who reads which part, and how do I read it myself? |

## Run it

```bash
python3 01_Text_and_Bytes/sorting_is_not_comparing/examples/sorting_is_not_comparing_py.py
python3 tools/run_examples.py --check     # what CI runs
```

## Sibling libraries

This is one of a set. Where another already teaches something, this one links rather than repeats — see [the crosswalk](CROSSWALK.md).

- [Encodings ↗](https://masiarek.github.io/encodings-learning-library/) — bits, bytes, characters, encodings, strings
- [Rust ↗](https://masiarek.github.io/rust-learning-library/) — including `String`, `&str` and `char`
- [ABAP ↗](https://masiarek.github.io/abap-learning-library/) — the SAP side

House conventions for adding a page: [CONTRIBUTING.md](CONTRIBUTING.md).

<!-- --8<-- [end:body] -->
