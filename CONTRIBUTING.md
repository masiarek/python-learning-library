# Conventions

House rules for writing a page here. Readers browsing lessons do not need this file; it is for whoever is about to add one.

## The shape of a lesson

```
01_Text_and_Bytes/
  sorting_is_not_comparing/
    README.md                                   the lesson
    examples/
      sorting_is_not_comparing_py.py            the program
      sorting_is_not_comparing_py.out           its recorded output
```

One idea per folder. The folder name is the idea, in `lower_snake_case`, and it becomes a permanent URL — name it for what it teaches, not for where it currently sits in the reading order.

## The page

Open with the title, then two lines that let a reader decide in five seconds whether this is their page:

```markdown
# Sorting is not comparing

**Level:** 201 · for Python programmers

**One line:** `sorted()` orders strings by code point, no human alphabet is ordered by code point, and the gap between those two facts is why a Polish name list comes back wrong.
```

`**Level:**` is `101` / `201` / `301` / `reference`, then `·`, then who it is for. The one-line summary states the *claim*, not the topic.

Then, in this order: the mechanism in prose, the generated output block, what the run shows, the bridge, `## Try it`, `## Practice` if the page has a kata, `## See also`.

Do not hard-wrap paragraphs. Write each paragraph as one long line and let the editor soft-wrap.

## Output is generated, never typed

Mark the spot and let the tool fill it:

```markdown
<!-- output:sorting_is_not_comparing_py -->
<!-- /output -->
```

`tools/run_examples.py` runs the program and pastes what it actually printed. Inside the markers is generated; outside is yours. There is a second kind, `<!-- source:stem -->`, which pastes the program itself — for pages where the code *is* the lesson.

```bash
python3 tools/run_examples.py                     # verify + refill
python3 tools/run_examples.py --update --only X   # record X's output as its key
python3 tools/run_examples.py --check             # write nothing, fail on drift (CI)
```

**Always pass `--only` with `--update`**, and **read what it recorded before committing**. `--update` accepts whatever the program printed, so it will happily enshrine a bug. Two prose numbers were wrong in this library's first three lessons and only caught by reading the recorded output against the sentence describing it — if a page says "eleven bytes", check that the run says eleven.

## The programs

**Stdlib only.** A reader must be able to run any page with the `python3` already on their machine, and CI has no install step to prove it.

**A comparison in another language is a link, not an example.** Where the contrast is the lesson — Rust's `len()` counts bytes where Python's counts code points — link the sibling library that owns that language and say the one sentence that makes the contrast land. Carrying the other language's example here would mean a second toolchain in CI for one page, and it duplicates a lesson that library already has. Check before you write one: [counting characters](01_Text_and_Bytes/counting_characters/README.md) nearly shipped a Rust port of a page the Rust library had already written.

**The library that owns the *subject* owns the page — and then both sides cross-reference it.** The rule above says where an *example* may live; this one says where the *page* does, and they point in opposite directions often enough to be worth stating apart. A lesson whose subject is a Python method belongs here even when the cross-language contrast is half of what makes it interesting: [Is it a letter?](01_Text_and_Bytes/is_it_a_letter/README.md) is about `str.isalpha()`, so it is a Python page, and the Rust library carries a see-also to it rather than a page of its own. When you land one, link out *and* add the bullet back on the sibling page — a comparison that only one of the two libraries knows about is half-built.

**Deterministic.** No clocks, no randomness, no network, no reading the filesystem, and **nothing that depends on an installed locale**. Every example runs under a fixed environment (`LC_ALL=C`, `PYTHONUTF8=1`). Where the honest answer *is* machine-dependent, print the dependency rather than a value: the sorting lesson prints whether `pl_PL.UTF-8` exists rather than an order that would differ between two computers. CI runs on Ubuntu **and** macOS, which is the only check that catches this class of mistake.

