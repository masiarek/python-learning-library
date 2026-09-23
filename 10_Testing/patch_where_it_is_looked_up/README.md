# `patch` where it is looked up

**Level:** 301 · for Python programmers

> **Stub — an outline, not a lesson.** There is no runnable example behind this page yet, so nothing on it has been through [the check that backs every other claim in this library](../../CONTRIBUTING.md). The bullets below are the questions the finished page has to answer.

**One line:** `unittest.mock.patch('mod.name')` replaces the attribute `name` in module `mod` for the duration of a test, so a function that did `from time import time` keeps its own reference and is unaffected by patching `time.time`, while patching `mymodule.time` works — the target is where the name is looked up at call time, which is a chapter-4 fact about names wearing a testing hat.

## What the finished page has to answer

- The rule from the `mock` documentation, measured: `import time; time.time()` looks the name up at the call and sees the patch; `from time import time` bound a second name at import, and does not.
- `patch` as a decorator and as a context manager, and the argument order when several decorators are stacked, which is [A decorator is a call](../../05_Functions/a_decorator_is_a_call/README.md) bottom-up.
- `autospec=True`, and why without it a `Mock` accepts any call and any attribute, so a misspelled `assert_called_once_wiht` used to pass silently; the `assert_*` names have raised `AttributeError` since 3.5, and `unsafe=True` turns that back off.
- `patch.object` for one attribute of one object, `patch.dict` for `os.environ`.
- `datetime.datetime` is a C type and cannot be patched in place; patch the name in the module that uses it.
- What a patch does to a name captured in a closure or a default argument before the test ran, which is [A default is computed once](../../05_Functions/a_default_is_computed_once/README.md).

## See also

- [Assignment does not copy](../../04_Names_and_Objects/assignment_does_not_copy/README.md) and [A closure captures the variable, not the value](../../05_Functions/a_closure_captures_the_variable/README.md): the two facts about names this page rests on
- [Where to patch ↗](https://docs.python.org/3/library/unittest.mock.html#where-to-patch) in the `unittest.mock` documentation
- [A test double by hand ↗](https://masiarek.github.io/rust-learning-library/28_Testing/a_test_double_by_hand/index.html) in the Rust library, where there is no `patch` and the seam has to be a trait
