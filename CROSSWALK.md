# The crosswalk

**Level:** reference · for anyone using more than one of these libraries

**One line:** One idea per row, and what each language does with it — so a concept you already understand in ABAP or Rust can be looked up rather than relearned.

These libraries were written separately and overlap on purpose: text handling is the place where a working programmer meets the same problem in every language and gets a different answer each time. This page is the index across them. It states the *idea* once, then names what each language calls it, so you can start from the column you already know.

A cell in the Python column links into this library. A cell in another column links into that library, or names the API when there is no page for it yet.

## Text and bytes

| The idea | Python | Rust | C | ABAP |
|---|---|---|---|---|
| Text vs. raw bytes as separate types | [`str` / `bytes`](01_Text_and_Bytes/str_is_not_bytes/README.md) | [`String` / `Vec<u8>` ↗](https://masiarek.github.io/rust-learning-library/14_Strings/anatomy_of_a_string/index.html) | no distinction — `char *` is both | `string` / `xstring` |
| Converting between them | [`.encode()` / `.decode()`](01_Text_and_Bytes/encode_and_decode/README.md) | `String::from_utf8` / `.as_bytes()` | hand-rolled, or `iconv` | `cl_abap_conv_codepage` |
| What happens on invalid input | `UnicodeDecodeError`, or an `errors=` policy | `from_utf8` returns `Result`; `from_utf8_lossy` substitutes | undefined — nothing checks | exception, or a replacement char |
| The "never fails" escape hatch | `errors="surrogateescape"` | none in std — the type will not hold it | — | — |
| Guaranteed-valid text type | `str` (code points, may hold lone surrogates) | `String` (UTF-8, enforced by the type) | — | `string` (UTF-16 internally) |

The sharpest difference is the third row. Rust makes invalid UTF-8 *unrepresentable* in a `String`, so the check happens once at the boundary and never again. Python checks at the boundary too but leaves you a way through it (`surrogateescape`), because a filename has to be openable even when it is not text. C checks nowhere. Which of those is right depends entirely on whether your program can refuse its input.

## Length and indexing

| The idea | Python | Rust | ABAP |
|---|---|---|---|
| Length in bytes | `len(s.encode("utf-8"))` | `s.len()` — bytes, always | `xstrlen( )` |
| Length in UTF-16 units | `len(s.encode("utf-16-le")) // 2` | [`s.encode_utf16().count()` ↗](https://masiarek.github.io/rust-learning-library/14_Strings/four_lengths/index.html) | `strlen( )` — this is ABAP's default |
| Length in code points | [`len(s)`](01_Text_and_Bytes/counting_characters/README.md) | [`s.chars().count()` ↗](https://masiarek.github.io/rust-learning-library/14_Strings/meet_the_char/index.html) | — (`strlen( )` counts UTF-16 units) |
| Length a reader would agree with | not in the stdlib | not in std — needs a crate | — |
| Indexing by position | `s[0]` gives a 1-char `str` | [`s[0]` does not compile](https://masiarek.github.io/rust-learning-library/14_Strings/string_slices/index.html) ↗ | `s(0)` gives a code unit |

Rust's refusal to index a string by integer is the design decision that most annoys newcomers and most reliably prevents the bug: `s[0..1]` on a multi-byte character *panics* rather than returning half a character. Python returns a whole code point, which is right more often than C and still not the same as a character. ABAP returns a UTF-16 code unit, so an emoji is two.

## Ordering and comparison

| The idea | Python | Rust | ABAP |
|---|---|---|---|
| Default sort order | [code point](01_Text_and_Bytes/sorting_is_not_comparing/README.md) | [code point (`Ord` on `str`) ↗](https://masiarek.github.io/rust-learning-library/14_Strings/comparing_strings/index.html) | UTF-16 code unit |
| Alphabetical for a real language | `locale.strxfrm`, or ICU | needs a crate | collation-aware compare, or a sort key column |
| Same-looking strings comparing unequal | [normalization](01_Text_and_Bytes/normalization/README.md) | same problem, same fix | same problem |
| Case-insensitive comparison | `str.casefold()` | `str::to_lowercase` (locale-independent) | `TRANSLATE ... TO UPPER CASE` |

All three languages get this equally wrong by default, and for the same reason: code-point order is the only ordering available without a locale database. This is the one row where "Python's answer" is not really Python's — it is everyone's.

## Classifying a character

| The idea | Python | Rust | ABAP |
|---|---|---|---|
| Is it a letter? | [`str.isalpha()`](01_Text_and_Bytes/is_it_a_letter/README.md) — General_Category `L*` | [`char::is_alphabetic` ↗](https://masiarek.github.io/rust-learning-library/14_Strings/meet_the_char/index.html) — the Alphabetic *property*, which is wider | `CO` against a character set, by hand |
| Is it a digit you can `int()`? | `str.isdecimal()` — `Nd` | `char::to_digit(10).is_some()` — ASCII only | `CO '0123456789'` |
| Is it a number of any kind? | `str.isnumeric()` — Numeric_Type, so `一` counts | `char::is_numeric` — `N*` categories, so `一` does not | — |
| Whitespace | `str.isspace()` — Unicode, plus `\x1c`–`\x1f` | [`char::is_whitespace` ↗](https://masiarek.github.io/rust-learning-library/14_Strings/rfc_1054_str_words/index.html) — `White_Space` only | `cl_abap_char_utilities` constants |
| Whole-string version | 12 methods on `str`; the ten class predicates also mean "…and not empty" | only three (`is_empty`, `is_ascii`, `is_char_boundary`) — you write `.chars().all(…)` | `CO` is already whole-field |
| The empty string | `False` for the ten class predicates | `true` — `all()` over nothing | worth checking on your system |

This is the one section where the *names* match and the *sets* do not, in both directions: Rust's `is_alphabetic` accepts combining marks that Python's `isalpha` rejects, and Python's `isnumeric` accepts a CJK ideograph that Rust's `is_numeric` rejects. The measured grid is on [Is it a letter?](01_Text_and_Bytes/is_it_a_letter/README.md). The general form of the hazard — every one of these is a table lookup whose answer depends on which edition of the table your toolchain was built against — is [the table has a version ↗](https://masiarek.github.io/encodings-learning-library/02_Characters/the_table_has_a_version/index.html).

## Where each library goes deeper

- **[Encodings library ↗](https://masiarek.github.io/encodings-learning-library/)** — the subject itself: what a code point is, how UTF-8 encodes one, byte order and the BOM, overlong sequences, mojibake, and the terminal tools (`od`, `xxd`, `iconv`) that show you the bytes. Read it when the question is *what is actually in the file*.
- **[Rust library ↗](https://masiarek.github.io/rust-learning-library/)** — `String` vs `&str`, `char`, slicing by byte, and what the type system buys. Read it when the question is *why won't this compile*.
- **[ABAP library ↗](https://masiarek.github.io/abap-learning-library/)** — the SAP side, where code pages are configuration rather than a literal.
- **This library** — Python's answers, and the places Python's answer is unusual.
