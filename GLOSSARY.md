# Glossary

**Level:** reference · for anyone

Short entries. Each links to the page that explains it properly — a definition here is a pointer, not a substitute.

**bytes** — Python's type for a sequence of numbers 0–255. Indexing one gives an `int`, not a one-byte `bytes`. See [`str` is not `bytes`](01_Text_and_Bytes/str_is_not_bytes/README.md).

**casefold** — `str.casefold()`, a more aggressive `lower()` intended for caseless comparison; it can change a string's length (`ß` → `ss`). See [Normalization](01_Text_and_Bytes/normalization/README.md).

**code point** — the number Unicode assigns to a character, written `U+0141`. What `len()` on a `str` counts. See [Counting characters](01_Text_and_Bytes/counting_characters/README.md).

**codec** — the named conversion between `str` and `bytes` — `utf-8`, `cp1250`, `latin-1`. Python's registry holds around a hundred. See [Encode and decode](01_Text_and_Bytes/encode_and_decode/README.md).

**collation** — ordering text the way a language's alphabet does, as opposed to by code point. See [Sorting is not comparing](01_Text_and_Bytes/sorting_is_not_comparing/README.md).

**errors policy** — the second argument to `.encode()` / `.decode()`, deciding what happens on a character the codec cannot handle: `strict`, `ignore`, `replace`, `backslashreplace`, `surrogateescape`. See [Encode and decode](01_Text_and_Bytes/encode_and_decode/README.md).

**grapheme cluster** — what a reader calls one character, which may be several code points (`👨‍👩‍👧` is five). Not in the standard library. See [Counting characters](01_Text_and_Bytes/counting_characters/README.md).

**mojibake** — text decoded with the wrong codec, so `ó` reads as `Ã³`. See [Encode and decode](01_Text_and_Bytes/encode_and_decode/README.md) and the [encodings library's page ↗](https://masiarek.github.io/encodings-learning-library/03_Encodings/mojibake/index.html) ↗.

**normalization** — rewriting text into a canonical form (NFC, NFD, NFKC, NFKD) so that strings which render identically also compare equal. See [Normalization](01_Text_and_Bytes/normalization/README.md).

**str** — Python's text type, a sequence of code points. Has `.encode()` and no `.decode()`. See [`str` is not `bytes`](01_Text_and_Bytes/str_is_not_bytes/README.md).

**surrogateescape** — the errors policy that smuggles undecodable bytes through a `str` and restores them exactly on re-encode. How Python opens a filename that is not valid UTF-8. See [Filenames are not text](01_Text_and_Bytes/filenames_are_not_text/README.md).
