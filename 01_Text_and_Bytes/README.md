# 01_Text_and_Bytes — Python's text model

**Level:** 101 → 301 · for Python programmers

Python 3's defining decision is that text and bytes are different types and it will not convert between them behind your back. Everything in this chapter follows from that one choice: why `len()` gives two answers, why `open()` is a bet, why a Polish name list sorts wrong, and why a filename is not quite a string.

This is the chapter to read first — not because text is the most important part of Python, but because it is the part where a wrong mental model survives longest before failing, and it fails in production on data from someone else's country.

| # | Lesson | The question it answers | Status |
|---|---|---|---|
| 1 | [`str` is not `bytes`](str_is_not_bytes/README.md) | Which type am I holding, and why won't Python mix them? | written |
| 2 | [Encode and decode](encode_and_decode/README.md) | Which direction is which, and what does `errors=` throw away? | written |
| 3 | [Opening a file](opening_a_file/README.md) | What encoding does `open()` use when I don't say? | stub |
| 4 | [Counting characters](counting_characters/README.md) | How long is this string — and which of the four answers did you want? | written |
| 5 | [Normalization](normalization/README.md) | Why can `'é' == 'é'` be `False`? | stub |
| 6 | [Sorting is not comparing](sorting_is_not_comparing/README.md) | Why does `sorted()` put `Łukasiewicz` after `Zawadzki`? | written |
| 7 | [Standard in, standard out, and pipes](stdin_stdout_and_pipes/README.md) | Why does printing an emoji work in my terminal and crash in cron? | stub |
| 8 | [Filenames are not text](filenames_are_not_text/README.md) | How does Python read a filename that isn't valid UTF-8? | stub |

## Where this sits relative to the other libraries

The [encodings library ↗](https://masiarek.github.io/encodings-learning-library/) ↗ teaches encodings *as a subject*, using four languages to illustrate. This chapter teaches **Python's answer** to that subject — the type boundary, the codec registry, the `errors=` policies, the locale coupling. Where a page here needs the language-agnostic groundwork, it links there rather than repeating it. [The crosswalk](../CROSSWALK.md) is the index of which idea lives where.
