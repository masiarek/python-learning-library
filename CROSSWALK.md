# The crosswalk

**Level:** reference · for anyone using more than one of these libraries

**One line:** One idea per row, and what each language does with it — so a concept you already understand in ABAP or Rust can be looked up rather than relearned.

These libraries were written separately and overlap on purpose: text handling is the place where a working programmer meets the same problem in every language and gets a different answer each time. This page is the index across them. It states the *idea* once, then names what each language calls it, so you can start from the column you already know.

A cell in the Python column links into this library. A cell in another column links into that library, or names the API when there is no page for it yet — an unlinked cell is a real answer with no page behind it, and often a gap worth filling. Stubs are deliberately not linked.

**The ABAP column is not machine-checked** — CI cannot run ABAP, and the ABAP library is one page long. Treat those cells as the name to search for, not as verified behaviour. Every Python, Rust and C cell either links to a page whose output is recorded, or states something checked while writing this one.

## Text and bytes

| The idea | Python | Rust | C | ABAP |
|---|---|---|---|---|
| Text vs. raw bytes as separate types | [`str` / `bytes`](01_Text_and_Bytes/str_is_not_bytes/README.md) | [`String` / `Vec<u8>` ↗](https://masiarek.github.io/rust-learning-library/14_Strings/anatomy_of_a_string/index.html) | no distinction — `char *` is both | [`string` / `xstring` ↗](https://masiarek.github.io/abap-learning-library/01_Foundations/how_long_is_a_string/index.html) |
| Converting between them | [`.encode()` / `.decode()`](01_Text_and_Bytes/encode_and_decode/README.md) | [`String::from_utf8` ↗](https://masiarek.github.io/rust-learning-library/14_Strings/string_methods/string_from_utf8/index.html) / [`.as_bytes()` ↗](https://masiarek.github.io/rust-learning-library/14_Strings/str_methods/str_as_bytes/index.html) | hand-rolled, or `iconv` | `cl_abap_conv_codepage` |
| Making one from scratch | [`bytes(n)` / `bytes(s, enc)` / `bytes([…])`](01_Text_and_Bytes/making_a_bytes_object/README.md) — one name, four jobs | `vec![0u8; n]` / `.as_bytes()` / `vec![1, 2, 3]` — three names | `{0}` for the zeros; a `char *` already is the bytes | `xstring` literal, or `cl_abap_conv_codepage` |
| What happens on invalid input | `UnicodeDecodeError`, or an [`errors=` policy](01_Text_and_Bytes/encode_and_decode/README.md) | [`from_utf8` returns `Result` ↗](https://masiarek.github.io/rust-learning-library/14_Strings/str_methods/str_from_utf8/index.html); [`from_utf8_lossy` substitutes ↗](https://masiarek.github.io/rust-learning-library/14_Strings/string_methods/string_from_utf8_lossy/index.html) | [undefined — nothing checks ↗](https://masiarek.github.io/encodings-learning-library/03_Encodings/validation_is_a_boundary/index.html) | exception, or a replacement char |
| The "never fails" escape hatch | [`surrogateescape`](01_Text_and_Bytes/filenames_are_not_text/README.md) | none in std — the type will not hold it | — | — |
| Guaranteed-valid text type | `str` (code points, may hold lone surrogates) | `String` — [UTF-8, enforced by the type ↗](https://masiarek.github.io/encodings-learning-library/05_Rust/string_is_bytes_that_promise_utf8/index.html) | — | `string` (UTF-16 internally) |

The sharpest difference is the third row. Rust makes invalid UTF-8 *unrepresentable* in a `String`, so the check happens once at the boundary and never again. Python checks at the boundary too but leaves you a way through it (`surrogateescape`), because a filename has to be openable even when it is not text. C checks nowhere. Which of those is right depends entirely on whether your program can refuse its input.

## Showing a value

| The idea | Python | Rust | ABAP |
|---|---|---|---|
| Show it to a person | [`str(x)`](01_Text_and_Bytes/repr_is_not_str/README.md), `f'{x}'` | `Display`, `{}` | `WRITE` |
| Show it to a programmer | [`repr(x)`](01_Text_and_Bytes/repr_is_not_str/README.md), `f'{x!r}'`, `f'{x = }'` | [`Debug`, `{:?}` ↗](https://masiarek.github.io/rust-learning-library/14_Strings/the_format_language/index.html) | the Debugger, plus a hex view |
| …with non-ASCII escaped | `ascii(x)`, `f'{x!a}'` | `escape_default` | — |
| What happens with no "person" form | falls back to `repr` — **silently** | will not compile: `Display` is not implemented | — |
| "Printable" | [`str.isprintable()`](01_Text_and_Bytes/repr_is_not_str/README.md) — what `repr` will not escape | no public predicate; `is_control` is a narrower question | `CO` against a set you wrote |
| A container's elements | always `repr` | always `Debug` | — |

Row four is the one with consequences. Python's `str()` falling back to `repr()` is what makes `str(b'Zoot!')` return `"b'Zoot!'"` instead of raising, and Rust's refusal to fall back is what makes the equivalent a compile error. Both languages define "printable" as *"what the debug form does not escape"*, and on every sample tested they agree about which characters those are.

## Mutable and immutable

| The idea | Python | Rust | C | ABAP |
|---|---|---|---|---|
| The frozen binary type | `bytes` | `&[u8]` — and `b"abc"` is a `&[u8; 3]` | none; nothing is frozen | `xstring` — a value, copied on assignment |
| The one you can write into | [`bytearray`](01_Text_and_Bytes/bytearray_is_mutable/README.md) | [`Vec<u8>` ↗](https://masiarek.github.io/rust-learning-library/26_Collections/the_vec/index.html) behind a `mut` binding | `char buf[N]` | the same `xstring` |
| Where mutability is written down | in the **type** — a Python name has no `mut` | in the **binding**, and in `&` against `&mut` | nowhere | nowhere |
| A literal you can edit | none — the literal is the `bytes` | none — [`b"abc"` is behind a `&` ↗](https://masiarek.github.io/rust-learning-library/14_Strings/rfc_69_byte_literals/index.html), and the write does not compile | `char *p = "abc"` compiles; writing is **undefined behaviour** | — |
| A borrowed view, no copy | `memoryview` | `&mut [u8]` | a pointer, unchecked | a field symbol (`ASSIGN`) |
| Letting a callee fill your buffer | `readinto` / `recv_into` / `pack_into` | `read_exact(&mut buf)` | `read(fd, buf, n)` | — |
| Two names for one buffer | assignment aliases; the callee can edit yours | only through `&mut`, and only one at a time | any two pointers | not by assignment — `ASSIGN` or `REF TO` |
| Writing past the end | `IndexError` | panics | corrupts whatever was next | — |
| What mutability costs | unhashable — no dict key, no set member | nothing at runtime; the borrow checker charges at compile time | nothing, and no safety either | — |

Python is the odd one out in the third row, and the rest of the column follows from it. A Python name cannot be declared mutable or not, so the only place left to record the difference is the object — which is why Python needs *two* types where Rust needs one `Vec<u8>` and a keyword. Rust and Swift put it on the binding; Go and C put it nowhere, and Go gets away with it only because `string` is frozen and `[]byte(s)` is an honest copy. C's version of this row is the bug the other four languages were designed against: writing through `char *p = "abc"` compiles cleanly and dies at runtime.

## Length and indexing

| The idea | Python | Rust | ABAP |
|---|---|---|---|
| Length in bytes | `len(s.encode("utf-8"))` | [`s.len()` ↗](https://masiarek.github.io/rust-learning-library/14_Strings/str_methods/str_len/index.html) — bytes, always | [`xstrlen( )` ↗](https://masiarek.github.io/abap-learning-library/01_Foundations/how_long_is_a_string/index.html) |
| Length in UTF-16 units | `len(s.encode("utf-16-le")) // 2` | [`s.encode_utf16().count()` ↗](https://masiarek.github.io/rust-learning-library/14_Strings/four_lengths/index.html) | `strlen( )` — this is ABAP's default |
| Length in code points | [`len(s)`](01_Text_and_Bytes/counting_characters/README.md) | [`s.chars().count()` ↗](https://masiarek.github.io/rust-learning-library/14_Strings/meet_the_char/index.html) | — (`strlen( )` counts UTF-16 units) |
| Length a reader would agree with | not in the stdlib | not in std — needs a crate | — |
| Indexing by position | `s[0]` gives a 1-char `str` | [`s[0]` does not compile ↗](https://masiarek.github.io/rust-learning-library/14_Strings/string_slices/index.html) | `s(0)` gives a code unit |
| Walking it one unit at a time | `for c in s` — code points | [`.chars()` / `.bytes()` / `.char_indices()` ↗](https://masiarek.github.io/rust-learning-library/14_Strings/walking_a_string/index.html) | offset arithmetic on code units |

Rust's refusal to index a string by integer is the design decision that most annoys newcomers and most reliably prevents the bug: `s[0..1]` on a multi-byte character *panics* rather than returning half a character. Python returns a whole code point, which is right more often than C and still not the same as a character. ABAP returns a UTF-16 code unit, so an emoji is two.

## Ordering and comparison

| The idea | Python | Rust | ABAP |
|---|---|---|---|
| Default sort order | [code point](01_Text_and_Bytes/sorting_is_not_comparing/README.md) | [code point (`Ord` on `str`) ↗](https://masiarek.github.io/rust-learning-library/14_Strings/comparing_strings/index.html) | UTF-16 code unit |
| Alphabetical for a real language | `locale.strxfrm`, or ICU | needs a crate | collation-aware compare, or a sort key column |
| Same-looking strings comparing unequal | [normalization](01_Text_and_Bytes/normalization/README.md) | same problem, same fix | same problem |
| Case-insensitive comparison | [`str.casefold()` ↗](https://masiarek.github.io/encodings-learning-library/02_Characters/preparing_a_string/index.html) | [`str::to_lowercase` ↗](https://masiarek.github.io/rust-learning-library/14_Strings/str_methods/str_to_lowercase/index.html) (locale-independent) | `TRANSLATE ... TO UPPER CASE` |
| ASCII-only shortcut | `s.lower()` has none — it is always Unicode | [`eq_ignore_ascii_case` ↗](https://masiarek.github.io/rust-learning-library/14_Strings/str_methods/str_eq_ignore_ascii_case/index.html) — cheap, and silently skips `Ł` | — |

All three languages get this equally wrong by default, and for the same reason: code-point order is the only ordering available without a locale database. This is the one row where "Python's answer" is not really Python's — it is everyone's.

## Classifying a character

| The idea | Python | Rust | ABAP |
|---|---|---|---|
| Is it a letter? | [`str.isalpha()`](01_Text_and_Bytes/is_it_a_letter/README.md) — General_Category `L*` | [`char::is_alphabetic` ↗](https://masiarek.github.io/rust-learning-library/14_Strings/meet_the_char/index.html) — the Alphabetic *property*, which is wider | `CO` against a character set, by hand |
| Is it a digit you can `int()`? | `str.isdecimal()` — `Nd` | `char::to_digit(10).is_some()` — ASCII only | `CO '0123456789'` |
| Is it a number of any kind? | `str.isnumeric()` — Numeric_Type, so `一` counts | `char::is_numeric` — `N*` categories, so `一` does not | — |
| Whitespace | `str.isspace()` — Unicode, plus `\x1c`–`\x1f` | [`char::is_whitespace` ↗](https://masiarek.github.io/rust-learning-library/14_Strings/rfc_1054_str_words/index.html) — `White_Space` only | `cl_abap_char_utilities` constants |
| Whole-string version | 12 methods on `str`; the ten class predicates also mean "…and not empty" | only three — [`is_ascii` ↗](https://masiarek.github.io/rust-learning-library/14_Strings/str_methods/str_is_ascii/index.html), [`is_empty` ↗](https://masiarek.github.io/rust-learning-library/14_Strings/str_methods/str_is_empty/index.html), [`is_char_boundary` ↗](https://masiarek.github.io/rust-learning-library/14_Strings/str_methods/str_is_char_boundary/index.html) — else you write `.chars().all(…)` | `CO` is already whole-field |
| The empty string | `False` for the ten class predicates | `true` — `all()` over nothing | worth checking on your system |
| Which edition of the table answered | `unicodedata.unidata_version` | whatever `rustc` was built with | the system code page |

This is the one section where the *names* match and the *sets* do not, in both directions: Rust's `is_alphabetic` accepts combining marks that Python's `isalpha` rejects, and Python's `isnumeric` accepts a CJK ideograph that Rust's `is_numeric` rejects. The measured grid is on [Is it a letter?](01_Text_and_Bytes/is_it_a_letter/README.md). The last row is the general form of the hazard — every one of these is a table lookup whose answer depends on which edition your toolchain was built against — and it has its own page: [the table has a version ↗](https://masiarek.github.io/encodings-learning-library/02_Characters/the_table_has_a_version/index.html).

## Taking a string apart, and putting one together

| The idea | Python | Rust | ABAP |
|---|---|---|---|
| Split on a separator | `s.split(sep)` | [`str::split` ↗](https://masiarek.github.io/rust-learning-library/14_Strings/str_methods/str_split/index.html) — lazy, returns an iterator | `SPLIT ... AT ... INTO TABLE` |
| Split on whitespace | `s.split()` — no argument | [`str::split_whitespace` ↗](https://masiarek.github.io/rust-learning-library/14_Strings/str_methods/str_split_whitespace/index.html) | `CONDENSE`, then `SPLIT` |
| Split into lines | [`s.splitlines()`](01_Text_and_Bytes/what_ends_a_line/README.md) | [`str::lines` ↗](https://masiarek.github.io/rust-learning-library/14_Strings/str_methods/str_lines/index.html) — and [what counts as a line ending ↗](https://masiarek.github.io/rust-learning-library/14_Strings/rfc_1212_line_endings/index.html) | `SPLIT AT cl_abap_char_utilities=>newline` |
| Which characters end a line | **ten** — `\n \v \f \r \x1c \x1d \x1e \x85` U+2028 U+2029, plus `\r\n` | **one**, plus a trailing `\r` trimmed — a lone `\r` is data | whichever constant you named; there is no default |
| …when reading a file instead | **three** — universal newlines gives `\n`, `\r`, `\r\n` | the same as `lines()`; `BufRead` does not have a second rule | `OPEN DATASET … IN TEXT MODE` — platform-dependent |
| Split once, keep the rest | `s.split(sep, 1)` | [`str::split_once` ↗](https://masiarek.github.io/rust-learning-library/14_Strings/str_methods/str_split_once/index.html) — returns an `Option` of the pair | — |
| What an empty separator does | `ValueError` | [`""` splits at every char boundary ↗](https://masiarek.github.io/rust-learning-library/14_Strings/splitting_on_nothing/index.html) — and yields empties at both ends | — |
| Join | `sep.join(parts)` | [`parts.join(sep)` ↗](https://masiarek.github.io/rust-learning-library/14_Strings/concatenating_strings/index.html) — the receiver is the slice, not the separator | `CONCATENATE ... SEPARATED BY` |
| Build up in a loop | `"".join(list)`, or `io.StringIO` | [`String::push_str` ↗](https://masiarek.github.io/rust-learning-library/14_Strings/building_a_string/index.html) — with `with_capacity` when you know the size | `CONCATENATE` in a loop |
| Find a substring | `s.find` / `s.index` — character offset | [`str::find` ↗](https://masiarek.github.io/rust-learning-library/14_Strings/str_methods/str_find/index.html) — **byte** offset, and `Option` rather than `-1` | `FIND ... IN`, `sy-fdpos` |
| Is it in there at all? | `sub in s` | [`str::contains` ↗](https://masiarek.github.io/rust-learning-library/14_Strings/str_methods/str_contains/index.html) | `CS` |
| Replace | `s.replace(a, b)` | [`str::replace` ↗](https://masiarek.github.io/rust-learning-library/14_Strings/str_methods/str_replace/index.html), [`replacen` ↗](https://masiarek.github.io/rust-learning-library/14_Strings/str_methods/str_replacen/index.html) for a count | `REPLACE ALL OCCURRENCES OF` |
| Trim the ends | [`s.strip()`](01_Text_and_Bytes/strip_is_a_set/README.md) — 29 code points, not four | [`str::trim` ↗](https://masiarek.github.io/rust-learning-library/14_Strings/str_methods/str_trim/index.html) — `White_Space`, so it leaves `U+001C`–`U+001F` that Python removes; `trim_ascii` is the cheap one | `CONDENSE`, or `SHIFT ... LEFT DELETING` |
| Trim a *set* of characters | [`s.lstrip(chars)`](01_Text_and_Bytes/strip_is_a_set/README.md) — the argument is a bag, and it repeats | `trim_start_matches(&[char])` — a `&str` pattern means the **whole string**, so you must spell the set out | `SHIFT … DELETING LEADING` takes a mask |
| Prefix and suffix | [`s.startswith`, `s.removeprefix`](01_Text_and_Bytes/strip_is_a_set/README.md) — once, and silent when it did not match | [`starts_with` ↗](https://masiarek.github.io/rust-learning-library/14_Strings/str_methods/str_starts_with/index.html), [`strip_prefix` ↗](https://masiarek.github.io/rust-learning-library/14_Strings/str_methods/str_strip_prefix/index.html) — returns `Option`, so "not there" is a value | `CP` with a pattern |
| Repeat | `s * 3` | [`str::repeat` ↗](https://masiarek.github.io/rust-learning-library/14_Strings/str_methods/str_repeat/index.html) | `DO 3 TIMES`, `CONCATENATE` |
| Parse into a number | `int(s)` / `float(s)` | [`s.parse::<T>()` ↗](https://masiarek.github.io/rust-learning-library/14_Strings/parsing_a_string/index.html) — the type decides the parser | `MOVE`, with silent conversion |
| Interpolate values in | [f-strings, `format()`, `str.format`](01_Text_and_Bytes/the_format_mini_language/README.md) — one grammar, four doors | [`format!` ↗](https://masiarek.github.io/rust-learning-library/14_Strings/the_format_language/index.html) — the same spec string produces the same bytes; a **macro**, so a runtime template does not compile | string templates, options named rather than punctuated |
| The older spelling | `'%s' % x` — one operator, one operand, and the only one that works on `bytes` | — | — |
| A literal with no escapes | `r"..."` | [`r#"..."#` ↗](https://masiarek.github.io/rust-learning-library/14_Strings/raw_strings_and_escapes/index.html) — the hashes let you nest quotes | — |

Two things run through the whole table. **Rust's versions are lazy and byte-indexed**: `split` hands back an iterator you can stop consuming, and `find` gives a byte offset you must not treat as a character position — which is the same trap as indexing, one method along. And **Rust returns `Option` where Python returns a sentinel or raises**: `find` gives `None` rather than `-1`, `split_once` gives `None` rather than a one-element list, so the failure is in the type instead of in the docs. The Python column here is thin on links on purpose — this library's chapter 1 is about the text *model*, and the method-by-method tour is one of the gaps this page is meant to make visible.

## Numbers, bytes and hex

| The idea | Python | Rust | C | Where the idea itself lives |
|---|---|---|---|---|
| A byte | `int` 0–255, or one element of `bytes` | [`u8` ↗](https://masiarek.github.io/rust-learning-library/19_Numbers/meet_the_byte/index.html) | `unsigned char` | [A byte is eight bits ↗](https://masiarek.github.io/encodings-learning-library/01_Bits_and_Bytes/a_byte_is_eight_bits/index.html) |
| A number that is not a byte | [`bytes([256])` raises `ValueError`](01_Text_and_Bytes/making_a_bytes_object/README.md) — nothing wraps | a literal will not compile; `300 as u8` is **44**, `u8::try_from` gives `Err` | `(unsigned char)300` is **44** — a warning at most | [A byte is eight bits ↗](https://masiarek.github.io/encodings-learning-library/01_Bits_and_Bytes/a_byte_is_eight_bits/index.html) |
| Writing one down in hex | `0xFF`, `hex(n)` | [`0xFF`, `{:#x}` ↗](https://masiarek.github.io/rust-learning-library/19_Numbers/why_hexadecimal/index.html) | `0xFF`, `%x` | [Hex is a shorthand ↗](https://masiarek.github.io/encodings-learning-library/01_Bits_and_Bytes/hex_is_a_shorthand/index.html) |
| Digit separators in a literal | `1_000_000` | [`1_000_000` ↗](https://masiarek.github.io/rust-learning-library/19_Numbers/writing_a_number_down/index.html) | `1'000'000` — C++14, and C23; rejected by C17 | — |
| Bytes to a hex string and back | `b.hex()` / `bytes.fromhex()` | `{:02x}` per byte; `hex` crate to parse | `printf("%02x")` | [Reading a hex dump ↗](https://masiarek.github.io/encodings-learning-library/01_Bits_and_Bytes/reading_a_hex_dump/index.html) |
| Is `414243` a number or three bytes? | depends entirely on the call you make | same — the type says which | same | [Hex: number or bytes? ↗](https://masiarek.github.io/encodings-learning-library/01_Bits_and_Bytes/hex_number_or_bytes/index.html) |
| Integer ↔ bytes, with an endianness | `int.to_bytes(n, "big")` | `u32::to_be_bytes` / `from_be_bytes` | cast, or `htonl` | [Byte order and the BOM ↗](https://masiarek.github.io/encodings-learning-library/03_Encodings/byte_order_and_bom/index.html) |
| Bit flags in one integer | `enum.IntFlag` | [`bitflags`-style constants ↗](https://masiarek.github.io/rust-learning-library/19_Numbers/bit_flags/index.html) | `#define` and bitwise or | — |
| What a float actually stores | `float` is IEEE 754 double | [`f32` / `f64` ↗](https://masiarek.github.io/rust-learning-library/19_Numbers/what_a_float_stores/index.html) | `float` / `double` | — |
| Overflow | `int` is arbitrary-precision — no overflow | panics in debug, wraps in release — [`checked_` / `saturating_` ↗](https://masiarek.github.io/rust-learning-library/29_Conversion/casting_with_as/index.html) | undefined for signed | — |

The fourth column is the one to notice: these are the rows where the *idea* is language-independent, so the encodings library owns it and all three languages are just spellings. The last two rows are where they genuinely differ — Python's integers do not overflow because they are not machine words, which removes a whole class of bug and a whole class of performance guarantee at the same time.

## Projects, dependencies and pinning

| The idea | Python | Rust |
|---|---|---|
| The manifest | [`pyproject.toml`, `[project]`](02_Projects_and_Environments/pyproject_toml/README.md) | [`Cargo.toml` ↗](https://masiarek.github.io/rust-learning-library/05_Tooling/cargo_dependencies/index.html) |
| The resolved lockfile | `uv.lock` — commit it for an app | [`Cargo.lock` ↗](https://masiarek.github.io/rust-learning-library/05_Tooling/cargo_lock/index.html) — commit it for a binary, not for a library |
| Dev-only dependencies | [`[dependency-groups]`](02_Projects_and_Environments/pyproject_toml/README.md) (PEP 735) | `[dev-dependencies]` — same idea, older |
| Opt-in extras | `[project.optional-dependencies]` | features — and they are **additive**, which is the trap |
| Two versions of one package | impossible in one environment | [allowed, if the majors differ ↗](https://masiarek.github.io/rust-learning-library/05_Tooling/two_versions_of_one_crate/index.html) — and the type from one is not the type from the other |
| Several packages, one resolve | `[tool.uv.workspace]` | [`[workspace]` ↗](https://masiarek.github.io/rust-learning-library/05_Tooling/practice_workspace/index.html) — Cargo had it first; uv borrowed the word |
| Pinning the toolchain itself | `requires-python`, `.python-version` | [`rust-toolchain.toml` ↗](https://masiarek.github.io/rust-learning-library/05_Tooling/pinning_the_toolchain/index.html) — the file the whole team gets |
| Building offline | wheels in a local index | [`cargo vendor` + `[patch]` ↗](https://masiarek.github.io/rust-learning-library/05_Tooling/vendoring_and_patch/index.html) |
| Where a tool keeps its settings | `[tool.<name>]` in the same file | `[package.metadata.<name>]`, or the tool's own file |

Cargo and `uv` look alike because one copied the other, and the vocabulary is worth learning once: *manifest*, *lock*, *workspace*, *feature*. The row that does not translate is the fifth — Python has one version of a package per environment and a conflict is a hard error, while Cargo will happily link two majors of the same crate and let you discover it when a type from one will not go where the other's is expected.

## Where each library goes deeper

- **[Encodings library ↗](https://masiarek.github.io/encodings-learning-library/)** — the subject itself: what a code point is, how UTF-8 encodes one, byte order and the BOM, overlong sequences, mojibake, and the terminal tools (`od`, `xxd`, `iconv`) that show you the bytes. Read it when the question is *what is actually in the file*.
- **[Rust library ↗](https://masiarek.github.io/rust-learning-library/)** — `String` vs `&str`, `char`, slicing by byte, and what the type system buys. Read it when the question is *why won't this compile*.
- **[ABAP library ↗](https://masiarek.github.io/abap-learning-library/)** — the SAP side, where code pages are configuration rather than a literal.
- **This library** — Python's answers, and the places Python's answer is unusual.
