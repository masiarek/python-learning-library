"""Build-time fixes that would otherwise cost a pinned plugin dependency.

Two jobs, both about the sidebar:

1. **Clean chapter labels.** MkDocs derives a section label from the folder name
   on disk, so `01_Bits_and_Bytes/` reads as "01 Bits And Bytes". The numeric prefix exists
   to set reading order in a file listing; it should not be visible in the nav.
   Only *prefixed* folders are relabelled from their name. A lesson folder takes
   its README's own H1, backticks dropped: MkDocs working from the folder name
   turned `bin_is_not_the_bits` into "Bin is not the bits" and `pyproject_toml`
   into "Pyproject toml", and `mkdocs build --strict` passes either way.
   `LABEL_OVERRIDES` holds the rare label that is deliberately not the H1.

2. **Order the sections.** `NAV_ORDER` states the intended reading order per
   folder, keyed by folder path, listing children by their on-disk name.

Why order here rather than by renaming files: a filename is a permanent URL.
Renumbering `03_` to `04_` to insert a lesson would move every page after it and
break any link anyone saved. Ordering is presentation, so it belongs in the
presentation layer. Unlisted pages keep their alphabetical slot at the bottom, so
adding a page needs no edit here.

One structural note that is easy to get wrong: the top-level object MkDocs hands
`on_nav` is a `Navigation`, whose children live on `.items`. Only `Section` has
`.children`. A hook that reaches for `.children` at the top level silently does
nothing at all — the build still succeeds, and the sidebar is simply never
touched.

Two checks ride along at the bottom of the file, unrelated to the sidebar:
every TAB inside a fence has to reach the page's HTML, and no fence title may
hold a backtick, which GitHub cannot parse. Each has a comment block of its own
saying why.
"""

from __future__ import annotations

import logging
import pathlib
import re

# A child of the "mkdocs" logger, so `mkdocs build --strict` counts its warnings.
log = logging.getLogger("mkdocs.plugins.mkdocs_hooks")

PREFIX = re.compile(r"^(\d+)[_-]")

# Words the naive title-caser gets wrong.
FIXUPS = {
    "Vs": "vs",
    "And": "and",
    "Or": "or",
    "The": "the",
    "To": "to",
    "A": "a",
    "In": "in",
    "Of": "of",
}

# Lesson folders whose sidebar label is deliberately not their H1. Every other
# lesson folder is labelled with its README's H1, backticks dropped -- see
# `_visit`. Keyed by on-disk folder name -- a folder name is a permanent URL, so
# the fix belongs here rather than in a rename. Like NAV_ORDER, an entry naming a
# folder that no longer exists is a silent no-op.
LABEL_OVERRIDES: dict[str, str] = {
    # The H1 is a claim, "Four ways to find it, and four ways to fail"; in a
    # sidebar, "it" has nothing to point at.
    "finding_a_substring": "Finding a substring",
}

# Reading order per folder path. Children named by on-disk name; anything not
# listed sorts alphabetically after the listed ones.
NAV_ORDER: dict[str, list[str]] = {
    "": [
        "index.md",
        "00_Start_Here",
        "01_Text_and_Bytes",
        "02_Projects_and_Environments",
        "KATAS.md",
        "CROSSWALK.md",
        "GLOSSARY.md",
        "RESOURCES.md",
        "ROADMAP.md",
        "TODO.md",
    ],
    # The type boundary first, then the two doors, then the constructor that
    # quietly is one of them, then the six places code points mislead you,
    # then the boundaries with the outside world -- ending with the registry
    # behind the two doors, which is where data arriving in pieces goes wrong.
    #
    # `opening_a_file` moved down into that last group on 2026-09-08, when it
    # stopped being a stub about the default encoding and became a page about
    # the file API. It reads after `what_ends_a_line`, because its line-counting
    # section is that page's boundary set applied to a file, and before the pipe
    # and filesystem pages, which are the same subject one layer out.
    "01_Text_and_Bytes": [
        "README.md",
        "str_is_not_bytes",
        "string_literals",
        "encode_and_decode",
        "making_a_bytes_object",
        "bytearray_is_mutable",
        "counting_characters",
        "slicing_is_not_indexing",
        "is_it_a_letter",
        "lowercasing_is_not_folding",
        "repr_is_not_str",
        "what_ends_a_line",
        "strip_is_a_set",
        "finding_a_substring",
        "translate_is_a_table",
        "the_format_mini_language",
        "padding_is_not_alignment",
        "bin_is_not_the_bits",
        "comparison_has_a_mode",
        "normalization",
        "sorting_is_not_comparing",
        "opening_a_file",
        "stdin_stdout_and_pipes",
        "filenames_are_not_text",
        "what_kind_of_file_is_this",
        "the_string_module",
        "the_codecs_registry",
    ],
    # The file first: every other page in this chapter is about something the
    # file names but does not itself do. Then the interpreter itself, starting
    # with the smallest thing you can hand it -- one line after -c.
    "02_Projects_and_Environments": [
        "README.md",
        "pyproject_toml",
        "dash_c_is_not_the_prompt",
    ],
}

