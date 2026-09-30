#!/usr/bin/env python3
"""Answers to the kata on 'A frozenset can be a member'.

Run:  python3 a_frozenset_can_be_a_member_kata_py.py
"""


def main() -> None:
    lines = [
        "len({frozenset({1, 2}), frozenset({2, 1})})",
        "frozenset({1, 2}) == {2, 1}",
        "{1, 2} in {frozenset({1, 2})}",
        "{frozenset({1, 2}): 'x'}[{1, 2}]",
        "type(frozenset({1}) & {1, 2}).__name__",
        "type({1, 2} & frozenset({1})).__name__",
        "len({frozenset(), frozenset(set())})",
        "frozenset('abca') == frozenset('cab')",
    ]
    for n, code in enumerate(lines, 1):
        try:
            result = repr(eval(code))
        except Exception as e:
            result = type(e).__name__
        print(f"{n}. {code:<42} {result}")


if __name__ == "__main__":
    main()
