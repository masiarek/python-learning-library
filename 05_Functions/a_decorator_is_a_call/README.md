# A decorator is a call, made when `def` runs

**Level:** 201 · for Python programmers

> **Stub — an outline, not a lesson.** There is no runnable example behind this page yet, so nothing on it has been through [the check that backs every other claim in this library](../../CONTRIBUTING.md). The bullets below are the questions the finished page has to answer.

**One line:** `@deco` above `def f` means `f = deco(f)`, executed once when the `def` statement runs, so a decorator that forgets to return a function leaves `f` as `None`, one that forgets `functools.wraps` renames every function it touches to `wrapper`, and a decorator with arguments is three calls rather than one.

## What the finished page has to answer

- The desugaring, and when it runs: at import for a module-level function, once, which is why a decorator that prints does so before `main` starts and why a decorator that registers its function into a list is a side effect of importing.
- Stacked decorators apply bottom-up, and the order shows in the result.
- What is lost without `functools.wraps`: `__name__`, `__doc__`, `__module__`, `__qualname__`, the annotations, and `inspect.signature`, which follows `__wrapped__` only if `wraps` set it. Measured on a decorated function with and without.
- A decorator with arguments: a function that returns a decorator that returns a wrapper, so `@retry(3)` is a call at `def` time, then another, then one per call.
- `@staticmethod`, `@classmethod` and `@property` are ordinary decorators whose return values are descriptors, which is the classes chapter's subject. A decorator applied to a method receives the plain function, before any binding to an instance.
- A decorator is a closure factory, so [A closure captures the variable, not the value](../a_closure_captures_the_variable/README.md) applies to whatever it captured.
- Where the cost lands: one extra Python call per call, and `functools.cache` as the decorator that pays for itself.

## See also

- [A closure captures the variable, not the value](../a_closure_captures_the_variable/README.md): the mechanism a wrapper is built from
- [Function definitions ↗](https://docs.python.org/3/reference/compound_stmts.html#function-definitions) in the language reference, which gives the desugaring, [`functools.wraps` ↗](https://docs.python.org/3/library/functools.html#functools.wraps), and [PEP 318 ↗](https://peps.python.org/pep-0318/)
- [What an attribute is ↗](https://masiarek.github.io/rust-learning-library/27_Modules/what_an_attribute_is/index.html) in the Rust library: `#[…]` looks like `@…` and is the opposite thing, read by the compiler rather than run by the interpreter