def _label(name: str) -> str:
    """Folder name on disk -> sidebar label."""
    words = PREFIX.sub("", name).replace("_", " ").replace("-", " ").split()
    out = [FIXUPS.get(w.capitalize(), w.capitalize()) for w in words]
    if out:
        out[0] = out[0][0].upper() + out[0][1:]
    return " ".join(out)


def _is_section(item) -> bool:
    return getattr(item, "children", None) is not None


def _first_src(item) -> str:
    """Source path of `item`, or of the first page anywhere beneath it."""
    page_file = getattr(item, "file", None)
    if page_file is not None:
        return page_file.src_uri
    for child in getattr(item, "children", None) or []:
        found = _first_src(child)
        if found:
            return found
    return ""


def _on_disk_name(item, depth: int) -> str:
    """The name NAV_ORDER lists this child by: a filename, or a folder segment."""
    src = _first_src(item)
    if not src:
        return (getattr(item, "title", "") or "").lower()
    parts = src.split("/")
    if not _is_section(item):
        return parts[-1]
    return parts[depth] if depth < len(parts) - 1 else parts[-1]


def _order_key(path: str, name: str) -> tuple[int, str]:
    listed = NAV_ORDER.get(path, [])
    if name in listed:
        return (listed.index(name), "")
    return (len(listed), name.lower())


def _readme_h1(section) -> str:
    """The H1 of a section's own README.md, read from disk ("" if it has none).

    Read from disk because MkDocs fills in a page's title only when it renders
    the page, long after `on_nav`. Backticks are dropped: the sidebar prints
    them as literal characters.
    """
    for child in section.children:
        page_file = getattr(child, "file", None)
        if page_file is None or page_file.src_uri.rsplit("/", 1)[-1] != "README.md":
            continue
        with open(page_file.abs_src_path, encoding="utf-8") as fh:
            for line in fh:
                if line.startswith("# "):
                    return line[2:].strip().replace("`", "")
    return ""


def _visit(items: list, path: str, depth: int) -> None:
    for child in items:
        if not _is_section(child):
            continue
        name = _on_disk_name(child, depth)
        # A numbered chapter folder is relabelled from its name. A lesson folder
        # takes its README's H1, which is authored prose, unless LABEL_OVERRIDES
        # names a label for it. Title-casing the folder name instead would fight
        # the page it points at ("Significant Figures").
        if name in LABEL_OVERRIDES:
            child.title = LABEL_OVERRIDES[name]
        elif PREFIX.match(name):
            child.title = _label(name)
        else:
            child.title = _readme_h1(child) or child.title

    items.sort(key=lambda c: _order_key(path, _on_disk_name(c, depth)))

    for child in items:
        if not _is_section(child):
            continue
        name = _on_disk_name(child, depth)
        _visit(child.children, f"{path}/{name}".lstrip("/"), depth + 1)


def on_nav(nav, config, files):
    """Relabel numbered chapters and apply NAV_ORDER, depth-first."""
    _visit(nav.items, "", 0)
    return nav