**It must run on the oldest Python the project claims.** `pyproject.toml` says `requires-python = ">=3.11"`, and the `python3` on your machine is almost certainly newer, so "it ran locally" proves nothing about the floor. The trap that made this a rule: a **backslash inside an f-string expression** — `f"{b'a\r\nb'.splitlines()}"` — is a `SyntaxError` before 3.12, because PEP 701 is what put f-strings in the grammar. Two examples landed on the same day in 2026-09 that did not run at all on 3.11, and both CI legs were green, because both runners ship something newer. Hoist the literal into a variable and interpolate the name. CI now has a `floor` job pinned to 3.11 for exactly this; to check before you push:

```bash
docker run --rm -v "$PWD":/w:ro -w /w -e LC_ALL=C -e LANG=C -e PYTHONUTF8=1 \
  python:3.11-slim python3 -I <path to your example>
```

**An exception's message is not API — prefer the type in an answer key.** `type(exc).__name__` is stable; the sentence after it is not. CPython rewords these between releases, and the key is compared byte for byte: 3.14 changed the unhashable-key `TypeError` from *"unhashable type: 'bytearray'"* to *"cannot use 'bytearray' as a dict key (unhashable type: 'bytearray')"*, and the `tomllib` bytes error was reworded in the same release. Some pages do print messages, because the message *is* the lesson — the `str`/`bytes` boundary reads better with Python's own words. That is a deliberate cost, and it comes with an obligation: run the example across `python:3.11/3.12/3.13/3.14-slim` before recording the key, and pick a wording that has been stable across all four.

**Written to be read aloud.** Numbered sections, aligned columns, prose in the print statements. A reader should understand the output without the page and the page without the output.

**A snippet in the prose puts its output in a trailing comment**, on the line that prints it, so the whole thing survives a copy-paste:

```python
len("Łódź")   # 4
```

**Never open a page with code that does not run.** The first block on a page is the one that gets pasted.

**A fence title never holds a backtick** — name code bare, as every title here does, because GitHub does not read a `` ``` `` line whose info string contains one as a fence (its closing `` ``` `` then opens a block that swallows what follows) and `mkdocs build --strict` fails on it; a `~~~` fence is the fallback if a title truly needs a backtick, since every fence-parsing tool in this repo accepts `~~~`.

## Bridges

Every lesson has a section **If you are coming from ABAP** — and Rust or C where the comparison is sharp. Those are the languages this reader already thinks in, and a bridge to a language you already speak is the fastest teaching on the page. Say what transfers *and* what the new language enforces that the old one left to habit.

The ABAP half is prose. CI cannot run ABAP, so every page says so: *(Not machine-checked — CI cannot run ABAP.)* Never quote an SAP code-page number without saying it should be verified against the system.

## Try it, and Practice

**`## Try it` closes a lesson.** Three to five numbered prompts, each one something the reader runs against *their own* files — the CSV that came out wrong, a script they already have, a filename their tools cannot see. All 19 finished lesson pages here end with one; the only pages without it are the three stubs, which have no example behind them to try. Treat it as required.

**`## Practice` is optional, and it is a different thing.** It holds a **kata**: predict the answer, then run it, then check. It goes after `## Try it` and before `## See also`.

The test for which section a prompt belongs in is whether **you can print the answer**:

- *"Read a file two ways and compare the `len()` of each"* has no answer — the answer is on the reader's disk. `## Try it`.
- *"Write down the type and value of these eight expressions before you run any of them"* has exactly one answer, and it is the same on every machine. `## Practice`.

Both failure modes are quiet. A kata with no checkable answer is a chore the reader abandons; a *Try it* with an answer printed under it is a claim about a file nobody here has seen.

**Fold the answer, and put `markdown="1"` on the tag:**

```markdown
<details markdown="1">
<summary><strong>Answers</strong></summary>

<!-- output:strip_is_a_set_kata_py -->
<!-- /output -->

</details>
```

That attribute is load-bearing and its absence is invisible from the author's chair. `md_in_html` is enabled in `mkdocs.yml`, so **without** `markdown="1"` the body ships as literal Markdown — asterisks and backticks drawn on the published page — while GitHub renders the same block correctly either way and `mkdocs build --strict` passes, because it is not a link error. The sibling encodings library shipped its first kata exactly like that, and the only surface showing the bug was the live site. Do not reach for a `???` Material admonition instead; that one prints as literal text on GitHub, which is the mirror of the same problem.

