#!/usr/bin/env python3
"""Answers to the kata on 'A set is a hash table': run each line, print it.

Run:  python3 a_set_is_a_hash_table_kata_py.py

Every set is printed sorted, because a set's own order is not part of it.
Exceptions are printed by type name, which CPython does not reword.
"""


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
    ]
    for n, code in enumerate(lines, 1):
        try:
            result = show(eval(code, dict(env)))
        except Exception as e:
            result = type(e).__name__
        print(f"{n:>2}. {code:<50} {result}")


if __name__ == "__main__":
    main()