# ---------------------------------------------------------------------------
# Fenced TABs. Python-Markdown expands every TAB in a page to spaces --
# `expandtabs(4)`, in its NormalizeWhitespace preprocessor -- before any fence
# is parsed, so until 2026-09-10 no page on this site carried a TAB byte. That
# included the TAB print() writes on 01_Text_and_Bytes/repr_is_not_str, which
# arrived as spaces, while GitHub rendered the same Markdown with it intact.
#
# The fix is one line of mkdocs.yml: `preserve_tabs: true` on
# pymdownx.superfences, which lifts fences out ahead of that pass. Upstream
# calls the option experimental, and losing it would break nothing a build
# reports, so this is the check: a page whose fences hold N TABs in its
# Markdown must hold at least N in its HTML, or the build warns and `--strict`
# fails.
#
# Only closed fences at the left margin are counted, which is where every
# fenced TAB in the library sits. The option also keeps the TABs in a fence
# nested in a list or a blockquote; not counting those means they can make the
# check pass but never fail. "At least N" rather than N because the homepage
# inlines README.md through pymdownx.snippets, and an inlined fence's TABs are
# in the HTML without being in `page.markdown`.
# ---------------------------------------------------------------------------

FENCE_OPEN = re.compile(r"`{3,}|~{3,}")


def _fenced_tabs(markdown: str) -> int:
    """TABs inside the closed fences that start at the left margin."""
    total = pending = 0
    fence = None
    for line in markdown.split("\n"):
        if fence is None:
            m = FENCE_OPEN.match(line)
            if m:
                fence, pending = m.group(), 0
        elif re.fullmatch(rf"{fence[0]}{{{len(fence)},}}\s*", line):
            total += pending
            fence = None
        else:
            pending += line.count("\t")
    return total


def on_page_content(html, page, config, files):
    """Warn when a page's HTML holds fewer TABs than its fences did."""
    want = _fenced_tabs(page.markdown)
    got = html.count("\t")
    if got < want:
        log.warning(
            "Fenced TABs lost: %s has %d inside its fences and %d in its "
            "HTML. Is `preserve_tabs: true` still set on pymdownx.superfences?",
            page.file.src_uri,
            want,
            got,
        )
    return html


# ---------------------------------------------------------------------------
# Backticks in a fence title. CommonMark forbids a backtick in the info string
# of a BACKTICK fence, so on github.com a line like
#
#     ```text title="Real output — `cargo test`"
#
# is not a fence at all. Measured 2026-09-10 with `gh api markdown`: the opener
# renders as the start of a paragraph, and the block's closing ``` opens a new
# code block that runs to the next bare fence line. That swallowed the lesson's
# next paragraph after 21 of 24 such fences, and on the Rust library's
# 15_First_Programs/rustc_without_cargo everything to the end of the page.
# pymdownx.superfences accepts the form, so neither the site nor `--strict`
# ever showed it. The 24 were in the Rust and encodings libraries and came out
# on 2026-09-10 ("Drop the backticks from fence titles, which GitHub cannot
# parse"); none was here, and this check is what keeps it that way.
#
# Fences are tracked the CommonMark way: one closes on the first later line of
# its own character, at least as long, with nothing after it but whitespace.
# So the bad form shown INSIDE a longer or a ~~~ fence, which is how a page
# about the rule has to show it, is content and passes. A ~~~ fence may hold a
# backtick in its info string, and passes; so does a four-backtick ````rust
# fence, which a line grep for a backtick after the fence cannot tell from the
# real thing. Leading indentation and `>` are skipped, because GitHub reads a
# fence in a list item or a blockquote by the same rule. And a line that only
# starts with a code span, ```` ``` ```` say, is a paragraph on both surfaces
# -- superfences cannot read it as a fence header either -- so it passes too.
#
# README.md is excluded from the build, because index.md inlines it through
# pymdownx.snippets, yet it is the first page github.com shows. So a file a
# page inlines is scanned as well, whole, and named by its own path.
# ---------------------------------------------------------------------------

