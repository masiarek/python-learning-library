# An `Enum` member is not its value

**Level:** 201 · for Python programmers

> **Stub — an outline, not a lesson.** There is no runnable example behind this page yet, so nothing on it has been through [the check that backs every other claim in this library](../../CONTRIBUTING.md). The bullets below are the questions the finished page has to answer.

**One line:** `Color.RED` is an object, `Color.RED == 1` is `False` unless the class is an `IntEnum`, `Color(1)` looks a member up by value and `Color['RED']` by name, two members with one value are one member and an alias, and iteration yields each member once, in definition order.

## What the finished page has to answer

- Members are singletons, so `is` is the honest comparison and `==` between members works because of it; `.name` and `.value`; `auto()`.
- Aliases: a second member with the same value *is* the first, `@unique` to forbid it, and what iteration and `len()` do with an alias.
- `IntEnum` and `StrEnum` (3.11): comparable with plain values, sortable, and written by `json.dumps` as their value where a plain `Enum` member raises `TypeError`, which is [`json` is not Python](../json_is_not_python/README.md) section 2.
- `Flag` and the bitwise operators, and what a combination that is not a named member prints as.
- `match` on an enum: `case Color.RED:` is a value pattern, and `case RED:` binds a new name to anything, which is the one place the dotted spelling is load-bearing.
- Members cannot be instantiated or subclassed once the enum has members, and why.

## See also

- [`json` is not Python](../json_is_not_python/README.md): a plain member has no spelling
- [`is` is not `==`](../../04_Names_and_Objects/is_is_not_equals/README.md): why members compare by identity
- [`enum` ↗](https://docs.python.org/3/library/enum.html) in the library reference and the [enum HOWTO ↗](https://docs.python.org/3/howto/enum.html)
- [What an enum is ↗](https://masiarek.github.io/rust-learning-library/13_Enums/what_an_enum_is/index.html) in the Rust library, where a variant is a type of its own and the compiler checks the `match`
