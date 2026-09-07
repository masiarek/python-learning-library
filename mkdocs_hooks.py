"""Build-time fixes that would otherwise cost a pinned plugin dependency.

Two jobs, both about the sidebar:

1. **Clean chapter labels.** MkDocs derives a section label from the folder name
   on disk, so `01_Bits_and_Bytes/` reads as "01 Bits And Bytes". The numeric prefix exists
   to set reading order in a file listing; it should not be visible in the nav.
   Only *prefixed* folders are relabelled — a lesson folder takes its label from
   its page's own H1, which is already written the way it should read.

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
"""

from __future__ import annotations

import re

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

# Reading order per folder path. Children named by on-disk name; anything not
# listed sorts alphabetically after the listed ones.
NAV_ORDER: dict[str, list[str]] = {
    "": [
        "index.md",
        "00_Start_Here",
        "01_Text_and_Bytes",
        "02_Projects_and_Environments",
        "CROSSWALK.md",
        "GLOSSARY.md",
        "RESOURCES.md",
        "ROADMAP.md",
        "TODO.md",
    ],
    # The type boundary first, then the two doors, then the constructor that
    # quietly is one of them, then the five places code points mislead you,
    # then the two boundaries with the outside world.
    "01_Text_and_Bytes": [
        "README.md",
        "str_is_not_bytes",
        "encode_and_decode",
        "making_a_bytes_object",
        "bytearray_is_mutable",
        "opening_a_file",
        "counting_characters",
        "is_it_a_letter",
        "repr_is_not_str",
        "what_ends_a_line",
        "strip_is_a_set",
        "the_format_mini_language",
        "normalization",
        "sorting_is_not_comparing",
        "stdin_stdout_and_pipes",
        "filenames_are_not_text",
        "what_kind_of_file_is_this",
    ],
    # The file first: every other page in this chapter is about something the
    # file names but does not itself do.
    "02_Projects_and_Environments": [
        "README.md",
        "pyproject_toml",
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


def _visit(items: list, path: str, depth: int) -> None:
    for child in items:
        if not _is_section(child):
            continue
        name = _on_disk_name(child, depth)
        # Only a numbered chapter folder gets relabelled. A lesson folder's
        # section label already comes from its page H1, which is authored prose;
        # title-casing it here would turn "Significant figures" into
        # "Significant Figures" and fight the page it points at.
        if PREFIX.match(name):
            child.title = _label(name)

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
