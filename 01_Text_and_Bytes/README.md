# 01_Text_and_Bytes — Python's text model

**Level:** 101 → 301 · for Python programmers

Python 3's defining decision is that text and bytes are different types and it will not convert between them behind your back. Everything in this chapter follows from that one choice: why `len()` gives two answers, why `open()` is a bet, why a Polish name list sorts wrong, and why a filename is not quite a string.

This is the chapter to read first — not because text is the most important part of Python, but because it is the part where a wrong mental model survives longest before failing, and it fails in production on data from someone else's country.

| # | Lesson | The question it answers | Status |
|---|---|---|---|
| 1 | [`str` is not `bytes`](str_is_not_bytes/README.md) | Which type am I holding, and why won't Python mix them? | written |
| 2 | [String literals](string_literals/README.md) | What do the `r`, `b` and `f` prefixes change — and why is `'\d'` two characters? | written |
| 3 | [Encode and decode](encode_and_decode/README.md) | Which direction is which, and what does `errors=` throw away? | written |
| 4 | [Making a `bytes` object](making_a_bytes_object/README.md) | Why is `bytes(5)` five zero bytes and `bytes([5])` one? | written |
| 5 | [`bytearray` is the mutable one](bytearray_is_mutable/README.md) | Which of the two binary types can I write into, and what does mutability cost? | written |
| 6 | [Opening a file](opening_a_file/README.md) | What encoding does `open()` use when I don't say? | stub |
| 7 | [Counting characters](counting_characters/README.md) | How long is this string — and which of the four answers did you want? | written |
| 8 | [Is it a letter?](is_it_a_letter/README.md) | What do the twelve `is*` predicates actually test? | written |
| 9 | [`repr` is not `str`](repr_is_not_str/README.md) | Why is a space "printable" and a tab not — and what did `str(b'x')` just do? | written |
| 10 | [What ends a line](what_ends_a_line/README.md) | Which characters count as a line break — and why do I get three different answers? | written |
| 11 | [`strip` is a set, not a prefix](strip_is_a_set/README.md) | Why did `lstrip('Arthur: ')` eat three more characters than I asked for? | written |
| 12 | [Four ways to find it](finding_a_substring/README.md) | Why did a search that found nothing hand back the last character of my string? | written |
| 13 | [`translate` is a table, keyed by ordinal](translate_is_a_table/README.md) | Why is `maketrans` a separate call, and why is `translate` one pass where three `.replace()` calls are not? | written |
| 14 | [The format mini-language](the_format_mini_language/README.md) | Is `f'{x:>8}'` the same grammar as `'{:>8}'.format(x)` — and where does `%` fit? | written |
| 15 | [Padding is not alignment](padding_is_not_alignment/README.md) | Why is my column still ragged after `ljust(20)` — and why did `zfill` keep the minus sign? | written |
| 16 | [Normalization](normalization/README.md) | Why can `'é' == 'é'` be `False`? | stub |
| 17 | [Sorting is not comparing](sorting_is_not_comparing/README.md) | Why does `sorted()` put `Łukasiewicz` after `Zawadzki`? | written |
| 18 | [Standard in, standard out, and pipes](stdin_stdout_and_pipes/README.md) | Why does printing an emoji work in my terminal and crash in cron? | stub |
| 19 | [Filenames are not text](filenames_are_not_text/README.md) | How does Python read a filename that isn't valid UTF-8? | written |
| 20 | [What kind of file is this?](what_kind_of_file_is_this/README.md) | Which of the five APIs answers the question I actually asked? | written |
| 21 | [The codecs registry](the_codecs_registry/README.md) | What is in the registry that `.encode()` and `.decode()` cannot reach — and why does decoding a stream in chunks differ? | written |

Eight of these pages end with a `## Practice` section — a kata: predict the answer, then run it, then check. They are indexed in [KATAS.md](../KATAS.md), which is also the only place they are put in an order, and that order is not this one: it puts the four `bytes` katas first, because that is the thing this chapter's readers report bouncing off.

## Where this sits relative to the other libraries

The [encodings library ↗](https://masiarek.github.io/encodings-learning-library/) teaches encodings *as a subject*, using four languages to illustrate. This chapter teaches **Python's answer** to that subject — the type boundary, the codec registry, the `errors=` policies, the locale coupling. Where a page here needs the language-agnostic groundwork, it links there rather than repeating it. [The crosswalk](../CROSSWALK.md) is the index of which idea lives where.
