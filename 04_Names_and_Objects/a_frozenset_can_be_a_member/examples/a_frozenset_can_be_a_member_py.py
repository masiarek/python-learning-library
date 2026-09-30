#!/usr/bin/env python3
"""A frozenset can be a member: the one reason Python has two set types.

Run:  python3 a_frozenset_can_be_a_member_py.py

A set can change after it is made, so its hash could change while it sits
inside another set or a dict, and the container would look in the wrong
place. Python therefore refuses to hash a set, and supplies frozenset: the
same set, minus every method that changes it, and therefore hashable. The
program shows what that buys (sets of sets, sets as dict keys), what it
costs (no add; |= builds a new object), and the one place Python quietly
converts a set for you: set membership, but not dict lookup. Every set is
printed sorted; exceptions are printed by type name only.
"""

from itertools import combinations


def show(s) -> str:
    """A set or frozenset, nested or not, in braces and a stable order."""
    if not isinstance(s, (set, frozenset)):
        return repr(s)
    if not s:
        return "{}"
    items = sorted(s, key=lambda v: (len(v), sorted(v)) if isinstance(v, frozenset) else (0, [v]))
    return "{" + ", ".join(show(x) for x in items) + "}"


def attempt(fn) -> str:
    try:
        return show(fn())
    except Exception as e:
        return type(e).__name__


def main() -> None:
    print("1. A SET CANNOT BE A MEMBER; A FROZENSET CAN")
    print(f"   {{{{1, 2}}, {{3}}}}                      -> {attempt(lambda: eval('{{1, 2}, {3}}'))}")
    sets = {frozenset({1, 2}), frozenset({3})}
    print(f"   {{frozenset({{1, 2}}), frozenset({{3}})}} -> {show(sets)}")
    power = {frozenset(c) for r in range(4) for c in combinations([1, 2, 3], r)}
    print(f"   every subset of {{1, 2, 3}}, as a set of frozensets: {len(power)} members")
    print(f"     {show(power)}")
    print("   The set of all subsets needs sets as members, and so needs frozenset.")
    print()

    print("2. SAME MEMBERS, SAME HASH, WHATEVER THE ORDER")
    a, b = frozenset([1, 2, 3]), frozenset([3, 2, 1])
    print(f"   frozenset([1, 2, 3]) == frozenset([3, 2, 1])            {a == b}")
    print(f"   hash(frozenset([1, 2, 3])) == hash(frozenset([3, 2, 1])) {hash(a) == hash(b)}")
    print(f"   frozenset({{1, 2}}) == {{1, 2}}                           {frozenset({1, 2}) == {1, 2}}")
    seen = {}
    for combo in [(1, 2), (2, 1), (1, 3), (3, 1), (2, 1)]:
        key = frozenset(combo)
        seen[key] = seen.get(key, 0) + 1
    print("   counting unordered pairs with frozenset keys:")
    for key in sorted(seen, key=sorted):
        print(f"     {show(key):<8} seen {seen[key]} times")
    print("   A pair and its reverse are one key: that is what an unordered pair is.")
    print()

    print("3. WHAT IT COSTS: NOTHING THAT CHANGES IT")
    f = frozenset({1, 2})
    print(f"   f.add(3)             -> {attempt(lambda: f.add(3))}")
    print(f"   f.union([3])         -> {attempt(lambda: f.union([3]))}   a new frozenset; f is still {show(f)}")
    print(f"   f.copy() is f        -> {f.copy() is f}   no copy needed for something that cannot change")
    t = frozenset({1})
    u = t
    t |= {2}
    print(f"   t = frozenset({{1}}); u = t; t |= {{2}}  ->  t = {show(t)}, u = {show(u)}, t is u: {t is u}")
    print("   |= on a frozenset builds a new object and rebinds t; u still sees the old one.")
    print(f"   type(frozenset({{1}}) | {{2}}) = {type(frozenset({1}) | {2}).__name__},"
          f"  type({{2}} | frozenset({{1}})) = {type({2} | frozenset({1})).__name__}   the left operand decides")
    print()

    print("4. THE ONE PLACE PYTHON FREEZES A SET FOR YOU")
    print(f"   {{1, 2}} in sets                 -> {attempt(lambda: {1, 2} in sets)}")
    s2 = set(sets)
    s2.remove({3})
    print(f"   sets.remove({{3}})               -> leaves {show(s2)}")
    print("   set membership, remove and discard accept a set argument and look it up")
    print("   as if it were frozen, although {1, 2} itself is unhashable.")
    d = {frozenset({1, 2}): "pair"}
    print(f"   d = {{frozenset({{1, 2}}): 'pair'}};  d[{{1, 2}}]  -> {attempt(lambda: d[{1, 2}])}")
    print(f"   d[frozenset({{2, 1}})]           -> {d[frozenset({2, 1})]!r}")
    print("   A dict does not do the conversion: freeze the key yourself.")


if __name__ == "__main__":
    main()
