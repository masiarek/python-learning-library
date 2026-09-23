# `@dataclass` writes the methods

**Level:** 201 → 301 · for Python programmers

> **Stub — an outline, not a lesson.** There is no runnable example behind this page yet, so nothing on it has been through [the check that backs every other claim in this library](../../CONTRIBUTING.md). The bullets below are the questions the finished page has to answer.

**One line:** `@dataclass` reads the class's annotations and writes `__init__`, `__repr__` and `__eq__` for you, and nothing else unless asked — no ordering without `order=True`, no hash unless frozen, no `__slots__` without `slots=True`, no type check ever — while it refuses a mutable *default* and accepts a mutable *field* without a word.

## What the finished page has to answer

- What was written, shown with `inspect.signature(C.__init__)` and `vars(C)` before and after; and the rule that a field without a default cannot follow one with, which is `TypeError` at class creation.
- `field()`: `default_factory`, `init=False`, `repr=False`, `compare=False`, `kw_only=True`; `__post_init__` for the derived field.
- `frozen=True`: assignment raises `FrozenInstanceError`, a subclass of `AttributeError`, and the hash comes back, which [Defining `__eq__` deletes `__hash__`](../defining_eq_deletes_hash/README.md) section 6 measures.
- `order=True` compares field tuples in declaration order, and refuses to coexist with a hand-written `__lt__`.
- `slots=True` (3.10) and what it changes about [A class attribute is shared](../a_class_attribute_is_shared/README.md) section 6.
- `asdict` and `astuple` copy deeply, `replace` makes a new instance, and `fields()` is the list the decorator worked from, which is why an unannotated name is not in it.
- Types are not checked, ever: `C('a')` when the field says `int` runs, which is [Annotations are not checked](../../05_Functions/annotations_are_not_checked/README.md) from the class's side.

## See also

- [Defining `__eq__` deletes `__hash__`](../defining_eq_deletes_hash/README.md), [A class attribute is shared](../a_class_attribute_is_shared/README.md) and [A default is computed once](../../05_Functions/a_default_is_computed_once/README.md): three pages that each measure one of the decorator's decisions
- [`dataclasses` ↗](https://docs.python.org/3/library/dataclasses.html) in the Python docs, and [PEP 557 ↗](https://peps.python.org/pep-0557/)
- [Representing a record ↗](https://masiarek.github.io/rust-learning-library/16_Structs/representing_a_record/index.html) in the Rust library, where `#[derive]` writes the same methods and the compiler checks the types the decorator here never does
