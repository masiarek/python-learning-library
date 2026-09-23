# Assignment makes a name local

**Level:** 201 · for Python programmers

> **Stub — an outline, not a lesson.** There is no runnable example behind this page yet, so nothing on it has been through [the check that backs every other claim in this library](../../CONTRIBUTING.md). The bullets below are the questions the finished page has to answer.

**One line:** The compiler reads the whole function before any of it runs and decides where each name lives, and one assignment to a name anywhere in the body makes it local everywhere in the body — so a `total += 1` on the last line turns a `print(total)` on the first line into `UnboundLocalError`, and `global` and `nonlocal` are declarations to the compiler, not operations.

## What the finished page has to answer

- The order a name is looked up in, local, enclosing, global, builtin, and the fact that the *kind* of a name is fixed at compile time while its *value* is found at run time. `co_varnames`, `co_freevars` and `co_names` on a function's `__code__` as the three lists the compiler produced, shown as a dated table rather than a key, because bytecode details move between releases.
- What counts as an assignment: `=`, `+=`, `del`, a `for` target, `with … as`, `except … as`, `import`, a `def` or `class` statement, and a walrus. Each one makes the name local to the enclosing function.
- `UnboundLocalError` is a `NameError`, and the message since 3.11 says what happened: the name is local and has no value yet.
- `global` and `nonlocal`: where each is allowed, that `nonlocal` needs an enclosing *function* scope and will not reach a class body or the module, and that a `global` at module level is a no-op.
- The class-body scope, which nested functions and comprehensions do not see, so a comprehension in a class body cannot read a class attribute two lines above it.
- What `locals()` returns after PEP 667 (3.13): a snapshot in a function, the live namespace at module and class level, dated.

## See also

- [A closure captures the variable, not the value](../a_closure_captures_the_variable/README.md): section 6 is this page in one row
- [Naming and binding ↗](https://docs.python.org/3/reference/executionmodel.html#naming-and-binding) in the language reference, and [Why am I getting an `UnboundLocalError` when the variable has a value? ↗](https://docs.python.org/3/faq/programming.html#why-am-i-getting-an-unboundlocalerror-when-the-variable-has-a-value) in the FAQ
- [PEP 667 ↗](https://peps.python.org/pep-0667/): the `locals()` change
- [Scope is about names ↗](https://masiarek.github.io/rust-learning-library/18_Ownership/scope_is_about_names/index.html) in the Rust library
