#!/usr/bin/env python3
"""A folded answer must be folded correctly, must have been run, and must be its own.

`## Practice` holds a kata: predict, run, check. Its answer is folded away in a
`<details>` block, and that block has failure modes no other gate in this repo
can see.

**The attribute.** `md_in_html` is enabled (mkdocs.yml), so a `<details>`
*without* `markdown="1"` ships its body as literal Markdown -- asterisks and
backticks drawn on the published page. GitHub renders the same block correctly
either way and `mkdocs build --strict` passes, because a missing attribute is
not a broken link. The author's own two previews are exactly the surfaces that
cannot show it.

**The answer.** An answer typed by hand is a claim like any other, and this
library does not take claims on trust -- so `## Practice` has to carry a
generated block (`<!-- output: -->` or `<!-- source: -->`) inside the fold.
That is what makes the answer key run in CI on Ubuntu, macOS and the 3.11
floor alongside every other example: a solution cannot rot into one that no
longer prints what the page says it prints.

**Whose answer it is.** Two rules the sibling encodings library gets for free
and this one does not. Every example here is Python, so a lesson's stem and its
kata's stem differ by one word -- `strip_is_a_set_py` against
`strip_is_a_set_kata_py` -- and pasting the lesson's own output into the fold
produces a plausible-looking answer to a question it does not answer. And a
fold copied from the page next door fills in perfectly: `run_examples.py` is
happy, the stem exists, the block renders, and the answer belongs to a
different kata. So the stem in the fold must say `_kata`, and its file must
live under the page's own folder.

Ten checks, each one a rule from CONTRIBUTING's "Try it, and Practice":

 1. Every `<details>` carries `markdown="1"`.
 2. No `???` fold. It is Material-only and prints as literal text on GitHub,
    which is the mirror of defect 1.
 3. A `## Practice` section folds its answer in a `<details>`.
 4. That fold contains at least one generated block.
 5. The block's stem contains `_kata`, so the key is the kata's own program.
 6. That stem's example file lives under the page's own folder.
 7. `## Try it` comes before `## Practice`, which comes before `## See also`.
 8. A stub has no `## Practice` -- there is no example behind it to answer with.
 9. Every `## Practice` has a row in KATAS.md, and every row points at a page
    that has one. The index is the one file no lesson owns, so nothing about
    your page reveals that its row is missing.
10. Every row's two links resolve, the kata link ends in `#practice`, and the
    IDs read K1, K2, K3... in table order -- so the number stays a label the
    table can renumber and never an address anyone saved.

    python3 tools/check_katas.py
    python3 tools/check_katas.py --selftest   # mutate each rule in turn

Code is stripped before any of this -- fenced blocks and inline spans both --
so a page may *show* a malformed block as an example, or name `<details>` in a
sentence, without failing its own gate. CONTRIBUTING.md does both.

What this gate does NOT check, on purpose: whether the answer is *right*.
`run_examples.py` owns that half -- it runs the program and compares stdout
against the recorded `.out` byte for byte, which is why an answer key must not
quote an exception message. `type(exc).__name__` is stable; the sentence after
it is reworded between CPython releases, and the key is compared byte for byte.
"""

from __future__ import annotations

import pathlib
import re
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
SKIP_DIRS = {".git", "site", ".venv", "__pycache__", ".github"}

FENCE = re.compile(r"^[ \t]*(```|~~~)")
CODE_SPAN = re.compile(r"`+[^`\n]*`+")
DETAILS = re.compile(r"<details\b[^>]*>", re.I)
GENERATED = re.compile(r"<!--\s*(?:output|source):([A-Za-z0-9_\-]+)\s*-->")
STUB = re.compile(r"^> \*\*Stub", re.M)
ADMONITION_FOLD = re.compile(r"^\?\?\?", re.M)
KATAS = REPO / "KATAS.md"
ROW = re.compile(
    r"^\|\s*K(\d+)\s*\|\s*\[[^\]]*\]\(([^)]+)\)\s*\|\s*\[[^\]]*\]\(([^)]+)\)\s*\|", re.M
)


