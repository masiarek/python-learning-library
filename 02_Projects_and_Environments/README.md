# 02_Projects_and_Environments — the project file and the interpreter that runs it

**Level:** 101 → 201 · for Python programmers

Chapter 1 is about a value in memory. This chapter is about everything around it: which file says what your project is, which interpreter is running, how you hand it code, and which packages that interpreter can see. It is the part of Python that is not the language at all — no PEP describes a virtual environment's purpose, and yet nothing you write runs without one being right.

It is also where the answers changed most recently. `pyproject.toml` reached its current shape across three PEPs between 2016 and 2024, dependency groups landed in 2024, and the tool most people now reach for did not exist in 2021. A page written five years ago is not wrong so much as describing a different world, which is a good reason to start from the file and work outwards rather than from any one tool.

| # | Lesson | The question it answers | Status |
|---|---|---|---|
| 1 | [`pyproject.toml`](pyproject_toml/README.md) | What is this file, who reads which part, and how do I read it myself? | written |

## What comes next here

Named rather than stubbed, because a folder name is a permanent URL and an empty one is clutter:

- **The virtual environment** — what `.venv` actually is (a directory, a `pyvenv.cfg` and some symlinks), and why "activating" one is nothing more than a `PATH` edit
- **`sys.path` and how an import finds a file** — the single question behind almost every `ModuleNotFoundError`
- **The lockfile** — what a resolved, pinned set of versions buys you that a range in `pyproject.toml` does not
- **Where a script's dependencies can live** — [PEP 723 ↗](https://peps.python.org/pep-0723/) inline metadata, for the one-file program that still needs a package

## Where this sits relative to the other libraries

[Cargo and its `Cargo.toml` ↗](https://masiarek.github.io/rust-learning-library/05_Tooling/cargo_dependencies/index.html) in the Rust library are the sharpest comparison available for anything in this chapter — same file format, same workspace idea, one tool instead of several. Where a page here would only restate it, it links there.
