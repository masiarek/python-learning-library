# `obj.x` is a search

**Level:** 301 · for Python programmers

> **Stub — an outline, not a lesson.** There is no runnable example behind this page yet, so nothing on it has been through [the check that backs every other claim in this library](../../CONTRIBUTING.md). The bullets below are the questions the finished page has to answer.

**One line:** Reading `obj.x` walks a fixed path — a data descriptor on the type, then the instance's own `__dict__`, then the type and its bases, then `__getattr__` — so a `@property` beats an instance attribute of the same name, a plain class attribute loses to one, and `__getattr__` runs only after everything else has failed, which is the whole difference between it and `__getattribute__`.

## What the finished page has to answer

- The order, as `object.__getattribute__` implements it, measured with a class that has all four kinds of `x` at once.
- What a descriptor is: an object on the *type* with `__get__`, and, if it also has `__set__` or `__delete__`, a *data* descriptor that wins over the instance dict. `property` is one; a plain function is a non-data descriptor, which is why `obj.method` is a fresh bound-method object on every access and `a.f is a.f` is `False`.
- `__slots__` as data descriptors, which is why [A class attribute is shared](../a_class_attribute_is_shared/README.md) section 6 raises when a slot and a class attribute share a name.
- `__getattr__` against `__getattribute__`: the first is a fallback for the miss, the second replaces the search and recurses into itself if written carelessly.
- `hasattr` catches `AttributeError` only, since 3.2, and `getattr(obj, name, default)` is the honest way to ask.
- `vars()` against `dir()`: one is a namespace, the other is a search over all of them.

## See also

- [A class attribute is shared](../a_class_attribute_is_shared/README.md): the first two steps of the search, and the write that does not fall through
- [`super()` is not the parent](../super_is_not_the_parent/README.md): the order the bases are searched in
- [Customizing attribute access ↗](https://docs.python.org/3/reference/datamodel.html#customizing-attribute-access) in the language reference, and the [Descriptor HowTo ↗](https://docs.python.org/3/howto/descriptor.html)
- [Method resolution ↗](https://masiarek.github.io/rust-learning-library/12_Traits/method_resolution/index.html) in the Rust library: the compile-time search that answers the same question there
