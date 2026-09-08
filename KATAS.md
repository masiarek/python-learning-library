# Katas

**Level:** reference · the practice track

**One line:** The lessons explain; the katas make you predict. Each one lives on the page for the topic it teaches — this is the only place they are put in an order.

## Why this exists at all

Three pages in this library explain `bytes`. If the concept still will not stick after three expositions, the missing thing is **repetition, not more prose** — which is what a kata is for and what a fourth page would not be. That is the whole argument, and it is the reason the first four katas below are all about the same type.

Reading an explanation and being able to produce the answer are different acts, and only the second one is what a kata trains. So no kata here asks you to recognise a definition. Every one asks you to **write the answer down before you run anything** — a type, a length, a set of bytes, a format spec — because a prediction you got wrong is the only signal that tells you which half of the page you actually absorbed.

## Where a kata lives

**A kata belongs to its topic, not to a folder of its own.** The page that explains the type boundary is the page that asks you to predict what crosses it, under a `## Practice` heading near the end, with the answer folded into a `<details markdown="1">` block.

That is deliberate, and the reason is that folders are URLs. A topic — `bytes`, the format spec, `strip` — is stable for years; a *sequence* is not. The moment a kata belongs between K1 and K2, a `K01_…/` folder either gets renumbered, breaking every link anyone saved, or starts lying about its own order. So the sequence lives here, in a table that costs nothing to reorder, and the numbers below are labels rather than addresses. Same rule as the sidebar: order is presentation, so it belongs in a page, never in a path.

**Every answer here is printed by a program**, recorded as an answer key and run by CI on Ubuntu, on macOS and on the 3.11 floor with every other example in the library — so a solution cannot rot into one that no longer says what the page says. [`tools/check_katas.py`](tools/check_katas.py) enforces that, and the rules are written down in [CONTRIBUTING.md](CONTRIBUTING.md).

## The katas

The order is the practice order, and it is **not** the sidebar's reading order — which is the point of having this table. Bytes first, because that is where the repetition was asked for.

| # | Kata | Lesson | Level |
|---|---|---|---|
| K1 | [Eight expressions over one word, and the one that lies quietly](01_Text_and_Bytes/str_is_not_bytes/README.md#practice) | [`str` is not `bytes`](01_Text_and_Bytes/str_is_not_bytes/README.md) | 101 |
| K2 | [Eight calls into a four-job constructor — which two are equal?](01_Text_and_Bytes/making_a_bytes_object/README.md#practice) | [Making a `bytes` object](01_Text_and_Bytes/making_a_bytes_object/README.md) | 101 → 201 |
| K3 | [What `+=` did to the other name, and the key that cannot be a key](01_Text_and_Bytes/bytearray_is_mutable/README.md#practice) | [`bytearray` is the mutable one](01_Text_and_Bytes/bytearray_is_mutable/README.md) | 201 |
| K4 | [Seven crossings, and the one that neither failed nor was right](01_Text_and_Bytes/encode_and_decode/README.md#practice) | [Encode and decode](01_Text_and_Bytes/encode_and_decode/README.md) | 101 → 201 |
| K5 | [Eight literals, and the one that breaks a regex you did not write raw](01_Text_and_Bytes/string_literals/README.md#practice) | [String literals](01_Text_and_Bytes/string_literals/README.md) | 201 |
| K6 | [Eight one-liners about a word that means two things](01_Text_and_Bytes/repr_is_not_str/README.md#practice) | [`repr` is not `str`](01_Text_and_Bytes/repr_is_not_str/README.md) | 201 |
| K7 | [Eight calls, and the one that is right by accident](01_Text_and_Bytes/strip_is_a_set/README.md#practice) | [`strip` is a set, not a prefix](01_Text_and_Bytes/strip_is_a_set/README.md) | 201 |
| K8 | [One drill per slot, then the grammar read backwards](01_Text_and_Bytes/the_format_mini_language/README.md#practice) | [The format mini-language](01_Text_and_Bytes/the_format_mini_language/README.md) | 201 |

**K1–K4 are one subject asked four ways** — the type boundary, the constructor, the mutable half, and the two doors between them. Doing them in order is worth more than doing any one of them twice, because the thing that does not stick is not a fact but a *habit*: asking "which of the two types am I holding?" at the moment a value arrives rather than at the moment it breaks.

**K8 is the odd one out, and deliberately.** The format spec is `[[fill]align][sign][z][#][0][width][grouping][.precision][type]` — nine independent slots in a fixed order, which is a grammar rather than a fact, and a grammar is exactly what drilling is for. It is the one kata here that also runs backwards: given the output, write the spec.

## Does an Anki deck follow?

**Yes — and it is a second commit, not a rendering of these katas.** Both halves of that matter, so both are written down here rather than left as an intention.

**Why it is not generated from the katas.** A kata and a card train different things. A kata is a paragraph of prediction with one checkable answer; a card is one fact retrieved in under ten seconds. Mechanically turning these answer keys into cards would put a forty-line table on the back of a card, which is a card nobody reviews twice. The sibling [Rust library ↗](https://masiarek.github.io/rust-learning-library/) already learned this: its 164 cards are written as cards, in `cards_*.py`, and its README says the strongest type is *predict the output* — a kata compressed past the point where the prose survives.

**The shape to copy, when it comes.** The Rust library's `10_Resources/anki/` is three files and one rule: `cards_*.py` is the source, `verify.py` compiles and runs every code block on a card *before* the deck is built, `build.py` renders the tab-separated `.txt`, and **the generated `.txt` is never hand-edited**. That gate is not ceremony — building four decks it caught a wrong claim about normalisation, an example that was itself a borrow error, and three snippets whose escapes had been eaten, all of which read as correct. A Python deck here would use the same contract as [`tools/run_examples.py`](tools/run_examples.py): stdlib only, `python3 -I`, exact output match, and `type(exc).__name__` rather than a message.

**What it is waiting for, and it is not a date.** The first deck is `Python::Bytes`, and it wants two pages this library does not have yet: [Opening a file](01_Text_and_Bytes/opening_a_file/README.md) and [Standard in, standard out, and pipes](01_Text_and_Bytes/stdin_stdout_and_pipes/README.md) are both still stubs, and a deck about the type boundary that cannot say what `open()` does when you do not name an encoding is teaching half of it. It also wants a `10_Resources/` chapter to live in, which does not exist here either — and an empty folder created in advance is clutter with a permanent URL attached.

So: katas now, deck after those two stubs graduate. If you are reading this and both of them are marked written in [ROADMAP.md](ROADMAP.md), the deck is the next thing.

## See also

- [CONTRIBUTING.md](CONTRIBUTING.md) — the `## Try it` / `## Practice` rules, and the two quiet failure modes they exist to catch
- [ROADMAP.md](ROADMAP.md) — what is written and what is a stub
- [What to write next](TODO.md) — the questions backlog this practice track came out of
- [Anki decks ↗](https://masiarek.github.io/rust-learning-library/10_Resources/anki/index.html) — the sibling library's deck, and the generator this one would copy
