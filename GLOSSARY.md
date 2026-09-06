# Glossary

**Level:** reference · for anyone

Short entries. Each links to the page that explains it properly — a definition here is a pointer, not a substitute.

**bytes** — Python's type for a sequence of numbers 0–255. Indexing one gives an `int`, not a one-byte `bytes`. See [`str` is not `bytes`](01_Text_and_Bytes/str_is_not_bytes/README.md).

**casefold** — `str.casefold()`, a more aggressive `lower()` intended for caseless comparison; it can change a string's length (`ß` → `ss`). See [Normalization](01_Text_and_Bytes/normalization/README.md).

**code point** — the number Unicode assigns to a character, written `U+0141`. What `len()` on a `str` counts. See [Counting characters](01_Text_and_Bytes/counting_characters/README.md).

**codec** — the named conversion between `str` and `bytes` — `utf-8`, `cp1250`, `latin-1`. Python's registry holds around a hundred. See [Encode and decode](01_Text_and_Bytes/encode_and_decode/README.md).

**collation** — ordering text the way a language's alphabet does, as opposed to by code point. See [Sorting is not comparing](01_Text_and_Bytes/sorting_is_not_comparing/README.md).

**dependency group** — a named set of packages a *developer* of the project needs and a user never installs, declared in `[dependency-groups]` ([PEP 735 ↗](https://peps.python.org/pep-0735/)). Not the same as an optional dependency, which a user can ask for. See [`pyproject.toml`](02_Projects_and_Environments/pyproject_toml/README.md).

**errors policy** — the second argument to `.encode()` / `.decode()`, deciding what happens on a character the codec cannot handle: `strict`, `ignore`, `replace`, `backslashreplace`, `surrogateescape`. See [Encode and decode](01_Text_and_Bytes/encode_and_decode/README.md).

**grapheme cluster** — what a reader calls one character, which may be several code points (`👨‍👩‍👧` is five). Not in the standard library. See [Counting characters](01_Text_and_Bytes/counting_characters/README.md).

**mojibake** — text decoded with the wrong codec, so `ó` reads as `Ã³`. See [Encode and decode](01_Text_and_Bytes/encode_and_decode/README.md) and the [encodings library's page ↗](https://masiarek.github.io/encodings-learning-library/03_Encodings/mojibake/index.html) ↗.

**normalization** — rewriting text into a canonical form (NFC, NFD, NFKC, NFKD) so that strings which render identically also compare equal. See [Normalization](01_Text_and_Bytes/normalization/README.md).

**pyproject.toml** — the one declarative file describing a Python project: standardised tables (`[project]`, `[build-system]`, `[dependency-groups]`) plus a `[tool.<name>]` room per tool. Replaced the executable `setup.py`. See [`pyproject.toml`](02_Projects_and_Environments/pyproject_toml/README.md).

**str** — Python's text type, a sequence of code points. Has `.encode()` and no `.decode()`. See [`str` is not `bytes`](01_Text_and_Bytes/str_is_not_bytes/README.md).

**surrogateescape** — the errors policy that smuggles undecodable bytes through a `str` and restores them exactly on re-encode. How Python opens a filename that is not valid UTF-8. See [Filenames are not text](01_Text_and_Bytes/filenames_are_not_text/README.md).

**TOML** — the config format `pyproject.toml` is written in, defined to be UTF-8 and with no type coercion: quotes decide whether `1.10` is a string or a float, and only lower-case `true` / `false` are booleans. See [`pyproject.toml`](02_Projects_and_Environments/pyproject_toml/README.md) and [the spec ↗](https://toml.io/en/).

**tomllib** — the standard-library TOML *reader*, since Python 3.11. `load()` takes a file opened `"rb"`, `loads()` takes a `str`, and there is no writer. See [`pyproject.toml`](02_Projects_and_Environments/pyproject_toml/README.md).

**workspace** — one repository holding several packages that share a single resolved environment, declared by a tool rather than by any PEP (`[tool.uv.workspace]`). Borrowed from Cargo. See [`pyproject.toml`](02_Projects_and_Environments/pyproject_toml/README.md).
