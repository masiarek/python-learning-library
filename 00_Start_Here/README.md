# Start here

**Level:** 101 · for anyone starting from zero

**One line:** This library teaches Python one idea per page, and every claim on every page is backed by a stdlib-only program that runs in CI and is checked against its recorded output — so nothing here can quietly go stale.

## What this is

A learning library about **Python**, built the same way as its [siblings](../CROSSWALK.md): one folder per idea, a page that makes a claim, and a program that proves it. The programs use nothing but the standard library, so you can run any page with the `python3` already on your machine.

It starts with **text and bytes** rather than with syntax, for a specific reason. Most Python tutorials cover `str` in an afternoon and move on. But the text model is where a wrong mental picture survives longest before failing — and when it fails, it fails on someone else's data, in production, in a country whose alphabet you didn't test with. It is also the part of Python that differs most from C, ABAP and Rust, so it is where cross-referencing the other libraries pays.

## Can you do these four things?

A diagnostic, not a test. Each one is a checkpoint, and each has a page.

1. **Say what `len()` counts, and name a case where two "obviously equal" strings compare `False`.** → [Counting characters](../01_Text_and_Bytes/counting_characters/README.md)
2. **Explain which of `.encode()` and `.decode()` you can call on a `str`, without guessing.** → [Encode and decode](../01_Text_and_Bytes/encode_and_decode/README.md)
3. **Say what encoding `open("data.txt")` uses on your machine, and on a colleague's.** → [Opening a file](../01_Text_and_Bytes/opening_a_file/README.md)
4. **Sort a list of Polish names correctly, and say what you traded to do it.** → [Sorting is not comparing](../01_Text_and_Bytes/sorting_is_not_comparing/README.md)

If all four are comfortable, chapter 1 is revision — skim the crosswalk instead and wait for chapter 2.

## How to run anything here

Every example is a plain file with no dependencies:

```bash
python3 01_Text_and_Bytes/sorting_is_not_comparing/examples/sorting_is_not_comparing_py.py
```

To check that every page still matches what its program prints — which is what CI does on both Ubuntu and macOS:

```bash
python3 tools/run_examples.py --check
```

## The reading order

1. [Text and bytes](../01_Text_and_Bytes/README.md) — the whole of chapter 1
2. [The crosswalk](../CROSSWALK.md) — the same ideas in Rust, C and ABAP
3. [Roadmap](../ROADMAP.md) — what is written, what is a stub, and what is next
