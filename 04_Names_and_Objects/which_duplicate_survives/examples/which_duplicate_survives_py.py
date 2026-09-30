#!/usr/bin/env python3
"""Which duplicate survives: every way to deduplicate makes two choices.

Run:  python3 which_duplicate_survives_py.py

Removing duplicates sounds like one operation. It is two decisions: which
of the equal items stands for the group (the first seen, the last seen, an
arbitrary one), and what order the survivors come out in (first-seen,
sorted, or whatever a hash table does). Each Python idiom makes both
choices silently, and a few make them in combinations nobody would pick on
purpose, like keeping the last spelling at the first position. Every set
is printed sorted; exceptions are printed by type name only.
"""

from itertools import groupby


def main() -> None:
    words = ["Pear", "fig", "pear", "Fig", "apple", "PEAR"]
    print("1. THE LIST, AND WHAT 'THE SAME' MEANS")
    print(f"   words = {words}")
    print("   Exact duplicates: none. Duplicates ignoring case: pear x3, fig x2.")
    print()

    print("2. EXACT DUPLICATES: FIVE IDIOMS, FOUR ORDERS")
    nums = [3, 1, 3, 2, 1, 3]
    print(f"   nums = {nums}")
    seen, first_seen = set(), []
    for n in nums:
        if n not in seen:
            seen.add(n)
            first_seen.append(n)
    rows = [
        ("list(set(nums))", list(set(nums)), "hash order: here it looks sorted, by luck"),
        ("sorted(set(nums))", sorted(set(nums)), "sorted, on purpose"),
        ("list(dict.fromkeys(nums))", list(dict.fromkeys(nums)), "first-seen order"),
        ("seen-set loop", first_seen, "first-seen order, the long way"),
        ("[k for k, _ in groupby(nums)]", [k for k, _ in groupby(nums)], "adjacent repeats only"),
    ]
    for code, result, note in rows:
        print(f"   {code:<30} {str(result):<18} {note}")
    print("   groupby, like Rust's dedup and ABAP's DELETE ADJACENT DUPLICATES,")
    print("   only merges neighbours: sort first, or it removes nothing useful.")
    print()

    print("3. DUPLICATES BY A KEY: WHICH SPELLING SURVIVES?")
    by_key_last = list({w.lower(): w for w in words}.values())
    first = {}
    for w in words:
        first.setdefault(w.lower(), w)
    by_key_first = list(first.values())
    print(f"   {{w.lower(): w for w in words}}.values()   {by_key_last}")
    print("     keys keep their FIRST position, values are overwritten by the LAST:")
    print("     'PEAR' sits where 'Pear' was. Nobody chose that combination.")
    print(f"   d.setdefault(w.lower(), w)               {by_key_first}")
    print("     setdefault never overwrites, so the first spelling wins, in first place.")
    srt = sorted(words, key=str.lower)
    grouped = [next(g) for _, g in groupby(srt, key=str.lower)]
    print(f"   sort by key, then groupby, take first     {grouped}")
    print("     sorted order, and the first of each run: sorted() is stable, so that")
    print("     is also the first seen. ABAP's SORT ... STABLE + DELETE ADJACENT")
    print("     DUPLICATES COMPARING and Rust's sort_by_key + dedup_by_key do the same.")
    print()

    print("4. EQUAL IS NOT IDENTICAL: THE SURVIVOR KEEPS ITS TYPE")
    mixed = [1.0, 1, True, 2]
    for code in ["set(mixed)", "list(dict.fromkeys(mixed))", "list(dict.fromkeys(reversed(mixed)))"]:
        print(f"   {code:<38} {eval(code, {'mixed': mixed})}")
    print(f"   mixed = {mixed}: 1.0, 1 and True are equal and hash alike, so they are")
    print("   one member, and whichever arrives first is the one you keep.")
    print()

    print("5. UNHASHABLE ITEMS")
    rows_ = [[1, 2], [3], [1, 2]]
    try:
        set(rows_)
        outcome = "worked"
    except TypeError as e:
        outcome = type(e).__name__
    print(f"   set({rows_}) -> {outcome}")
    as_tuples = list(dict.fromkeys(map(tuple, rows_)))
    print(f"   list(dict.fromkeys(map(tuple, rows)))  -> {as_tuples}   hash a frozen copy")
    slow = []
    for r in rows_:
        if r not in slow:
            slow.append(r)
    print(f"   'if r not in out: out.append(r)'        -> {slow}   works on anything, but")
    print("   each 'in' scans the list: fine for ten items, quadratic for a million.")


if __name__ == "__main__":
    main()
