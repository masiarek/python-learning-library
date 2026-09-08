# Glossary

**Level:** reference · for anyone

Short entries. Each links to the page that explains it properly — a definition here is a pointer, not a substitute.

**bytearray** — the mutable `bytes`: the same numbers 0–255, but you may write into them. It has no literal — `bytearray(b"…")` wraps the `bytes` one — and it is unhashable, so it cannot be a dict key or a set member. See [`bytearray` is the mutable one](01_Text_and_Bytes/bytearray_is_mutable/README.md).

**bytes** — Python's type for a sequence of numbers 0–255. Indexing one gives an `int`, not a one-byte `bytes`. See [`str` is not `bytes`](01_Text_and_Bytes/str_is_not_bytes/README.md).

**casefold** — `str.casefold()`, a more aggressive `lower()` intended for caseless comparison; it can change a string's length (`ß` → `ss`). See [Normalization](01_Text_and_Bytes/normalization/README.md).

**category** — see *General_Category*.

**code point** — the number Unicode assigns to a character, written `U+0141`. What `len()` on a `str` counts. See [Counting characters](01_Text_and_Bytes/counting_characters/README.md).

**`bytes()` the call** — not a conversion but four constructors sharing a name: empty, encode-a-`str`, allocate-*n*-zero-bytes, build-from-ints. The argument's type picks. See [Making a `bytes` object](01_Text_and_Bytes/making_a_bytes_object/README.md).

**codec** — an entry in Python's codec registry. Usually a named conversion between `str` and `bytes` — `utf-8`, `cp1250`, `latin-1` — but the registry also holds `str`→`str` and `bytes`→`bytes` transforms (`rot13`, `base64`, `zlib`) that `.encode()`/`.decode()` refuse. See [Encode and decode](01_Text_and_Bytes/encode_and_decode/README.md) and [The codecs registry](01_Text_and_Bytes/the_codecs_registry/README.md).

**collation** — ordering text the way a language's alphabet does, as opposed to by code point. See [Sorting is not comparing](01_Text_and_Bytes/sorting_is_not_comparing/README.md).

**dangling symlink** — a symlink whose target does not exist. `os.lstat` reads it happily and `Path.is_symlink()` is `True`, while `Path.exists()`, `Path.is_file()` and `os.stat` all behave as though nothing is there — so it is indistinguishable from an absent path unless you ask with `lstat`. See [What kind of file is this?](01_Text_and_Bytes/what_kind_of_file_is_this/README.md).