FENCE_LINE = re.compile(r"(?P<fence>`{3,}|~{3,})(?P<info>.*)")
# A `--8<-- "path"` line, as pymdownx.snippets reads one. A `:section` or
# `:start:end` suffix picks part of the file; the whole file is scanned.
SNIPPET = re.compile(r"""[ \t]*-+8<-+[ \t]+(["'])(?P<path>.+?)\1""")
BACKTICK_TITLE = (
    "Fence title holds a backtick: %s. GitHub does not read a ``` line whose "
    "info string contains one as a fence, so the block's closing ``` "
    "swallows what follows. Name the code bare, or open the fence with ~~~."
)

# The check's own cases, run on every build rather than behind a flag nobody
# passes: a scan that stops catching its own example fails the build instead
# of passing everything quietly.
BACKTICK_TITLE_CASES = [
    ("the title it exists for", '```text title="a `b` c"\nx\n```', [1]),
    ("the same title on a ~~~ fence", '~~~text title="a `b` c"\nx\n~~~', []),
    ("a bare four-backtick fence", "````rust\nfn f() {}\n````", []),
    ("the title shown inside a longer fence",
     '````markdown\n```text title="a `b` c"\nx\n```\n````', []),
    ("the title shown inside a ~~~ fence",
     '~~~markdown\n```text title="a `b` c"\nx\n```\n~~~', []),
    ("the title behind a blockquote's >",
     '> ```text title="a `b` c"\n> x\n> ```', [1]),
    ("the title indented in a list item",
     '1. Step\n\n    ```text title="a `b` c"\n    x\n    ```', [3]),
    ("a line starting with a code span, then the title",
     '```` ``` ```` opens a fence.\n\n```text title="a `b` c"\nx\n```', [3]),
    ("a fence only a bare line closes, then the title",
     '```\n```rust\n```\n```text title="a `b` c"\nx\n```', [4]),
]


def _backtick_titles(markdown: str) -> list[int]:
    """Line numbers of top-level ``` openers whose info string holds a backtick."""
    # superfences' own header pattern, which decides whether the site opens a
    # fence on that line. Imported here, not at the top, so that importing this
    # file still needs nothing beyond the standard library.
    from pymdownx.superfences import RE_NESTED_FENCE_START

    hits: list[int] = []
    fence = None
    for n, line in enumerate(markdown.split("\n"), 1):
        body = line.lstrip(" \t>")
        if fence is None:
            m = FENCE_LINE.match(body)
            if not m:
                continue
            if m["fence"][0] == "`" and "`" in m["info"]:
                header = RE_NESTED_FENCE_START.match(body)
                if header is None or header["unrecognized"]:
                    continue  # not a fence on the site either: a code span
                hits.append(n)
            fence = m["fence"]
        elif re.fullmatch(rf"{fence[0]}{{{len(fence)},}}[ \t]*", body):
            fence = None
    return hits


def _lines_above(page, markdown: str) -> int:
    """Lines MkDocs took off the top of the file before handing the rest over
    as `markdown` -- front matter, and the blank lines after it."""
    try:
        source = page.file.content_string
    except (OSError, ValueError):
        return 0
    if not markdown or not source.endswith(markdown):
        return 0
    return source[: len(source) - len(markdown)].count("\n")


def on_pre_build(config):
    """Warn if the fence-title scan has stopped passing its own cases."""
    for label, text, want in BACKTICK_TITLE_CASES:
        got = _backtick_titles(text)
        if got != want:
            log.warning(
                "The fence-title check is broken: on %s it reports lines %s, "
                "expected %s.",
                label,
                got,
                want,
            )


def on_page_markdown(markdown, page, config, files):
    """Warn once per fence title holding a backtick, here or in what it inlines."""
    src = page.file.src_uri
    skipped = _lines_above(page, markdown)
    for n in _backtick_titles(markdown):
        log.warning(BACKTICK_TITLE, f"{src}:{n + skipped}")
    inlined = {
        m["path"].split(":", 1)[0]
        for m in map(SNIPPET.fullmatch, markdown.split("\n"))
        if m
    }
    for rel in sorted(inlined):
        path = pathlib.Path(config["docs_dir"], rel)
        if path.is_file():
            for n in _backtick_titles(path.read_text(encoding="utf-8-sig")):
                log.warning(BACKTICK_TITLE, f"{rel}:{n}, inlined into {src}")
    return markdown