def strip_code(text: str) -> str:
    """Blank out code, keeping line numbers intact.

    A page is allowed to *show* a wrong `<details>` as an example, and to name
    the tag inside backticks in a sentence. Only markup the page actually emits
    is the page's own, so only that is checked. Both forms go: fenced blocks,
    and inline spans -- the second is not an edge case, it is how this gate's
    rules are written down in CONTRIBUTING.
    """
    out, in_fence = [], False
    for line in text.split("\n"):
        if FENCE.match(line):
            in_fence = not in_fence
            out.append("")
            continue
        out.append("" if in_fence else CODE_SPAN.sub("", line))
    return "\n".join(out)


def section(text: str, heading: str) -> str | None:
    """The body under `## <heading>`, up to the next `## `, or None."""
    m = re.search(rf"^## {re.escape(heading)}\s*$", text, re.M)
    if not m:
        return None
    rest = text[m.end():]
    nxt = re.search(r"^## ", rest, re.M)
    return rest[: nxt.start()] if nxt else rest


def pages() -> list[pathlib.Path]:
    return [
        p
        for p in sorted(REPO.rglob("*.md"))
        if not any(part in SKIP_DIRS for part in p.relative_to(REPO).parts)
    ]


def example_stems() -> dict[str, str]:
    """stem -> repo-relative path, for every example in the library."""
    found: dict[str, str] = {}
    for p in sorted(REPO.rglob("examples/*")):
        if p.suffix in {".py", ".rs", ".sh", ".c"} and not any(
            part in SKIP_DIRS for part in p.relative_to(REPO).parts
        ):
            found[p.stem] = str(p.relative_to(REPO))
    return found


def check_text(rel: str, raw: str, examples: dict[str, str] | None = None) -> list[str]:
    """Every defect in one page's markup, as finished sentences.

    `examples` maps a stem to where its file lives; pass None to skip the
    on-disk half of rule 6 (the selftest drives this function on a fixture).
    """
    text = strip_code(raw)
    bad: list[str] = []

    for tag in DETAILS.findall(text):
        if 'markdown="1"' not in tag and "markdown='1'" not in tag:
            bad.append(
                f"{rel}: `{tag}` has no markdown=\"1\", so md_in_html leaves its "
                "body as literal Markdown on the site. GitHub and --strict will "
                "both stay green."
            )

    if ADMONITION_FOLD.search(text):
        bad.append(
            f"{rel}: a `???` collapsible is Material-only and prints as literal "
            'text on GitHub. Use <details markdown="1">.'
        )

    practice = section(text, "Practice")
    if practice is None:
        return bad

    if STUB.search(text):
        bad.append(
            f"{rel}: a stub has a `## Practice` section. There is no example "
            "behind the page, so the answer cannot have been run."
        )

    stems = GENERATED.findall(practice)
    if not DETAILS.search(practice):
        bad.append(
            f"{rel}: `## Practice` does not fold its answer in a <details> "
            "block, so the kata is spoiled by the page that sets it."
        )
    elif not stems:
        bad.append(
            f"{rel}: `## Practice` folds an answer that was typed, not run. Put "
            "the solution in examples/<stem>_kata_py.py and paste it with "
            "<!-- output:<stem>_kata_py -->, so CI checks the answer too."
        )

    folder = rel.rsplit("/", 1)[0] + "/" if "/" in rel else ""
    for stem in stems:
        if "_kata" not in stem:
            bad.append(
                f"{rel}: `## Practice` answers with {stem!r}, which is not a "
                "kata's own program -- almost certainly the lesson's output "
                "pasted a second time. Name the answer key <stem>_kata_py."
            )
            continue
        if examples is None:
            continue
        where = examples.get(stem)
        if where is None:
            bad.append(
                f"{rel}: `## Practice` answers with {stem!r}, and no examples/ "
                "file has that stem."
            )
        elif not where.startswith(folder):
            bad.append(
                f"{rel}: `## Practice` answers with {stem!r}, which lives in "
                f"{where} -- another lesson's folder. A fold copied from the "
                "page next door fills in perfectly and answers the wrong kata."
            )

    # Compare DOCUMENT order against the canonical one. Building the list by
    # iterating the canonical tuple would produce it sorted by construction --
    # a check that cannot fail, which is what the selftest caught.
    seen = []
    for h in ("Try it", "Practice", "See also"):
        m = re.search(rf"^## {re.escape(h)}\s*$", text, re.M)
        if m:
            seen.append((m.start(), h))
    seen.sort()
    names = [h for _, h in seen]
    canonical = [h for h in ("Try it", "Practice", "See also") if h in names]
    if names != canonical:
        bad.append(
            f"{rel}: the closing sections are in the order {names}. "
            "CONTRIBUTING puts them Try it, then Practice, then See also."
        )
    return bad