**dependency group** — a named set of packages a *developer* of the project needs and a user never installs, declared in `[dependency-groups]` ([PEP 735 ↗](https://peps.python.org/pep-0735/)). Not the same as an optional dependency, which a user can ask for. See [`pyproject.toml`](02_Projects_and_Environments/pyproject_toml/README.md).

**error handler** — the function behind an `errors=` name, taking the exception and returning `(replacement, where to resume)`. Python ships eight; the registry is open, so a ninth is about ten lines ([PEP 293 ↗](https://peps.python.org/pep-0293/)). One name serves both directions, and it is called once per *run* of bad input, not once per character. See [The codecs registry](01_Text_and_Bytes/the_codecs_registry/README.md).

**errors policy** — the second argument to `.encode()` / `.decode()`, deciding what happens on a character the codec cannot handle: `strict`, `ignore`, `replace`, `backslashreplace`, `surrogateescape`. See [Encode and decode](01_Text_and_Bytes/encode_and_decode/README.md).

**format specification** — everything after the colon in a replacement field — `*^+12.3f` — handed as a *string* to the object's own `__format__`, which may define its own meaning for it. The standard one has nine slots in a fixed order. See [The format mini-language](01_Text_and_Bytes/the_format_mini_language/README.md).

**escape sequence** — a backslash and what follows it inside a literal, resolved by the **compiler**, not at run time. Python has fixed-width `\xNN`, greedy octal `\NNN`, and three code-point escapes that do not exist inside a `bytes` literal. An unrecognised one is kept. See [String literals](01_Text_and_Bytes/string_literals/README.md).

**General_Category** — the one-per-code-point classification (`Lu`, `Ll`, `Lo`, `Mn`, `Nd`, `No`, `Pc`…) that `unicodedata.category()` returns and that `str.isalpha()` tests. Distinct from a *property* like Alphabetic, which is derived from it and wider. See [Is it a letter?](01_Text_and_Bytes/is_it_a_letter/README.md).

**grapheme cluster** — what a reader calls one character, which may be several code points (`👨‍👩‍👧` is five). Not in the standard library. See [Counting characters](01_Text_and_Bytes/counting_characters/README.md).

**incremental decoder** — a codec as an *object* rather than a call: it holds the bytes of an unfinished character between calls, which is the only correct way to decode a stream arriving in arbitrary chunks. `codecs.getincrementaldecoder(name)()`; the last call needs `final=True` or a truncated stream reads as clean. See [The codecs registry](01_Text_and_Bytes/the_codecs_registry/README.md).

**isdecimal / isdigit / isnumeric** — three nested predicates, not synonyms: `Nd` only, then anything with a digit value, then anything with a numeric value at all. `int()` accepts the first. See [Is it a letter?](01_Text_and_Bytes/is_it_a_letter/README.md).

**line boundary** — one of the ten characters `str.splitlines()` breaks a string at: `\n`, `\v`, `\f`, `\r`, `\x1c`, `\x1d`, `\x1e`, `\x85` (NEL), `U+2028` and `U+2029`, plus `\r\n` counted once. Wider than the three a file in text mode recognizes and the one `re` does. See [What ends a line](01_Text_and_Bytes/what_ends_a_line/README.md).

**magic number** — the fixed first bytes that identify a file format, like a PNG's `89 50 4E 47 0D 0A 1A 0A`. Reading them is the only way to learn what a file actually contains; Python's standard library shipped sniffers for this (`imghdr`, `sndhdr`) until they were removed in 3.13. See [What kind of file is this?](01_Text_and_Bytes/what_kind_of_file_is_this/README.md).

**memoryview** — a borrowed window onto another object's buffer, so slicing it copies nothing. Writable when it wraps a `bytearray`, read-only over a `bytes`. Rust's `&mut [u8]`. See [`bytearray` is the mutable one](01_Text_and_Bytes/bytearray_is_mutable/README.md).

**mojibake** — text decoded with the wrong codec, so `ó` reads as `Ã³`. See [Encode and decode](01_Text_and_Bytes/encode_and_decode/README.md) and the [encodings library's page ↗](https://masiarek.github.io/encodings-learning-library/03_Encodings/mojibake/index.html).

**normalization** — rewriting text into a canonical form (NFC, NFD, NFKC, NFKD) so that strings which render identically also compare equal. See [Normalization](01_Text_and_Bytes/normalization/README.md).

**printable** — in Python, *not* about ink: `str.isprintable()` is true when `repr()` would not escape the character, which is General_Category `L`, `M`, `N`, `P` or `S` plus the ASCII space. So a space is printable and a tab is not, and `string.printable` — the older, POSIX sense — is not printable. See [`repr` is not `str`](01_Text_and_Bytes/repr_is_not_str/README.md).

**pyproject.toml** — the one declarative file describing a Python project: standardised tables (`[project]`, `[build-system]`, `[dependency-groups]`) plus a `[tool.<name>]` room per tool. Replaced the executable `setup.py`. See [`pyproject.toml`](02_Projects_and_Environments/pyproject_toml/README.md).

**repr** — the representation of an object aimed at a programmer rather than a reader, reached as `repr(x)`, `f'{x!r}'` or `f'{x = }'`, and used automatically for the elements of any container. Rust splits the same idea into the `Debug` and `Display` traits. See [`repr` is not `str`](01_Text_and_Bytes/repr_is_not_str/README.md).

**raw string** — a literal with the `r` prefix, in which backslash sequences are not interpreted. The backslash still ends the literal, so a raw string cannot end in an odd number of them. See [String literals](01_Text_and_Bytes/string_literals/README.md).

**str** — Python's text type, a sequence of code points. Has `.encode()` and no `.decode()`. See [`str` is not `bytes`](01_Text_and_Bytes/str_is_not_bytes/README.md).

**`chars` argument** — the operand of `strip` / `lstrip` / `rstrip`: a **set** of characters to remove, not a prefix, and it repeats. `'Arthur: three!'.lstrip('Arthur: ')` is `'ee!'`. `removeprefix` is the one that takes a prefix. See [`strip` is a set, not a prefix](01_Text_and_Bytes/strip_is_a_set/README.md).

**surrogateescape** — the errors policy that smuggles undecodable bytes through a `str` and restores them exactly on re-encode. How Python opens a filename that is not valid UTF-8. See [Filenames are not text](01_Text_and_Bytes/filenames_are_not_text/README.md).

**TOML** — the config format `pyproject.toml` is written in, defined to be UTF-8 and with no type coercion: quotes decide whether `1.10` is a string or a float, and only lower-case `true` / `false` are booleans. See [`pyproject.toml`](02_Projects_and_Environments/pyproject_toml/README.md) and [the spec ↗](https://toml.io/en/).

**tomllib** — the standard-library TOML *reader*, since Python 3.11. `load()` takes a file opened `"rb"`, `loads()` takes a `str`, and there is no writer. See [`pyproject.toml`](02_Projects_and_Environments/pyproject_toml/README.md).

**universal newlines** — the translation Python's text mode applies on the way in: `\r\n` and `\r` both arrive as `\n`. It is why iterating a file gives three line boundaries where `splitlines()` gives ten, and why `newline=""` exists for the `csv` module. See [What ends a line](01_Text_and_Bytes/what_ends_a_line/README.md).

**workspace** — one repository holding several packages that share a single resolved environment, declared by a tool rather than by any PEP (`[tool.uv.workspace]`). Borrowed from Cargo. See [`pyproject.toml`](02_Projects_and_Environments/pyproject_toml/README.md).
