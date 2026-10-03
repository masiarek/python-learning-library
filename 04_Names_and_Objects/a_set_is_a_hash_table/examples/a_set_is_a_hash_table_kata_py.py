#!/usr/bin/env python3
"""Answers to the kata on 'A set is a hash table': run each line, print it.

Run:  python3 a_set_is_a_hash_table_kata_py.py

Every set is printed sorted, because a set's own order is not part of it.
Exceptions are printed by type name, which CPython does not reword.
Lines 12 to 15 are four precedence katas; the second part tries every
bracketing of two of them, to show which readings the answer rules out.
"""

from operator import and_, or_, sub, xor


OPS = {"|": or_, "&": and_, "^": xor, "-": sub}


def bracketings(operands, ops):
    """Every full bracketing of operands joined by ops, as (text, value) pairs."""
    if not ops:
        return [operands[0]]
    out = []
    for k in range(len(ops)):
        for left in bracketings(operands[: k + 1], ops[:k]):
            for right in bracketings(operands[k + 1 :], ops[k + 1 :]):
                out.append((f"({left[0]} {ops[k]} {right[0]})", OPS[ops[k]](left[1], right[1])))
    return out


def count_same(expr: str, env: dict) -> int:
    """How many full bracketings of expr give the set Python's own reading gives."""
    tokens = expr.split()
    operands = [(t, env[t]) for t in tokens if t.isalpha()]
    ops = [t for t in tokens if t in OPS]
    python = eval(expr, {}, dict(env))
    return sum(1 for _, value in bracketings(operands, ops) if value == python)


def show(value) -> str:
    if isinstance(value, (set, frozenset)):
        return "{" + ", ".join(repr(x) for x in sorted(value)) + "}" if value else "set()"
    return repr(value)


def main() -> None:
    s1, s2 = {"a", "b", "c"}, {"c", "d", "e"}
    env = {"s1": s1, "s2": s2}
    lines = [
        "s1 | s2",
        "s1.intersection(s2)",
        "s1 ^ s2",
        "len({True, 1, 1.0, '1'})",
        "set((1, 2, 3)) & set((2, 3, 4)) & set((3, 4, 5))",
        "{1, 2, 3} ^ {3, 4, 5} ^ {5, 6, 7} ^ {7, 8, 1}",
        "{1} ^ {1} ^ {1}",
        "s1 | ['z']",
        "s1.union(['z'])",
        "set().issubset([])",
        "type({})",
        "{1, 2, 3} | {3, 4, 5} & {5, 6, 7}",
        "{1, 2, 3, 4} - {3, 4, 5} & {4, 5, 6}",
        "{1, 2} | {2, 3} ^ {1, 2} & {2, 4}",
        "{1, 2} | {2, 3} ^ {1, 3} - {3, 4} & {1, 4}",
    ]
    for n, code in enumerate(lines, 1):
        try:
            result = show(eval(code, dict(env)))
        except Exception as e:
            result = type(e).__name__
        print(f"{n:>2}. {code:<50} {result}")

    print()
    print("Lines 14 and 15 under every bracketing; Python's is marked.")
    A, B, C = frozenset({1, 2}), frozenset({2, 3}), frozenset({2, 4})
    print("Line 14 as A | B ^ A & C with A = {1, 2}, B = {2, 3}, C = {2, 4}:")
    python = A | B ^ A & C
    for text, value in bracketings([("A", A), ("B", B), ("A", A), ("C", C)], ["|", "^", "&"]):
        mark = "  Python: & first, then ^, then |" if text == "(A | (B ^ (A & C)))" else ""
        print(f"   {text:<24} {show(set(value)):<12}{mark}".rstrip())
    same = count_same("A | B ^ A & C", dict(A=A, B=B, C=C))
    same_was = count_same("A | B ^ A & C", dict(A=A, B=B, C=frozenset({3, 4})))
    print(f"   {same} of 5 bracketings gives {show(set(python))}; with C = {{3, 4}}, {same_was} of 5 do, because")
    print("   A & C is then set() and B ^ set() is B: the ^ step does nothing.")
    A, B, C, D, E = (frozenset(s) for s in ({1, 2}, {2, 3}, {1, 3}, {3, 4}, {1, 4}))
    print("Line 15 as A | B ^ C - D & E with A = {1, 2}, B = {2, 3}, C = {1, 3}, D = {3, 4}, E = {1, 4}:")
    print(f"   Python reads (A | (B ^ ((C - D) & E))) = {show(set(A | B ^ C - D & E))}: - first, then &, then ^, then |")
    same = count_same("A | B ^ C - D & E", dict(A=A, B=B, C=C, D=D, E=E))
    same_was = count_same("A | B ^ C - A & D", dict(A=A, B=B, C=frozenset({3, 4}), D=frozenset({2, 4})))
    print(f"   {same} of 14 bracketings gives {show(set(A | B ^ C - D & E))}; as first written, A | B ^ C - A & D with")
    print(f"   C = {{3, 4}} and D = {{2, 4}}, {same_was} of 14 did: (C - A) & D is disjoint from A, and then")
    print("   (A | B) ^ X == A | (B ^ X), so ^ against | could never show.")


if __name__ == "__main__":
    main()
