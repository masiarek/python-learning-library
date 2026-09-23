# 05_Functions — what happens when `def` runs

**Level:** 201 · for Python programmers, especially ones coming from C, Rust or ABAP

`def` is not a declaration. It is a statement that runs, in order with the statements around it, and when it runs it evaluates the default values, applies the decorators, stores the annotations and builds a function object that holds references into the scope it was made in. Every page in this chapter is a consequence of that sentence, and every surprise is a piece of work that happened earlier than the reader thought — a default, a decorator — or later — a closure's lookup, a type check that never comes.

| # | Lesson | The question it answers | Status |
|---|---|---|---|
| 1 | [A default is computed once](a_default_is_computed_once/README.md) | Why does my function remember the previous call's list — and why does `None` fix it? | written |
| 2 | [A closure captures the variable, not the value](a_closure_captures_the_variable/README.md) | Why do three lambdas built in one loop all return the last value — and which of the three fixes should I use? | written |
| 3 | [Assignment makes a name local](assignment_makes_it_local/README.md) | Why did adding `total += 1` at the bottom of a function break the `print(total)` at the top? | stub |
| 4 | [A decorator is a call, made when `def` runs](a_decorator_is_a_call/README.md) | What does `@deco` actually do, and when — and why did every function I decorated get renamed `wrapper`? | stub |
| 5 | [Annotations are not checked](annotations_are_not_checked/README.md) | Why did `f('a')` run when I wrote `def f(x: int)` — and what does check it? | stub |

## Where this sits relative to the other libraries

The [Rust library's closures chapter ↗](https://masiarek.github.io/rust-learning-library/23_Closures/index.html) is the sharp comparison for page 2: the compiler chooses how a closure captures and refuses the loop shape Python allows, and [`move` ↗](https://masiarek.github.io/rust-learning-library/23_Closures/the_move_keyword/index.html) is capture by value on demand. Rust has no default arguments, and [Optional arguments ↗](https://masiarek.github.io/rust-learning-library/17_Option_and_Result/optional_arguments/index.html) is what it does instead. C has neither closures nor defaults, so a callback there is a function pointer and a `void *`, and ABAP has neither either: a method's `DEFAULT` must be a constant, and an object stands in for a closure. Both of those absences are said on the pages, in the bridge sections, rather than in a page of their own.
