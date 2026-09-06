# Normalization

**Level:** 201 · for Python programmers

> **Stub — an outline, not a lesson.** There is no runnable example behind this page yet, so nothing on it has been through [the check that backs every other claim in this library](../../CONTRIBUTING.md). The bullets below are the questions the finished page has to answer.

**One line:** `café` and `café` can be two different strings that render identically, and `unicodedata.normalize()` is what you run before comparing anything that came from outside your process.

- What are NFC, NFD, NFKC and NFKD, and which one do you actually want? (NFC for storage and comparison; NFKC only when you accept that `ﬁ` becomes `fi` and `²` becomes `2`.)
- Why does macOS hand back NFD from the filesystem while nearly everything else uses NFC?
- What is `str.casefold()` and why is it not `str.lower()`? (`ß` → `ss`, and the length changes.)
- The comparison recipe: normalize, then casefold, then compare — in that order, and why the order matters.
- Where does this bite in real data — a filename against a database row, a deduplication pass, a login form.

## See also

- [Counting characters](../counting_characters/README.md) — where the NFC/NFD length difference first shows up
- [Sorting is not comparing](../sorting_is_not_comparing/README.md)
