# Annotations are not checked

**Level:** 201 · for Python programmers, especially ones coming from Rust, C or ABAP

> **Stub — an outline, not a lesson.** There is no runnable example behind this page yet, so nothing on it has been through [the check that backs every other claim in this library](../../CONTRIBUTING.md). The bullets below are the questions the finished page has to answer.

**One line:** `def f(x: int)` accepts a string, because an annotation is stored and never enforced: the checker that reads it is a separate program, and at run time `typing` is mostly a way of writing things down — which is why a `TypedDict` is a plain `dict`, `typing.cast` does nothing, and `isinstance(x, list[int])` raises.

## What the finished page has to answer

- `f('a')` runs. Where the annotation went: `f.__annotations__`, and `typing.get_type_hints`.
- When the annotation expression is evaluated, which is three regimes and has to be a dated table: eagerly at `def` time through 3.13, as strings under `from __future__ import annotations`, and lazily since 3.14 under PEP 649 and PEP 749, where a forward reference that used to raise `NameError` at `def` time no longer does.
- What the run time does with `typing` objects: `list[int]` is a `types.GenericAlias` you can print but not `isinstance` against; a `Protocol` is checked only if `runtime_checkable`, and then by method names alone; `NewType` returns its argument; `TypedDict` and `NamedTuple` are `dict` and `tuple` at run time.
- What does check: mypy, pyright and their relatives, run separately, none of them in the standard library, which is why this library cannot run one in CI and the page will have to show a checker's output as a dated fence.
- What annotations *are* used for at run time: `dataclasses` reads them to find its fields and still checks nothing, `functools.singledispatch` dispatches on them, and frameworks build validators from them.
- The contrast that makes the page worth writing: in Rust, C and ABAP a type is a fact the compiler enforces; in Python it is a claim a tool may verify.

## See also

- [A default is computed once](../a_default_is_computed_once/README.md): the other thing that happens at `def` time
- [`typing` ↗](https://docs.python.org/3/library/typing.html) and the [annotations best-practices HOWTO ↗](https://docs.python.org/3/howto/annotations.html) in the Python docs
- [PEP 649 ↗](https://peps.python.org/pep-0649/) and [PEP 749 ↗](https://peps.python.org/pep-0749/): the 3.14 change
