# What to write next — the questions backlog

**Level:** reference · for whoever is about to write a page

**One line:** Forty-odd questions Adam asked while reading the Python docs, each routed to the page that answers it, the page that half-answers it, or the page that does not exist yet — because "we should cover formatting" is not a plan and "these eight questions are one page" is.

## How to read this page

Three things before you use it.

**This is a backlog, not teaching text.** Every other page here carries a claim that a program checked ([CONTRIBUTING.md](CONTRIBUTING.md)). Nothing in the **Hook** column has been through that. A hook is *a claim to verify when the page is written*, not a fact this library has established. Expect roughly one in three to come out differently once a program is pointed at it — which is the reason to point a program at it. The handful marked **measured** were run on 2026-09-07 against Python 3.14.7 while this page was being written, and are quoted so the "do these first" ranking rests on something.

**The `#` column is Adam's own numbering**, kept so a question can be found again in the message it came from. It has two collisions — two items numbered `20` and two numbered `35` — left as they arrived rather than silently renumbered.

**Status means one of five things:**

| Status | Meaning |
|---|---|
| **written** | A page here answers it. The row links the page; nothing to do. |
| **partly** | A page here touches it and stops short. The row says where the gap is. |
| **gap** | Nothing here answers it. This is the backlog proper. |
| **sibling** | The answer belongs in another library ([encodings ↗](https://masiarek.github.io/encodings-learning-library/), [Rust ↗](https://masiarek.github.io/rust-learning-library/)) under the rule in [CONTRIBUTING.md](CONTRIBUTING.md) — the library that owns the *subject* owns the page. |
| **answer here** | A yes/no question that does not need a page. Answered in this file and closed. |

---

## Do these five first

Ranked by how many of the questions below one page closes, and by whether the page has a *surprise* in it — a measured result that contradicts the obvious reading. A page with no surprise is a docs restatement, and the docs are already written.

| | Page to write | Closes | Why this one |
|---|---|---|---|
| **1** | **[The format mini-language](01_Text_and_Bytes/the_format_mini_language/README.md)** — **written 2026-09-07** | #2 #4 #5 #6 #19 #20a #29 #31, and the two C# tutorials in the tail | Eight questions, one grammar. The biggest single gap in the library, and [the crosswalk](CROSSWALK.md) already says so in print: *"the method-by-method tour is one of the gaps this page is meant to make visible."* The surprise is #19 — **formatting an integer with `'{:n}'` temporarily changes a process-global locale setting, and the docs say outright that this affects other threads.** A data race inside a formatting call |
| **2** | **[String literals](01_Text_and_Bytes/string_literals/README.md)** — **written 2026-09-07** | #3 #32, the escape-table item and the `U+` vs `0x` item in the tail | The foundation the format page stands on, and nothing in either library covers Python's literal *syntax* — [writing a code point ↗](https://masiarek.github.io/encodings-learning-library/02_Characters/writing_a_code_point/index.html) covers the escapes, not the prefixes. The surprise is a contrast Adam's own source hands us: **C#'s `\x` is variable-length and eats following hex digits — `\xA1A` is one character, not two — where Python's `\x` is exactly two digits and `\xA1A` is `¡A`.** Same escape, two grammars, and one of them has a documented warning attached |
| **3** | **[`repr` is not `str`](01_Text_and_Bytes/repr_is_not_str/README.md)** — **written 2026-09-07** | #1 #15 #30 | Adam's *first* question, and it cannot be answered without this page: "printable" in Python does not mean "makes ink" — it means **`repr()` will not hex-escape it**, which is why `str.isprintable()` says `' '` is printable and `'\t'` is not. Measured: `string.printable.isprintable()` is **`False`**, and the docs say that is by design. Also lands `str(b'Zoot!')` → `"b'Zoot!'"`, the quietest bug in the language |
| **4** | **[`strip` is a set, not a prefix](01_Text_and_Bytes/strip_is_a_set/README.md)** — **written 2026-09-07** | #12 #26 | The one item in the list that is a *bug people ship*. Measured: `'Arthur: three!'.lstrip('Arthur: ')` is **`'ee!'`** — the argument is a character set, so it ate the `thr` — while `.removeprefix('Arthur: ')` is `'three!'`. One program, one table, and the Rust contrast is sharp: `trim_start_matches` takes a pattern, `strip_prefix` returns an `Option` |
| **5** | **A drilling mechanism — katas or a deck** | #4 #33 #35b, and the C# challenge in the tail | Not a topic. Adam asked for this **three times** in one message, and once with a reason: *"still struggle with the bytes concept — not sure how to hammer this."* This library has no exercise mechanism at all; the [Rust library ↗](https://masiarek.github.io/rust-learning-library/) already has compile-verified Anki decks generated from source, so the pattern exists and the tooling is worth copying rather than inventing. Decide the shape before writing any content: a deck, a `katas/` folder with a checker, or `## Try it` sections that graduate into one |

**Progress, 2026-09-07.** Pages 1, 2, 3 and 4 have landed. Closed: #1, #2, #3, #5, #6, #12, #15, #19, #20a, #26, #29, #30, #31, #32 and the two unnumbered escape-table items — sixteen of the forty, in four pages, which is the point of grouping them. **One to go: the drilling mechanism**, which is infrastructure rather than a page and needs a shape decided before any content is written.

**Why not the method tour first.** #9 #10 #13 #14 #17 #18 #24 #27 #34 #36 #37 are ten questions about individual `str` methods, and they are worth one chapter — but they are worth it *after* the four pages above, because most of them are one paragraph each and a chapter of paragraphs is a docs mirror. The shape that earns its place is a small number of pages each built around a method that **does not do what its name says**: `strip` (a set), `find` (returns `-1`, and you probably wanted `in`), `translate` (a `dict` keyed by ordinals, which is why `maketrans` exists), `zfill` (sign-aware, and only for ASCII `0`). That is a page each, not a method each. Two of the four have landed: [`strip` is a set](01_Text_and_Bytes/strip_is_a_set/README.md) and [`translate` is a table](01_Text_and_Bytes/translate_is_a_table/README.md).

---

## Formatting — the biggest gap

Nothing in this library covers `str.format`, f-strings, or `%`. Eight of Adam's questions live here, and they are one grammar asked eight ways.

| # | The question | Status | Hook to verify |
|---|---|---|---|
| 2 | Does it make sense to teach [format string syntax ↗](https://docs.python.org/3/library/string.html#format-string-syntax)? | **written** — [The format mini-language](01_Text_and_Bytes/the_format_mini_language/README.md) | Yes — because it is the same mini-language in four places (`str.format`, f-strings, `format()`, `__format__`) and *not* the same as `%`. Rust's [`format!` ↗](https://masiarek.github.io/rust-learning-library/14_Strings/the_format_language/index.html) borrowed the grammar, which makes it the best crosswalk row in the chapter |
| 4 | [Format spec ↗](https://docs.python.org/3/library/string.html#formatspec) as katas or Anki — is there a page? | **half** | There is [a page](01_Text_and_Bytes/the_format_mini_language/README.md) now; there is still no mechanism. See row 5 of the five above. The spec is `[[fill]align][sign][z][#][0][width][grouping][.precision][type]` — nine independent slots, which is exactly the shape drilling is for |
| 5 | Explain the 3.1/3.4 change: `'{} {}'` vs `'{0} {1}'`; and `!s` `!r` `!a` | **written** — conversion flags on [`repr` is not `str`](01_Text_and_Bytes/repr_is_not_str/README.md) §6, numbering on [the format page](01_Text_and_Bytes/the_format_mini_language/README.md) §3 | Auto-numbering and manual numbering **cannot be mixed** — `'{} {0}'.format(a, b)` raises `ValueError`. That is the fact the changelog note leaves out, and it is the one that bites. The three conversion flags belong on the `repr` page instead |
| 6 | [PEP 682 ↗](https://peps.python.org/pep-0682/) negative zero, and the [SO answer ↗](https://stackoverflow.com/questions/11010683/how-to-have-negative-zero-always-formatted-as-positive-zero-in-a-python-string/36604981) — how does Rust deal with it? | **written** — and the answer is that **Rust has the same bug and no `z` option**: `format!("{:.0}", -0.4)` is `-0` too. Measured | **Measured:** `format(-0.001, '.2f')` is `'-0.00'` — a number that is not negative, displayed as negative, because rounding happened after the sign. `format(-0.001, 'z.2f')` is `'0.00'`; the `z` option is 3.11+. Verify what Rust prints for the same value, and whether it has any equivalent (expected: no — you round first) |
| 19 | The `n` type temporarily sets `LC_CTYPE` to `LC_NUMERIC`, "affects other threads" — what is this? | **written** — [§5](01_Text_and_Bytes/the_format_mini_language/README.md) | The best hook in the whole backlog: **a formatting call that mutates process-global state.** It only fires when the separators are non-ASCII or multi-byte *and* the two locale categories differ, which is why nobody meets it until they do. Pairs with [locale and `LC_CTYPE` ↗](https://masiarek.github.io/encodings-learning-library/06_Terminal/locale_and_lc_ctype/index.html) in the encodings library. **Measured under `LC_ALL=C`:** `format(1234, 'n')` is `'1234'` — the example is inert until a locale exists, which is itself the lesson and the reason this example must print its own locale |
| 20a | Why is `format_map` useful? | **written** — [§6](01_Text_and_Bytes/the_format_mini_language/README.md) | Because `format(**m)` *copies* into a `dict` and `format_map` does not — so a `dict` subclass with `__missing__` survives. One paragraph on the format page, not a page |
| 29 | The debug specifier `f'{number=}'` | **written** — [`repr` is not `str`](01_Text_and_Bytes/repr_is_not_str/README.md) §6 | **Measured:** `f'{n=}'` is `'n=14.3'`, and whitespace inside the braces is preserved verbatim — `f'{ n  -  4  = }'` keeps every space. It also silently switches the default conversion to `repr()`, which is why it belongs half here and half on the `repr` page |
| 31 | Anything to learn from [printf-style formatting ↗](https://docs.python.org/3/library/stdtypes.html#printf-style-string-formatting)? | **written** — [§7](01_Text_and_Bytes/the_format_mini_language/README.md) | Yes, two things. `'%s' % x` is **not** a function call — it is one operator with one right operand, so a tuple is unpacked and a bare tuple must be wrapped, which is the classic `TypeError: not all arguments converted`. And `%` is the only one of the four that works on `bytes` (since 3.5, [PEP 461 ↗](https://peps.python.org/pep-0461/)) — the reason it cannot be retired |

**Also here, from the unnumbered tail:** the [C# string interpolation tutorial ↗](https://learn.microsoft.com/en-us/dotnet/csharp/fundamentals/tutorials/string-interpolation) and its `{0,-20}` alignment example are the same grammar with the alignment written *inside* the field rather than before the type — a good crosswalk row, and the `ljust`/`rjust` question (#10) is really "why does a language have both a method and a format spec for this?"

---

## Literals — the other gap with no page

| # | The question | Status | Hook to verify |
|---|---|---|---|
| 3 | What are string literals — is there a page? | **written** | [String literals](01_Text_and_Bytes/string_literals/README.md). The nearest before it was [writing a code point ↗](https://masiarek.github.io/encodings-learning-library/02_Characters/writing_a_code_point/index.html), which covers escapes across four languages but not Python's *prefix* system. The page to write is the prefix grid — `r` `b` `f` `rb` `br` `fr`, what each disables, and the two that cannot combine (`bf` does not exist, and there is no such thing as an f-bytes literal) |
| 32 | Bytes literals and raw literals — how do other languages do it? | **written** — and Python's raw string turns out to be the *weaker* one: `r"C:\Users\"` compiles in Rust and not here | Three facts worth a table: a bytes literal may contain only ASCII *regardless of the source encoding*; a raw literal cannot end in an odd number of backslashes, so `r"\"` is a syntax error while `r"\""` is two characters; and `\0` in Python is octal, not a special case. Rust's `r#"…"#` solves the trailing-backslash problem the other way, with counted hashes |
| — | The escape table from the .NET docs, and *"I thought Unicode starts with `U+` but here is an example with `0x`"* | **written** — [§2 and §3](01_Text_and_Bytes/string_literals/README.md) | Two separate answers, both short. `U+00E9` is a **code point name**; `0x00E9` is an **integer literal** that happens to equal it; `é` is a **source-code escape**. Same number, three notations, three jobs — the encodings library makes exactly this point and this page should link it rather than repeat it. And the sharp contrast is the .NET warning itself: **C#'s `\x` takes one to four hex digits and keeps eating**, so `\xA1A` is `ਚ` (`U+0A1A`) and not `¡A`, while Python's `\x` is exactly two digits and `'\xA1A'` is `'¡A'`. **Measured.** A language that made the escape variable-length had to document a footgun; a language that fixed the width did not |
| — | [C++ string and character literals ↗](https://learn.microsoft.com/en-us/cpp/cpp/string-and-character-literals-cpp) — how good or bad is C++ here? | **partly** | C is now a column on [String literals](01_Text_and_Bytes/string_literals/README.md) and in [the crosswalk](CROSSWALK.md); C++ is still only prose. Worth one more row: C++ has `u8` `u` `U` `L` `R` prefixes *and* `char8_t`/`char16_t`/`char32_t`/`wchar_t`, so the prefix says the element type as well as the encoding — which is more information than Python's prefixes carry and more decisions than most callers want |

---

## Character classification — mostly answered already

Seven of Adam's questions are already on one page. [Is it a letter?](01_Text_and_Bytes/is_it_a_letter/README.md) covers all twelve `is*` predicates, the empty-string split, the Rust column and the `bytes` column.

| # | The question | Status |
|---|---|---|
| 7 | Why is `isdecimal` useful, does Rust have it, how does it differ from `isdigit`? | **written** — [Is it a letter?](01_Text_and_Bytes/is_it_a_letter/README.md) §3 and §"Three kinds of number". `int()` accepts `isdecimal` and nothing wider; Rust's `char::is_digit` takes a radix and is ASCII-only, so it is a false friend |
| 8 | Why is `islower` useful — what are cased characters? | **written** — §5. `'ABC1'.isupper()` is `True` because a digit has no case to disagree with; `ǅ` is titlecase and neither |
| 20b | `isalnum` vs other languages | **written** — §4. It is the union of **four** predicates, not two, which is why `½` is alphanumeric |
| 21 | `isalpha` vs other languages | **written** — §2, plus the measured Rust grid: `is_alphabetic` is the Alphabetic *property*, `isalpha` is the `L*` *categories*, and they disagree in both directions |
| 22 | `isascii` — why still useful with UTF-8? | **written** — §1. It is one of the only two that are `True` on the empty string. The "why useful" answer to add if the page is ever revisited: it is the cheap gate before an expensive Unicode-aware path |
| 23 | `isspace` — compare to other languages | **written** — §1 and §7, plus [what ends a line](01_Text_and_Bytes/what_ends_a_line/README.md). Python counts `U+001C`–`U+001F` as whitespace and Rust's `White_Space` property does not |
| 1 | `isprintable` / `string.printable` — how can you print whitespace? | **written** — [`repr` is not `str`](01_Text_and_Bytes/repr_is_not_str/README.md). "Printable" means `repr()` will not escape it, which is why `U+0020` is the one printable separator in Unicode and every other space character is not |

---

## `str` and `bytes` — the pages exist; the drilling does not

| # | The question | Status | Hook to verify |
|---|---|---|---|
| 16 | `str.encode` — is there a page? | **written** | [Encode and decode](01_Text_and_Bytes/encode_and_decode/README.md), including every `errors=` handler and `surrogateescape` |
| 33 | *"Still struggle with the bytes concept — maybe katas, anki"* | **written pages, gap in practice** | Three pages already: [`str` is not `bytes`](01_Text_and_Bytes/str_is_not_bytes/README.md), [making a `bytes` object](01_Text_and_Bytes/making_a_bytes_object/README.md), [`bytearray` is the mutable one](01_Text_and_Bytes/bytearray_is_mutable/README.md). If the concept still will not stick after three pages, the missing thing is **repetition, not exposition** — which is why this is row 5 of the five above and not a fourth page |
| 15 | The four `str()` signatures — is there a page? | **written** | [`repr` is not `str`](01_Text_and_Bytes/repr_is_not_str/README.md) §5. `str(b'Zoot!')` is `"b'Zoot!'"` — **measured** — a five-character bytes object silently becoming an eight-character string with quotes in it. Python has a whole command-line flag (`-b`) to make it a warning, which is the strongest possible admission that it is a trap |
| 9 | `join` raises `TypeError` on `bytes` — show it, and compare Rust, C, ABAP | **partly** | The boundary is on [`str` is not `bytes`](01_Text_and_Bytes/str_is_not_bytes/README.md); this specific error is not. Note the asymmetry worth measuring: `b', '.join([b'a', b'b'])` works fine, so `join` is not "string only" — it is "the separator's own type only", and mixing is what fails |
| 35a | *"Is it correct?"* — the Unicode-vs-bytes summary from the Google exercises | **answer here** | Substantially yes. Two nits: *"regular Python strings are unicode"* is true but the useful phrasing is that a `str` is a sequence of **code points**, not of characters ([counting characters](01_Text_and_Bytes/counting_characters/README.md) is the page); and *"various libraries such as regular expressions work correctly if passed either type"* is the one to distrust — `re` accepts both and **changes what `\w` and `\d` mean** depending which it got. That is not "works correctly if passed either", it is two different engines behind one API |

---

## The method tour — ten questions, worth four pages

Nothing here covers these. The recommendation above is to group them, not to write one page per method.

| # | Method | Status | Hook to verify |
|---|---|---|---|
| 12, 26 | `lstrip` / `strip` / `removeprefix` | **written** | [`strip` is a set, not a prefix](01_Text_and_Bytes/strip_is_a_set/README.md) — three differences, not one, and only one filename in four survives `rstrip('.txt')` |
| 13, 27 | `maketrans` / `translate` | **written** | [`translate` is a table, keyed by ordinal](01_Text_and_Bytes/translate_is_a_table/README.md) — all four hooks held. The table is a `dict` of ints on **both** sides, a value may be a string of any length or `None`, and any object answering `__getitem__` is a table, so a `dict` subclass with `__missing__` is a whitelist filter in one pass. Two things the hook did not predict: the practical reason to use it is that the substitution is **one pass**, which chained `.replace()` is not — `html.escape` in the stdlib carries a comment saying its first line must go first — and `'abc'.translate('xyz')` is a **silent no-op**, because a `str` is a legal table whose `IndexError` means "leave it alone" |
| 18, 36 | `find` vs `index` vs `in` | **gap** | The docs note is the lesson: *use `find` only if you need the position.* `-1` is a valid index in Python, so `if s.find(x):` and `if s.find(x) > -1:` are both wrong in different ways — the first is `False` at position 0, the second is fine. Rust returns `Option<usize>` and a **byte** offset, so the same bug will not compile and a different one can |
| 24 | `partition` / `rpartition` | **gap** | They always return a 3-tuple, so the unpack never raises — the failure shows up as an empty separator field. **Measured:** `'Monty Python'.rpartition('-')` is `('', '', 'Monty Python')` and `partition` puts the whole string *first* instead. The two failure shapes are mirror images, and picking the wrong one silently moves your data |
| 10 | `ljust` / `rjust` | **gap** | Two things: the original is returned unchanged when it is already too long — **it never truncates** — and the padding is counted in **code points**, so a column of names is aligned only if every character is one column wide. `'Łódź'.ljust(10)` and `'日本'.ljust(10)` are both length 10 and only one of them lines up |
| 14 | `zfill` | **gap** | Sign-aware: `'-42'.zfill(5)` is `'-0042'`, not `'00-42'`. **Measured**, and `'+4'.zfill(5)` is `'+0004'`. It is `'{:05d}'.format` for strings, and the format spec's `0` does the same thing — another "why are there two ways" row for the format page |
| 17 | `expandtabs` | **gap** | It is **column arithmetic, not replacement** — a tab becomes however many spaces reach the next stop, so the output depends on what came before it on the line. **Measured:** `'01\t012\t0123'.expandtabs(4)` is `'01  012 0123'` — two spaces then one. And it counts *characters*, so it gets a wide-character column wrong for the same reason `ljust` does |
| 34, 36 | Slicing, negative indices, `s[:n] + s[n:] == s` | **gap** | The invariant is worth stating and testing over out-of-range and negative `n`. The Rust contrast is the sharpest in the language: `&s[0..1]` on `"é"` **panics at runtime**, because Rust slices by byte and enforces the char boundary — [slicing by byte ↗](https://masiarek.github.io/encodings-learning-library/05_Rust/slicing_by_byte/index.html) owns it |
| 25 | `splitlines` vs `split('\n')` | **written** | [What ends a line](01_Text_and_Bytes/what_ends_a_line/README.md) — ten boundaries, scanned out of the whole code space, and the three-answer table |
| 11 | `lower()` and Default Case Folding — is there a page? | **gap** | And there is a docs bug to check here: `str.lower()` is documented as using *"section 3.13 'Default Case Folding'"*, but case **folding** is what `casefold()` does; `lower()` is default case *conversion*. Verify against the standard before writing it down — if it holds, it is a one-line report worth filing. The behaviour to show either way: `'ß'.lower()` is `'ß'` and `'ß'.casefold()` is `'ss'`, so lowercasing is not case-insensitivity |
| 37 | `*` repetition, `in` / `not in`, `ord()` / `chr()` | **partly** | `ord`/`chr` appear throughout [counting characters](01_Text_and_Bytes/counting_characters/README.md) and [sorting](01_Text_and_Bytes/sorting_is_not_comparing/README.md) but are never *introduced*. The repetition operator's hook: `'Hi' * -8` is `''`, not an error — so a computed multiplier that goes negative produces an empty column instead of a traceback |

---

## Modules — `string` and `codecs`

| # | The question | Status | Hook to verify |
|---|---|---|---|
| 37 | The `string` module constants, `capwords`, `Template`, `Formatter` | **gap** | Worth one page, and the honest framing is *"the leftovers drawer"*: the constants are ASCII-only by definition and predate the `is*` methods, `capwords` is not `title()`, `Template` is the `$`-syntax that exists because `%` and `.format` are both too powerful to hand a user, and `Formatter` is the subclass hook nobody needs. The constants are also a good ASCII table in disguise |
| 1 | `string.printable` | **written** | [`repr` is not `str`](01_Text_and_Bytes/repr_is_not_str/README.md) §4. **Measured:** it is 100 characters long and `string.printable.isprintable()` is `False`, which the docs flag as deliberate |
| 28 | The [`codecs` ↗](https://docs.python.org/3/library/codecs.html) module — is there a page? Any new concepts? | **written** | [The codecs registry](01_Text_and_Bytes/the_codecs_registry/README.md). All three hooks held, one number did not: Python ships **eight** built-in error handlers, not five, so the one you write is the **ninth**. Two findings the hook did not predict — the *encoder* has the same bug and it never raises (`utf-16` writes its BOM once per chunk, leaving a `U+FEFF` sitting in the text as data), and the incremental interface is offered by every codec but honoured by only some (`zlib` streams, `base64` pads every chunk, and 3.11/3.12 decode the result to `b'abcde'` and report success where 3.13+ raise) |

---

## Unicode and the wider reading — mostly the sibling library's

The rule ([CONTRIBUTING.md](CONTRIBUTING.md)) is that the library owning the *subject* owns the page. These are encodings subjects; this library links them.

| The question | Status | Where |
|---|---|---|
| Add the [Unicode core spec ch.2 ↗](https://www.unicode.org/versions/Unicode17.0.0/core-spec/chapter-2/#G13708) link | **do it** | `RESOURCES.md` here and in the encodings library |
| Is there a page on **collation**? [UTS #10 ↗](https://www.unicode.org/reports/tr10/tr10-53.html) | **partly** | [Sorting is not comparing](01_Text_and_Bytes/sorting_is_not_comparing/README.md) here is the Python half; [sorting and collation ↗](https://masiarek.github.io/encodings-learning-library/07_Real_Data/sorting_and_collation/index.html) is a **stub** in the sibling. Neither names UTS #10's three-level model (primary/secondary/tertiary), which is the thing that makes "why is `ł` next to `l` but after it" answerable |
| **Deterministic sorting** ([UTS #10, *Deterministic Sorting* ↗](https://www.unicode.org/reports/tr10/tr10-53.html#Deterministic_Sorting)) | **gap** | Sibling. And it is a *good* gap: a collation that is correct is not necessarily deterministic, so two equal-ranking strings can swap between runs — which breaks pagination, diffs, and any test that sorts. Python's answer is `sorted(key=…)` stability plus a tiebreak on the raw string |
| What is different about **Unicode regex**? [UTS #18 ↗](https://www.unicode.org/reports/tr18/) | **gap** | Sibling, and it touches this library through `re`: `\w` against `str` is Unicode, against `bytes` is ASCII, and `re.UNICODE` vs `re.ASCII` is the switch. UTS #18's levels 1/2/3 are the vocabulary for saying *how* Unicode-aware an engine is; the encodings library already measures [PCRE2 ↗](https://masiarek.github.io/encodings-learning-library/11_Tools/pcre2/index.html) |
| Do we have pages for **sed, awk, sh**? | **partly** | [sed ↗](https://masiarek.github.io/encodings-learning-library/11_Tools/sed/index.html) and [awk ↗](https://masiarek.github.io/encodings-learning-library/11_Tools/awk/index.html) exist. **`sh` does not** — and a shell page is a real gap, because the shell is the one language in the set with no string type at all |
| [perlfaq5 ↗](https://perldoc.perl.org/perlfaq5) and [perlpacktut ↗](https://perldoc.perl.org/perlpacktut) — compare ABAP, Rust, Python, C | **gap** | Split them. perlfaq5 is file I/O and belongs against [opening a file](01_Text_and_Bytes/opening_a_file/README.md) (a stub here). **perlpacktut is the better one** — `pack`/`unpack` is Python's `struct`, Rust's `to_be_bytes`, C's cast-and-pray, and ABAP's fixed-width fields, which is a four-language page about the same idea and connects to [fixed-width byte fields ↗](https://masiarek.github.io/encodings-learning-library/07_Real_Data/fixed_width_byte_fields/index.html) |
| **Grapheme clusters** / .NET `StringInfo` | **partly** | [Counting characters](01_Text_and_Bytes/counting_characters/README.md) counts them with a deliberately crude approximation and says so. The proper page is the sibling's [a code point is not a character ↗](https://masiarek.github.io/encodings-learning-library/02_Characters/a_code_point_is_not_a_character/index.html), still a **stub**. The .NET detail worth stealing: .NET calls it a *text element* and ships an enumerator, which is one of the few standard libraries that does — Python does not, and that absence is the lesson |
| **Normalization** | **partly, and a boundary to settle** | A **stub** here; **written** in the sibling as [04_Python/normalization ↗](https://masiarek.github.io/encodings-learning-library/04_Python/normalization/index.html). Two libraries, one Python page, and the [roadmap](ROADMAP.md) already flags this as an open question. Decide it before writing: the sibling's Python chapter should probably point here |
| **Noncharacters** and private use ([FAQ ↗](https://www.unicode.org/faq/private_use.html#noncharacters)) | **partly** | Named in the sibling's [preparing a string ↗](https://masiarek.github.io/encodings-learning-library/02_Characters/preparing_a_string/index.html); no page. The hook: **a noncharacter is not invalid** — `U+FFFE` is a legal code point that UTF-8 will happily encode, and the reason the BOM works is that its byte-swapped twin is one of them |
| The [UTF FAQ ↗](https://www.unicode.org/faq/utf_bom.html) — anything new? | **written** | [Byte order and the BOM ↗](https://masiarek.github.io/encodings-learning-library/03_Encodings/byte_order_and_bom/index.html) covers it, including the `U+FFFE` mirror argument |
| **Ordinal string operations** (.NET `StringComparison.Ordinal`) — do we have it? | **gap, and a good one** | Not by that name, and the name is what is missing. Python's `==` **is** ordinal — it compares code points and nothing else — but Python never says so, so a Python programmer has no word for the distinction .NET forces you to make at every call. The four `résumé` spellings and their `IndexOf` results are a ready-made crosswalk row, and the last detail is the sharpest: .NET's *culture-sensitive* comparison **ignores embedded NUL characters**, so two strings that differ by a NUL compare equal. Verify Python's behaviour on the same pair |
| **String normalization** ([MS docs ↗](https://learn.microsoft.com/en-us/globalization/text/text-normalization)) | **partly** | Same row as normalization above |
| **Why UTF-7?** ([.NET `UTF7Encoding` ↗](https://learn.microsoft.com/en-us/dotnet/api/system.text.utf7encoding)) | **gap** | Short and worth it. UTF-7 exists because 1990s mail gateways were **7-bit**, and it is obsolete *and dangerous*: it is deprecated in .NET, and it is a live XSS vector because one string has several UTF-7 spellings. The sibling already uses it in [parser differentials ↗](https://masiarek.github.io/encodings-learning-library/12_Adversarial/parser_differentials/index.html); the missing piece is the *why* |
| The .NET [encoding overview ↗](https://learn.microsoft.com/en-us/globalization/encoding/encoding-overview), [best practices for strings ↗](https://learn.microsoft.com/en-us/dotnet/standard/base-types/best-practices-strings), [display data ↗](https://learn.microsoft.com/en-us/dotnet/standard/base-types/best-practices-display-data), [character encoding intro ↗](https://learn.microsoft.com/en-us/dotnet/standard/base-types/character-encoding-introduction) | **reference** | Read for *examples to borrow*, not for a page. The one structural idea worth importing is .NET's insistence that **every** string API takes an explicit comparison mode — the opposite of Python, where the default is invisible. Compare against [Python text in practice ↗](https://masiarek.github.io/encodings-learning-library/10_Best_Practices/python_text_in_practice/index.html) |
| [PowerShell character encoding ↗](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_character_encoding) — how good or bad? | **reference** | One row, not a page. The honest answer is *"much better since 6.0, and the version boundary is the whole story"*: Windows PowerShell 5.1 defaults to UTF-16LE for `>` redirection and the ANSI code page elsewhere; PowerShell 7 defaults to BOM-less UTF-8 everywhere. Verify before writing |
| [Intel HEX ↗](https://en.wikipedia.org/wiki/Intel_HEX) — useful for the tri-format kata? | **sibling** | Yes, one idea in particular. The sibling's [tribit ↗](https://masiarek.github.io/encodings-learning-library/08_Build_Your_Own/tribit/index.html) is a hand-rolled encoding; Intel HEX is a *shipped* one with the two things a hand-rolled format usually lacks — a **record type** and a **checksum** — and its checksum is two's-complement of the sum of every byte, which is four lines to implement and instantly makes a corrupted file detectable. That is the lesson to borrow: the format is unremarkable, the framing discipline is not |

---

## Exercises

| # | The question | Status | Hook |
|---|---|---|---|
| 4, 33 | Katas or Anki | **gap** | Row 5 of the five above |
| 35b | Rewrite the [Google Python exercises ↗](https://developers.google.com/edu/python) in C, ABAP and Rust, cross-referencing solutions | **gap, and check the licence first** | The idea is good and it is exactly this library's crosswalk instinct. But the material is someone else's: [CONTRIBUTING.md](CONTRIBUTING.md) says a *topic* may be taken and the prose, examples and data must be written here, and the exercise files carry an Apache 2.0 header — so the shape that works is **our own exercises on the same topics**, credited, not a port of theirs. Decide that before writing any of it |
| — | The [C# formatting challenge ↗](https://learn.microsoft.com/en-us/training/modules/csharp-basic-formatting/5-challenge) — worth doing as a kata? | **gap** | As a *format* it is worth copying: a fixed input, a fixed expected output, and the reader has to produce the format string. That is a kata with an answer key, which is the same contract `tools/run_examples.py` already enforces for pages |

---

## See also

- [Roadmap](ROADMAP.md) — what is written and what is a stub, page by page
- [The crosswalk](CROSSWALK.md) — the same ideas in Rust, C and ABAP; the place a new comparison row lands
- [CONTRIBUTING.md](CONTRIBUTING.md) — what it takes to turn a row above into a page
- [The sibling's backlog ↗](https://masiarek.github.io/encodings-learning-library/TODO.html) — the same job, done for the encodings library, and the model this page follows