**An answer has to have been run** — required, not preferred, and machine-checked. The solution goes in `examples/<stem>_kata_py.py` beside the lesson's own program and is pasted into the fold with `<!-- output:<stem>_kata_py -->`, so the answer key runs in CI on Ubuntu, macOS and the 3.11 floor with every other example, and a solution cannot rot into one that no longer prints what the page says.

Two rules follow from every example here being Python, and both catch a mistake nothing else does. **The stem in the fold must contain `_kata`**: a lesson's stem and its kata's stem differ by one word, so pasting `<!-- output:strip_is_a_set_py -->` into the fold fills in perfectly and answers a question nobody asked. And **the file must live under the page's own folder**: a fold copied from the page next door also fills in perfectly, and `run_examples.py` has no way to know it is on the wrong page.

**Prefer `type(exc).__name__` over the message** in an answer key. The key is compared byte for byte and CPython rewords these between releases — 3.14 changed the unhashable-key `TypeError` from *"unhashable type: 'bytearray'"* to *"cannot use 'bytearray' as a dict key (unhashable type: 'bytearray')"*. A lesson page may print a message where the message *is* the lesson, at the cost of running it across `python:3.11/3.12/3.13/3.14-slim` first; a kata should not need to.

```bash
python3 tools/check_katas.py              # ten rules, all of them from this section
python3 tools/check_katas.py --selftest   # prove the gate still bites
```

It reads prose only. Fenced blocks **and inline code spans** are stripped first, so a page may show a malformed fold as an example, or name the tag in a sentence, without failing its own gate — which is what this section does twice.

**A kata lives on the page for the topic it teaches**, never in a folder of its own and never with a number in its heading. Folders are permanent URLs and a sequence is the thing that gets reordered — the same reasoning as [Nav order](#nav-order) below. The sequence lives in [KATAS.md](KATAS.md), a table that costs nothing to reshuffle, and **a new kata needs a row there**: the index is the one file no lesson owns, so nothing about your page can reveal that its row is missing. `check_katas.py` fails a `## Practice` with no row, a row pointing at a page with no kata, a row whose links do not resolve, and numbering that has stopped reading K1, K2, K3 in table order.

**Do not print the kata's number on its own page.** Open with a short bold title instead. The number lives in that one table, which is what makes reordering free; a `K7` in a page's prose is a second place to update and the reason a stale one goes unnoticed.

**A stub gets neither section.** It has no example behind it, so a *Try it* would point at nothing and a folded answer would be a guess with a disclosure triangle over it.

## Other people's material

This library exists alongside good paid material, and several pages were prompted by it. **Cite it, link it, and write your own.** A page may take a *topic* from an article or a course — a topic is not ownable — but the prose, the examples and the data must be written here. Do not paste someone's code into an example, do not paraphrase their explanation, and do not reproduce their figures. Put the source in [RESOURCES.md](RESOURCES.md) and say on the page that it prompted it. This repository is public; that is the whole reason the rule is strict.

## Links

- Link a folder by naming its `README.md` — `[label](some_folder/README.md)`, never `[label](some_folder/)`.
- A repo path in backticks should be a link, not bare code text.
- **A link that leaves the library ends its label with ` ↗`**; an internal link never does. `python3 tools/check_link_style.py --fix` adds and removes them.
- Where a sibling library already teaches something, link to it and do not repeat it. A folder README publishes as `index.html`, never `README.html`.

## Nav order

Sidebar reading order lives in `NAV_ORDER` in `mkdocs_hooks.py`, keyed by folder path. **Never set order by renaming files to `01_`, `02_`** — a filename is a permanent URL. A lesson's sidebar *label* is its README's `# H1` with the backticks dropped, so write the label there; `LABEL_OVERRIDES`, beside `NAV_ORDER`, holds the rare label that is deliberately not the H1.

## Before you commit

```bash
python3 tools/run_examples.py --check
python3 tools/check_link_style.py
python3 tools/check_katas.py
uv run --group docs mkdocs build --strict
```

All four are what CI runs.
