# Glossary

**Level:** reference · for anyone

Short entries. Each links to the page that explains it properly — a definition here is a pointer, not a substitute.

**bytearray** — the mutable `bytes`: the same numbers 0–255, but you may write into them. It has no literal — `bytearray(b"…")` wraps the `bytes` one — and it is unhashable, so it cannot be a dict key or a set member. See [`bytearray` is the mutable one](01_Text_and_Bytes/bytearray_is_mutable/README.md).

**bytes** — Python's type for a sequence of numbers 0–255. Indexing one gives an `int`, not a one-byte `bytes`. See [`str` is not `bytes`](01_Text_and_Bytes/str_is_not_bytes/README.md).

**case conversion** — turning text into its uppercase, lowercase or titlecase *form*, for a person to read. `str.upper()`, `str.lower()`, `str.title()`. Unicode's Default Case Conversion, section 3.13.2 — **not** the same operation as case folding, which is why `'ß'.lower()` is `'ß'`. It is a whole-string operation: it may change the length, and `str.lower()` reads a letter's neighbours to pick Greek `σ` or `ς`. See [Lowercasing is not folding](01_Text_and_Bytes/lowercasing_is_not_folding/README.md).

**case folding** — producing a *key* nobody reads, such that two strings that differ only by case produce the same key. `str.casefold()`. Unicode's Default Case Folding, section 3.13.3, and the correct operation for caseless comparison — `'straße'.casefold() == 'STRASSE'.casefold()` where the `lower()` version is `False`. Folds 297 code points differently from `lower()`. See [Lowercasing is not folding](01_Text_and_Bytes/lowercasing_is_not_folding/README.md).

**casefold** — `str.casefold()`, the method that performs *case folding*; a more aggressive `lower()` for caseless comparison, which can change a string's length (`ß` → `ss`). See [Lowercasing is not folding](01_Text_and_Bytes/lowercasing_is_not_folding/README.md) and [Normalization](01_Text_and_Bytes/normalization/README.md).

**category** — see *General_Category*.

**cell** — one character position of a fixed-width grid: a terminal column, a monospaced font's advance. What a reader sees a padded column measured in, and *not* what `len()` counts — `'日本'` is two code points and four cells. Nothing in the standard library computes it. See [Padding is not alignment](01_Text_and_Bytes/padding_is_not_alignment/README.md).

**code point** — the number Unicode assigns to a character, written `U+0141`. What `len()` on a `str` counts. See [Counting characters](01_Text_and_Bytes/counting_characters/README.md).

**`bytes()` the call** — not a conversion but four constructors sharing a name: empty, encode-a-`str`, allocate-*n*-zero-bytes, build-from-ints. The argument's type picks. See [Making a `bytes` object](01_Text_and_Bytes/making_a_bytes_object/README.md).

**codec** — an entry in Python's codec registry. Usually a named conversion between `str` and `bytes` — `utf-8`, `cp1250`, `latin-1` — but the registry also holds `str`→`str` and `bytes`→`bytes` transforms (`rot13`, `base64`, `zlib`) that `.encode()`/`.decode()` refuse. See [Encode and decode](01_Text_and_Bytes/encode_and_decode/README.md) and [The codecs registry](01_Text_and_Bytes/the_codecs_registry/README.md).

**collation** — ordering text the way a language's alphabet does, as opposed to by code point. See [Sorting is not comparing](01_Text_and_Bytes/sorting_is_not_comparing/README.md).

**dangling symlink** — a symlink whose target does not exist. `os.lstat` reads it happily and `Path.is_symlink()` is `True`, while `Path.exists()`, `Path.is_file()` and `os.stat` all behave as though nothing is there — so it is indistinguishable from an absent path unless you ask with `lstat`. See [What kind of file is this?](01_Text_and_Bytes/what_kind_of_file_is_this/README.md).

