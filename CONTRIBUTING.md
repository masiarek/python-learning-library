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

Then, in this order: the mechanism in prose, the generated output block, what the run shows, the bridge, `## Try it`, `## See also`.

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

**Stdlib only.** A reader must be able to run any page with the `python3` already on their machine, and CI has no install step to prove it. A page may *name* a third-party library in prose when leaving it out would give bad advice — [sorting](01_Text_and_Bytes/sorting_is_not_comparing/README.md) names PyICU for exactly that reason — but it may not import one.

**Deterministic.** No clocks, no randomness, no network, no reading the filesystem, and **nothing that depends on an installed locale**. Every example runs under a fixed environment (`LC_ALL=C`, `PYTHONUTF8=1`). Where the honest answer *is* machine-dependent, print the dependency rather than a value: the sorting lesson prints whether `pl_PL.UTF-8` exists rather than an order that would differ between two computers. CI runs on Ubuntu **and** macOS, which is the only check that catches this class of mistake.

**Written to be read aloud.** Numbered sections, aligned columns, prose in the print statements. A reader should understand the output without the page and the page without the output.

**A snippet in the prose puts its output in a trailing comment**, on the line that prints it, so the whole thing survives a copy-paste:

```python
len("Łódź")   # 4
```

**Never open a page with code that does not run.** The first block on a page is the one that gets pasted.

## Bridges

Every lesson has a section **If you are coming from ABAP** — and Rust or C where the comparison is sharp. Those are the languages this reader already thinks in, and a bridge to a language you already speak is the fastest teaching on the page. Say what transfers *and* what the new language enforces that the old one left to habit.

The ABAP half is prose. CI cannot run ABAP, so every page says so: *(Not machine-checked — CI cannot run ABAP.)* Never quote an SAP code-page number without saying it should be verified against the system.

## Other people's material

This library exists alongside good paid material, and several pages were prompted by it. **Cite it, link it, and write your own.** A page may take a *topic* from an article or a course — a topic is not ownable — but the prose, the examples and the data must be written here. Do not paste someone's code into an example, do not paraphrase their explanation, and do not reproduce their figures. Put the source in [RESOURCES.md](RESOURCES.md) and say on the page that it prompted it. This repository is public; that is the whole reason the rule is strict.

## Links

- Link a folder by naming its `README.md` — `[label](some_folder/README.md)`, never `[label](some_folder/)`.
- A repo path in backticks should be a link, not bare code text.
- **A link that leaves the library ends its label with ` ↗`**; an internal link never does. `python3 tools/check_link_style.py --fix` adds and removes them.
- Where a sibling library already teaches something, link to it and do not repeat it. A folder README publishes as `index.html`, never `README.html`.

## Nav order

Sidebar reading order lives in `NAV_ORDER` in `mkdocs_hooks.py`, keyed by folder path. **Never set order by renaming files to `01_`, `02_`** — a filename is a permanent URL.

## Before you commit

```bash
python3 tools/run_examples.py --check
python3 tools/check_link_style.py
uv run --group docs mkdocs build --strict
```

All three are what CI runs.
