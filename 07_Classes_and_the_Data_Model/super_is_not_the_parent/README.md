# `super()` is not the parent

**Level:** 301 · for Python programmers

> **Stub — an outline, not a lesson.** There is no runnable example behind this page yet, so nothing on it has been through [the check that backs every other claim in this library](../../CONTRIBUTING.md). The bullets below are the questions the finished page has to answer.

**One line:** `super()` returns the *next class in the instance's method resolution order*, not the base class named in the `class` line, so with more than one base a `super().__init__()` can land in a sibling — which is what makes cooperative `__init__` work across a diamond, and what breaks it when one class in the chain forgets to call `super()`.

## What the finished page has to answer

- `C.__mro__` for a diamond, and the C3 rule that produced it: a class before its bases, and the bases in the order written.
- The measured surprise: `class D(B, C)` where `B.__init__` calls `super().__init__()` and lands in `C`, not in the shared base.
- Cooperative methods: every class in the chain calls `super()`, passes on the keyword arguments it does not use, and the one that does not is the one that silently ends the chain.
- The zero-argument form is compiler magic, a `__class__` cell filled in for functions defined in a class body, which is why `super()` in a function defined outside the class raises `RuntimeError`, and what the two-argument form is for.
- Mixins as the design this exists for, and `__init_subclass__` as the hook that replaces many of them.
- What the MRO decides beyond `super()`: which method `obj.m()` finds, which is [`obj.x` is a search](../attribute_lookup_is_a_search/README.md) across bases.

## See also

- [`obj.x` is a search](../attribute_lookup_is_a_search/README.md): the lookup that walks the same order
- [`super()` ↗](https://docs.python.org/3/library/functions.html#super) in the Python docs, [The Python 2.3 method resolution order ↗](https://docs.python.org/3/howto/mro.html), and Raymond Hettinger's [Python's `super()` considered super! ↗](https://rhettinger.wordpress.com/2011/05/26/super-considered-super/)
- [Supertraits ↗](https://masiarek.github.io/rust-learning-library/12_Traits/supertraits/index.html) in the Rust library: a language with no inheritance, and what it does where Python would reach for `super()`