def index_rows() -> list[tuple[int, str, str]]:
    """(number, kata href, lesson href) for every row of the KATAS.md table."""
    if not KATAS.exists():
        return []
    return [(int(n), k, les) for n, k, les in ROW.findall(KATAS.read_text(encoding="utf-8"))]


def check_index(practice_pages: set[str]) -> list[str]:
    """The index and the pages must agree, and the numbering must be a sequence."""
    if not KATAS.exists():
        return [f"KATAS.md is missing, and {len(practice_pages)} page(s) have a kata."]

    bad: list[str] = []
    rows = index_rows()
    numbers = [n for n, _, _ in rows]
    if numbers != list(range(1, len(numbers) + 1)):
        bad.append(
            f"KATAS.md numbers its rows {numbers} -- they must read K1, K2, K3... "
            "in table order. The number is a label the table renumbers freely; "
            "that only works while it matches the position."
        )

    indexed: set[str] = set()
    for n, kata_href, lesson_href in rows:
        if not kata_href.endswith("#practice"):
            bad.append(
                f"KATAS.md K{n}: the kata link is {kata_href!r}, which does not "
                "end in #practice, so it lands on the page rather than on the "
                "exercise."
            )
        for href in (kata_href, lesson_href):
            if not (REPO / href.split("#", 1)[0]).exists():
                bad.append(f"KATAS.md K{n}: {href!r} names no such file.")
        indexed.add(kata_href.split("#", 1)[0])

    for rel in sorted(practice_pages - indexed):
        bad.append(
            f"{rel}: has a `## Practice` section and no row in KATAS.md. Nothing "
            "on the page can reveal that -- add the row where the kata should be "
            "attempted, and renumber."
        )
    for rel in sorted(indexed - practice_pages):
        bad.append(f"KATAS.md points at {rel}, which has no `## Practice` section.")
    return bad


def scan() -> list[str]:
    bad: list[str] = []
    practice: set[str] = set()
    examples = example_stems()
    for p in pages():
        rel = p.relative_to(REPO).as_posix()
        raw = p.read_text(encoding="utf-8")
        bad += check_text(rel, raw, examples)
        if rel != "KATAS.md" and section(strip_code(raw), "Practice") is not None:
            practice.add(rel)
    return bad + check_index(practice)


# --------------------------------------------------------------------------
# The selftest. A check that survives its own mutation is not guarding anything.
# --------------------------------------------------------------------------

GOOD = """# A page

## Try it

1. Do a thing.

## Practice

Predict it.

<details markdown="1">
<summary><strong>Answers</strong></summary>

<!-- output:a_page_kata_py -->
```text
the answer
```
<!-- /output -->

</details>

## See also

- Something
"""

FIXTURE = "01_Chapter/a_page/README.md"
FIXTURE_EXAMPLES = {
    "a_page_kata_py": "01_Chapter/a_page/examples/a_page_kata_py.py",
    "next_door_kata_py": "01_Chapter/next_door/examples/next_door_kata_py.py",
}

MUTATIONS = [
    ('a <details> with no markdown="1"',
     lambda t: t.replace('<details markdown="1">', "<details>")),
    ("a ??? fold instead of <details>",
     lambda t: t.replace('<details markdown="1">', "??? note")),
    ("an answer that was typed, not run",
     lambda t: t.replace("<!-- output:a_page_kata_py -->", "").replace("<!-- /output -->", "")),
    ("an unfolded answer",
     lambda t: t.replace('<details markdown="1">', "").replace("</details>", "")),
    ("the lesson's own output pasted as the answer",
     lambda t: t.replace("a_page_kata_py", "a_page_py")),
    ("a fold copied from the page next door",
     lambda t: t.replace("a_page_kata_py", "next_door_kata_py")),
    ("an answer key with no file behind it",
     lambda t: t.replace("a_page_kata_py", "a_typo_kata_py")),
    ("Practice before Try it",
     lambda t: t.replace("## Try it", "## TRY IT LATER").replace("## See also", "## Try it\n\n## See also")),
    ("a stub carrying a Practice section",
     lambda t: t.replace("# A page", "# A page\n\n> **Stub — an outline, not a lesson.**")),
]

