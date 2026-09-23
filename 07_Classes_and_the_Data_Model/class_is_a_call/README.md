# `class` is a call

**Level:** 301 · for Python programmers, especially ones coming from ABAP, Rust or C

> **Stub — an outline, not a lesson.** There is no runnable example behind this page yet, so nothing on it has been through [the check that backs every other claim in this library](../../CONTRIBUTING.md). The bullets below are the questions the finished page has to answer.

**One line:** A `class` statement runs its body top to bottom like a function, collects the names it bound into a dict, and calls `type(name, bases, dict)` — so a class is an object made at run time, a class decorator or a metaclass is only a different callee, and `__init_subclass__` gets you most of what a metaclass does without writing one.

## What the finished page has to answer

- `type(C) is type`, and `type('C', (Base,), {'x': 1})` making the same class the statement would, measured side by side.
- The body is code: a `print`, a loop or an `if` in a class body runs when the class is made, once, at import.
- The hooks in the order they fire: `__prepare__`, the body, `__set_name__` on each descriptor, `__init_subclass__` on the parent, then the metaclass's `__new__` and `__init__`, and later `__call__` on every instantiation, which is where a singleton or an instance cache lives.
- `__init_subclass__` (PEP 487) as the ordinary tool for registries and validation, and the short list of things that still need a metaclass.
- A class is a value: kept in a dict, returned from a function, made in a loop. [A decorator is a call](../../05_Functions/a_decorator_is_a_call/README.md) applies to `@dataclass` and to every other class decorator.
- The contrast that makes the page: in ABAP a class is a repository object activated before anything runs, in Rust and C a type does not exist at run time at all.

## See also

- [A decorator is a call, made when `def` runs](../../05_Functions/a_decorator_is_a_call/README.md): the function-side version of a callee you did not see
- [Customizing class creation ↗](https://docs.python.org/3/reference/datamodel.html#customizing-class-creation) in the language reference, [`type` ↗](https://docs.python.org/3/library/functions.html#type), and [PEP 487 ↗](https://peps.python.org/pep-0487/)
- [A type is not a constructor ↗](https://masiarek.github.io/rust-learning-library/16_Structs/a_type_is_not_a_constructor/index.html) in the Rust library: the other end of the same axis