**dependency group** — a named set of packages a *developer* of the project needs and a user never installs, declared in `[dependency-groups]` ([PEP 735 ↗](https://peps.python.org/pep-0735/)). Not the same as an optional dependency, which a user can ask for. See [`pyproject.toml`](02_Projects_and_Environments/pyproject_toml/README.md).

**East_Asian_Width** — the Unicode property that says how many cells a character asks for: `W` and `F` are two, `Na`/`H`/`N` are one, and `A` is **Ambiguous** — one cell in a Western context and two in a legacy East Asian one, decided by the reader's terminal rather than by the string. `unicodedata.east_asian_width` is the only cell-width data Python ships. See [Padding is not alignment](01_Text_and_Bytes/padding_is_not_alignment/README.md).

**error handler** — the function behind an `errors=` name, taking the exception and returning `(replacement, where to resume)`. Python ships eight; the registry is open, so a ninth is about ten lines ([PEP 293 ↗](https://peps.python.org/pep-0293/)). One name serves both directions, and it is called once per *run* of bad input, not once per character. See [The codecs registry](01_Text_and_Bytes/the_codecs_registry/README.md).

**errors policy** — the second argument to `.encode()` / `.decode()`, deciding what happens on a character the codec cannot handle: `strict`, `ignore`, `replace`, `backslashreplace`, `surrogateescape`. See [Encode and decode](01_Text_and_Bytes/encode_and_decode/README.md).

**fill character** — the single character a padding call repeats: the second argument to `ljust`/`rjust`/`center`, or the slot before the alignment in a format spec (`'.<6'`). Exactly one character, always — `'a'.ljust(5, 'ab')` is a `TypeError` — and it may itself be two cells wide, which makes the column worse rather than better. See [Padding is not alignment](01_Text_and_Bytes/padding_is_not_alignment/README.md).

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

**ordinal comparison** — comparing two strings by their code points, left to right, first difference wins: no alphabet, no locale, no case table, no normalization. What Python's `==`, `<`, `in`, `find`, `startswith`, `hash` and `sorted` all do, and the only mode Python has. The name is .NET's, which makes every string API take a `StringComparison`; Python's is invisible because there is nothing to choose. See [Comparison has a mode](01_Text_and_Bytes/comparison_has_a_mode/README.md).

**printable** — in Python, *not* about ink: `str.isprintable()` is true when `repr()` would not escape the character, which is General_Category `L`, `M`, `N`, `P` or `S` plus the ASCII space. So a space is printable and a tab is not, and `string.printable` — the older, POSIX sense — is not printable. See [`repr` is not `str`](01_Text_and_Bytes/repr_is_not_str/README.md).

**pyproject.toml** — the one declarative file describing a Python project: standardised tables (`[project]`, `[build-system]`, `[dependency-groups]`) plus a `[tool.<name>]` room per tool. Replaced the executable `setup.py`. See [`pyproject.toml`](02_Projects_and_Environments/pyproject_toml/README.md).

**repr** — the representation of an object aimed at a programmer rather than a reader, reached as `repr(x)`, `f'{x!r}'` or `f'{x = }'`, and used automatically for the elements of any container. Rust splits the same idea into the `Debug` and `Display` traits. See [`repr` is not `str`](01_Text_and_Bytes/repr_is_not_str/README.md).

**raw string** — a literal with the `r` prefix, in which backslash sequences are not interpreted. The backslash still ends the literal, so a raw string cannot end in an odd number of them. See [String literals](01_Text_and_Bytes/string_literals/README.md).

**sentinel** — a value inside a function's ordinary return type that stands for *no answer*: `str.find` returns `-1`. It is not an error and does not interrupt anything, so it reaches the next line like any other value — and `-1` in particular is a **valid index**, which is why an unchecked `find` result slices out the last character rather than failing. The alternatives are raising (`str.index`) and a type that cannot be used unwrapped (Rust's `Option`). See [Four ways to find it](01_Text_and_Bytes/finding_a_substring/README.md).

**separator field** — the middle element of the three-tuple from `str.partition` / `str.rpartition`. Empty exactly when the separator was not found, which is the only signal of a miss those two methods give — the tuple is always three long, so the unpack never raises. The other two fields cannot answer the question: on a miss the whole string lands in the first field for `partition` and the third for `rpartition`. See [Four ways to find it](01_Text_and_Bytes/finding_a_substring/README.md).

**sequence protocol** — the operations every Python sequence shares, `index` among them: `list`, `tuple`, `range`, `str` and `bytes` all have `.index()` and all raise `ValueError` on a miss. `find` is not part of it — it exists only on `str`, `bytes` and `bytearray`, which is why there is no `list.find` and why the `-1` mistake has nowhere else in the language to be written. See [Four ways to find it](01_Text_and_Bytes/finding_a_substring/README.md).

**slice** — both the operation `s[a:b:c]` and the built-in *type* it builds: a real object with `start`, `stop` and `step`, passed to `__getitem__` where an index would pass an `int`. Its bounds are clamped to the sequence's length before anything is read, so a slice cannot be out of range — only a step of `0` raises. See [Slicing is not indexing](01_Text_and_Bytes/slicing_is_not_indexing/README.md).

**str** — Python's text type, a sequence of code points. Has `.encode()` and no `.decode()`. See [`str` is not `bytes`](01_Text_and_Bytes/str_is_not_bytes/README.md).

**`chars` argument** — the operand of `strip` / `lstrip` / `rstrip`: a **set** of characters to remove, not a prefix, and it repeats. `'Arthur: three!'.lstrip('Arthur: ')` is `'ee!'`. `removeprefix` is the one that takes a prefix. See [`strip` is a set, not a prefix](01_Text_and_Bytes/strip_is_a_set/README.md).

**surrogateescape** — the errors policy that smuggles undecodable bytes through a `str` and restores them exactly on re-encode. How Python opens a filename that is not valid UTF-8. See [Filenames are not text](01_Text_and_Bytes/filenames_are_not_text/README.md).

**string interpolation** — building a string by substituting values into a template. Python has four spellings with different powers: an f-string (compiled from a literal, so a runtime template cannot be one), `str.format` and `format_map` (a field name may walk attributes and index), `%` (a separate, older language), and `string.Template` (a name and nothing else). Which one you may use is decided by where the template came from. See [The format mini-language](01_Text_and_Bytes/the_format_mini_language/README.md) and [The `string` module](01_Text_and_Bytes/the_string_module/README.md).

**`string.Template`** — the `$name` templating class, whose value is what its grammar *cannot* do: a placeholder is a `$` and an identifier and stops there, so a template from a user cannot walk an attribute the way a `str.format` field can. `substitute` raises on a missing or malformed name; `safe_substitute` never raises. See [The `string` module](01_Text_and_Bytes/the_string_module/README.md).

**tab stop** — the column a tab advances to: the next multiple of `tabsize`, not a fixed run of spaces. So what `expandtabs` writes for one tab depends on everything before it on the line, and only LF and CR reset the count. See [Padding is not alignment](01_Text_and_Bytes/padding_is_not_alignment/README.md).

**TOML** — the config format `pyproject.toml` is written in, defined to be UTF-8 and with no type coercion: quotes decide whether `1.10` is a string or a float, and only lower-case `true` / `false` are booleans. See [`pyproject.toml`](02_Projects_and_Environments/pyproject_toml/README.md) and [the spec ↗](https://toml.io/en/).

**titlecase** — Unicode's third case, distinct from upper and lower: `ǅ` (`U+01C5`) is General_Category `Lt`, the form a digraph takes at the start of a capitalised word, and it is neither `isupper()` nor `islower()`. Python has three word-capitalising functions that all handle that character correctly and disagree about where a word starts — `str.title()` breaks after any uncased character, so it gets `O'Brien` right and `Don'T` wrong; `string.capwords()` splits on whitespace and does the reverse; `str.capitalize()` does only the first character. See [Lowercasing is not folding](01_Text_and_Bytes/lowercasing_is_not_folding/README.md).

**tomllib** — the standard-library TOML *reader*, since Python 3.11. `load()` takes a file opened `"rb"`, `loads()` takes a `str`, and there is no writer. See [`pyproject.toml`](02_Projects_and_Environments/pyproject_toml/README.md).

**translation table** — the argument to `str.translate()`: a mapping from a **code point number** to an `int`, a `str` of any length, or `None` to delete. `str.maketrans` builds one, and any object whose `__getitem__` accepts an `int` will do — a `dict` subclass with `__missing__` maps everything you did not list. A `LookupError` from it means *leave this character alone*, which is why passing a `str` by mistake is a silent no-op. `bytes.translate` takes a different thing entirely: a 256-byte sequence, plus a separate `delete` argument. See [`translate` is a table, keyed by ordinal](01_Text_and_Bytes/translate_is_a_table/README.md).

**universal newlines** — the translation Python's text mode applies on the way in: `\r\n` and `\r` both arrive as `\n`. It is why iterating a file gives three line boundaries where `splitlines()` gives ten, and why `newline=""` exists for the `csv` module. See [What ends a line](01_Text_and_Bytes/what_ends_a_line/README.md).

**workspace** — one repository holding several packages that share a single resolved environment, declared by a tool rather than by any PEP (`[tool.uv.workspace]`). Borrowed from Cargo. See [`pyproject.toml`](02_Projects_and_Environments/pyproject_toml/README.md).