GOOD_ROW = (
    "| # | Kata | Lesson | Level |\n|---|---|---|---|\n"
    "| K1 | [k](CONTRIBUTING.md#practice) | [l](CONTRIBUTING.md) | 101 |\n"
)

INDEX_CASES = [
    ("a kata with no row in the index", GOOD_ROW, {"CONTRIBUTING.md", "orphan.md"}),
    ("a row pointing at a page with no kata", GOOD_ROW, set()),
    ("numbering that skips", GOOD_ROW.replace("| K1 |", "| K2 |"), {"CONTRIBUTING.md"}),
    ("a kata link that does not reach #practice",
     GOOD_ROW.replace("#practice", ""), {"CONTRIBUTING.md"}),
    ("a row naming a file that does not exist",
     GOOD_ROW.replace("CONTRIBUTING.md#practice", "NOPE.md#practice"), {"CONTRIBUTING.md"}),
]


def selftest() -> int:
    global KATAS
    import tempfile

    print("selftest: one good page, then one mutation at a time\n")
    failures = 0

    def report(ok: bool, name: str, detail: list[str] | None = None) -> None:
        nonlocal failures
        failures += 0 if ok else 1
        print(f"  {'ok  ' if ok else 'FAIL'}  {name}")
        if not ok:
            for line in detail or []:
                print(f"          unexpected: {line}")
            if not detail:
                print("          expected a complaint, GOT NONE")

    clean = check_text(FIXTURE, GOOD, FIXTURE_EXAMPLES)
    report(not clean, "the good page passes", clean)

    # The rules are written down in prose that names the tag. A gate that fails
    # the file describing it is not a gate, it is a trap.
    prose = GOOD + "\nA page may write `<details>` and `???` in a sentence.\n"
    noisy = check_text(FIXTURE, prose, FIXTURE_EXAMPLES)
    report(not noisy, "a <details> named in an inline code span is ignored", noisy)

    for name, mutate in MUTATIONS:
        report(bool(check_text(FIXTURE, mutate(GOOD), FIXTURE_EXAMPLES)), name)

    # The index rules read KATAS.md, so they are exercised against a temporary
    # one rather than by editing the repo to prove a gate bites.
    saved = KATAS
    with tempfile.TemporaryDirectory() as tmp:
        for name, body, practice in INDEX_CASES:
            KATAS = pathlib.Path(tmp) / "KATAS.md"
            KATAS.write_text(body, encoding="utf-8")
            report(bool(check_index(practice)), name)
        KATAS = pathlib.Path(tmp) / "KATAS.md"
        KATAS.write_text(GOOD_ROW, encoding="utf-8")
        quiet = check_index({"CONTRIBUTING.md"})
        report(not quiet, "a correct index says nothing", quiet)
    KATAS = saved

    print()
    if failures:
        print(
            f"selftest FAILED: {failures} case(s) wrong. A check that survives "
            "its own mutation is not guarding anything."
        )
        return 1
    print(
        f"selftest ok: {len(MUTATIONS)} page mutations and {len(INDEX_CASES)} "
        "index mutations, each one reported."
    )
    return 0


def main(argv: list[str]) -> int:
    if "--selftest" in argv:
        return selftest()
    bad = scan()
    if not bad:
        n = len(index_rows())
        print(
            f"katas: K1-K{n}, each folded correctly, answered by its own program, "
            "and indexed."
        )
        return 0
    print("katas: folded answers that will not render, were not run, or are not theirs.\n")
    for line in bad:
        print(f"  {line}")
    print("\n  CONTRIBUTING.md, 'Try it, and Practice', has the rules and why.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
