#!/usr/bin/env python3
"""Answers to the kata on 'Which duplicate survives'.

Run:  python3 which_duplicate_survives_kata_py.py
"""

from itertools import groupby


def main() -> None:
    names = ["ann", "Bob", "ANN", "bob", "cy", "Ann"]
    env = {"names": names, "groupby": groupby}
    lines = [
        "sorted(set(names))",
        "list(dict.fromkeys(names))",
        "list(dict.fromkeys(n.lower() for n in names))",
        "list({n.lower(): n for n in names}.values())",
        "[k for k, _ in groupby(['b', 'a', 'a', 'b', 'b'])]",
        "list(dict.fromkeys([1, 1.0, True]))",
        "list(dict.fromkeys([True, 1.0, 1]))",
        "len(set([0, 0.0, False, '', None]))",
    ]
    for n, code in enumerate(lines, 1):
        print(f"{n}. {code:<48} {eval(code, env)}")


if __name__ == "__main__":
    main()
