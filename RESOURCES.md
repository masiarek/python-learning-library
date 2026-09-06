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
- [`unicodedata` ↗](https://docs.python.org/3/library/unicodedata.html) — `normalize`, `combining`, `category`, `name`.
- [PEP 383 ↗](https://peps.python.org/pep-0383/) — `surrogateescape`, and the filename problem it was invented for.
- [PEP 686 ↗](https://peps.python.org/pep-0686/) — making UTF-8 mode the default, and what it changes.
- [PEP 540 ↗](https://peps.python.org/pep-0540/) — UTF-8 mode itself.

## Real Python

Subscription material, and good. Cited here as sources rather than summarized:

- [Unicode & Character Encodings in Python: A Painless Guide ↗](https://realpython.com/python-encodings-guide/) — Brad Solomon. The broad tour, Python-centric. Overlaps chapter 1 here and goes wider on number systems and string literals.
- [How to Sort Unicode Strings Alphabetically in Python ↗](https://realpython.com/python-sort-unicode-strings/) — Bartosz Zaczyński. The article that prompted [Sorting is not comparing](01_Text_and_Bytes/sorting_is_not_comparing/README.md); it goes further than that page does, into transliteration, natural sort order and multi-key sorting.
- [Build a Word Count Command-Line App ↗](https://realpython.com/courses/python-project-word-count/) — the course whose non-ASCII lesson prompted [Counting characters](01_Text_and_Bytes/counting_characters/README.md).

## Talks

- Ned Batchelder, [Pragmatic Unicode ↗](https://nedbatchelder.com/text/unipain.html) — the "unipain" talk. Still the clearest statement of the boundary discipline, and the source of the *encode on the way out, decode on the way in* framing.
- Bob Steagall, [Fast Conversion From UTF-8 ↗](https://www.youtube.com/watch?v=5FQ87-Ecb-A) — CppCon 2018. Not Python, but the clearest visual account of how UTF-8 decoding actually works.

## The sibling libraries

- [Encodings ↗](https://masiarek.github.io/encodings-learning-library/) · [Rust ↗](https://masiarek.github.io/rust-learning-library/) · [ABAP ↗](https://masiarek.github.io/abap-learning-library/) — see [the crosswalk](CROSSWALK.md).
