# Resources

**Level:** reference · for anyone

External material worth your time, by what it is good for. Everything here is somebody else's work — this library links to it and does not reproduce it. Where a page here was prompted by one of these, the page says so and the code and prose are written from scratch.

## The primary sources

- [Unicode Standard ↗](https://www.unicode.org/versions/latest/) — the actual thing. Chapter 3 (Conformance) is the one with the rules.
- [UTS #10: Unicode Collation Algorithm ↗](https://unicode.org/reports/tr10/) — what correct alphabetical ordering means. Behind [Sorting is not comparing](01_Text_and_Bytes/sorting_is_not_comparing/README.md).
- [UAX #29: Text Segmentation ↗](https://unicode.org/reports/tr29/) — where a "character" begins and ends, for a reader. Behind [Counting characters](01_Text_and_Bytes/counting_characters/README.md).
- [UAX #15: Normalization Forms ↗](https://unicode.org/reports/tr15/) — NFC, NFD, NFKC, NFKD.

## Python's own documentation

- [Unicode HOWTO ↗](https://docs.python.org/3/howto/unicode.html) — the best free single document on this subject. Short, official, current.
- [`codecs` — standard encodings ↗](https://docs.python.org/3/library/codecs.html#standard-encodings) — the full list of codec names, and the error-handler table.
- [`string` — Common string operations ↗](https://docs.python.org/3/library/string.html) — the constants, `capwords`, `Template` and `Formatter`, plus the format-string grammar, which lives here rather than with `str`. Behind [The `string` module](01_Text_and_Bytes/the_string_module/README.md).
- [`codecs` ↗](https://docs.python.org/3/library/codecs.html) — the module itself: the registry, `getincrementaldecoder`, and `register_error`. Behind [The codecs registry](01_Text_and_Bytes/the_codecs_registry/README.md).
- [PEP 293 ↗](https://peps.python.org/pep-0293/) — codec error handling callbacks, which is what makes the handler list extensible.
- [`unicodedata` ↗](https://docs.python.org/3/library/unicodedata.html) — `normalize`, `combining`, `category`, `name`.
- [PEP 383 ↗](https://peps.python.org/pep-0383/) — `surrogateescape`, and the filename problem it was invented for.
- [PEP 686 ↗](https://peps.python.org/pep-0686/) — making UTF-8 mode the default, and what it changes.
- [PEP 540 ↗](https://peps.python.org/pep-0540/) — UTF-8 mode itself.

## Real Python

Subscription material, and good. Cited here as sources rather than summarized:

- [Unicode & Character Encodings in Python: A Painless Guide ↗](https://realpython.com/python-encodings-guide/) — Brad Solomon. The broad tour, Python-centric. Overlaps chapter 1 here and goes wider on number systems and string literals.
- [How to Sort Unicode Strings Alphabetically in Python ↗](https://realpython.com/python-sort-unicode-strings/) — Bartosz Zaczyński. The article that prompted [Sorting is not comparing](01_Text_and_Bytes/sorting_is_not_comparing/README.md); it goes further than that page does, into transliteration, natural sort order and multi-key sorting.
- [Python Project: Build a Word Count Command-Line App ↗](https://realpython.com/courses/word-count-app-project/) — Bartosz Zaczyński. The course whose non-ASCII lesson prompted [Counting characters](01_Text_and_Bytes/counting_characters/README.md).

## Other languages' FAQs

Old, free, and written by people who had already met the problem. Cited as sources; nothing is run and nothing is copied.

- [perlfaq5 — Files and Formats ↗](https://perldoc.perl.org/perlfaq5) — forty-two questions about file I/O, and the source of four of the six sections in [Opening a file](01_Text_and_Bytes/opening_a_file/README.md): flushing an output handle, counting the lines in a file, why opening read-write wipes it out, and renaming a file reliably. The topics transfer; the Perl does not, and none of it is reproduced here. Its companion [perlpacktut ↗](https://perldoc.perl.org/perlpacktut) is still on [the backlog](TODO.md) as the `struct` / `to_be_bytes` / fixed-width-field page.
## Microsoft's .NET documentation

Free, and worth reading even if you never write C#, because .NET names distinctions Python leaves implicit. Cited as sources; nothing here is reproduced.

- [Best practices for using strings in .NET ↗](https://learn.microsoft.com/en-us/dotnet/standard/base-types/best-practices-strings) — the article that prompted [Comparison has a mode](01_Text_and_Bytes/comparison_has_a_mode/README.md). Its structural idea is that every string API should take an explicit `StringComparison`; its sharpest detail is that culture-sensitive comparison ignores embedded NUL characters. **Neither is machine-checked here** — CI runs no .NET — and the Python behaviour on the same pair was measured on that page rather than assumed.
- [Character encoding in .NET ↗](https://learn.microsoft.com/en-us/dotnet/standard/base-types/character-encoding-introduction) — read alongside it. `System.String` is UTF-16, so .NET's "character" is a code *unit* and its surrogate handling is visible in a way Python's is not.
- [Encoding overview ↗](https://learn.microsoft.com/en-us/globalization/encoding/encoding-overview) and [best practices for displaying data ↗](https://learn.microsoft.com/en-us/dotnet/standard/base-types/best-practices-display-data) — the wider pair, filed in [TODO.md](TODO.md) as reference rather than as pages.

## macOS specifics

The two pages behind [Filenames are not text](01_Text_and_Bytes/filenames_are_not_text/README.md)'s macOS half. Both are about the *terminal*, not about Python, and neither is the source of a number on that page — every measurement there was re-run on 2026-09-06 against Linux, because both pages predate APFS.

- [Display high-bit characters in Terminal on Mac ↗](https://support.apple.com/guide/terminal/display-high-bit-characters-trmlxxx/mac) — Apple. The Terminal profile's text-encoding menu and its "set locale environment variables on startup" checkbox. Read it for what the three settings *are*; the advice to change them is for a world that is no longer the default.
- [Terminal Primer – Part 3 – Special Characters ↗](https://scriptingosx.com/2017/08/special-characters/) — Armin Briegel. Shell quoting and escaping, not encodings — but it is where the Finder `/` ↔ shell `:` swap is best explained. Written for `bash` in 2017; its `!` and single-quote rules do not hold in `fish`.

## Talks

- Ned Batchelder, [Pragmatic Unicode ↗](https://nedbatchelder.com/text/unipain.html) — the "unipain" talk. Still the clearest statement of the boundary discipline, and the source of the *encode on the way out, decode on the way in* framing.
- Bob Steagall, [Fast Conversion From UTF-8 ↗](https://www.youtube.com/watch?v=5FQ87-Ecb-A) — CppCon 2018. Not Python, but the clearest visual account of how UTF-8 decoding actually works.

## The sibling libraries

- [Encodings ↗](https://masiarek.github.io/encodings-learning-library/) · [Rust ↗](https://masiarek.github.io/rust-learning-library/) · [ABAP ↗](https://masiarek.github.io/abap-learning-library/) — see [the crosswalk](CROSSWALK.md).
