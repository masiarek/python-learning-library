# 07_Classes_and_the_Data_Model — every operator is a method, and every lookup is a search

**Level:** 201 → 301 · for Python programmers, especially ones coming from ABAP, Java or C#

A class in Python is made at run time by running its body, and an object of that class is a namespace whose lookups fall through to the class. Almost nothing else is built in. `==`, `hash()`, `len()`, `if x`, `obj.x`, `with`, `for` and `+` each become a call to a method with a double-underscored name, which the class may define, inherit or leave to `object`'s defaults. The pages here are the places where that design gives an answer a reader from a language with declared fields, a `static` keyword and a fixed `equals`-and-`hashCode` pair does not expect.

| # | Lesson | The question it answers | Status |
|---|---|---|---|
| 1 | [A class attribute is shared](a_class_attribute_is_shared/README.md) | Why did every instance see the item I appended through one — and why did `c.count = 1` not change `Counter.count`? | written |
| 2 | [`obj.x` is a search](attribute_lookup_is_a_search/README.md) | Why did a `@property` beat the instance attribute — and why does `__getattr__` not run for names that exist? | stub |
| 3 | [`super()` is not the parent](super_is_not_the_parent/README.md) | Why did `super().__init__()` call a class that is not my base class? | stub |
| 4 | [`class` is a call](class_is_a_call/README.md) | What actually runs when Python reaches a `class` statement — and when do I need a metaclass? | stub |
| 5 | [Defining `__eq__` deletes `__hash__`](defining_eq_deletes_hash/README.md) | Why did my class stop working as a dict key the moment I gave it `__eq__` — and why is my `@dataclass` unhashable? | written |
| 6 | [`if x` calls a method](if_x_calls_a_method/README.md) | Why is an object of my class always true — and why did `if result:` miss a legitimate `0`? | stub |
| 7 | [`@dataclass` writes the methods](dataclass_writes_the_methods/README.md) | Which methods did `@dataclass` write, which did it refuse, and what does it never check? | stub |

## Where this sits relative to the other libraries

Rust has no classes, and the [structs ↗](https://masiarek.github.io/rust-learning-library/16_Structs/index.html) and [traits ↗](https://masiarek.github.io/rust-learning-library/12_Traits/index.html) chapters of the Rust library are what it has instead: [Comparison traits ↗](https://masiarek.github.io/rust-learning-library/12_Traits/comparison_traits/index.html) is page 5's pair of methods as two derives, [Method resolution ↗](https://masiarek.github.io/rust-learning-library/12_Traits/method_resolution/index.html) is page 2's search done by the compiler, and the absence of inheritance is page 3's whole subject seen from the other side. ABAP declares at the definition what Python decides by lookup: `CLASS-DATA` against `DATA` is page 1, and a hashed table's declared key is page 5. The [concurrency library ↗](https://masiarek.github.io/concurrency-learning-library/) owns what happens when two threads touch one class attribute. Chapter 4's [`is` is not `==`](../04_Names_and_Objects/is_is_not_equals/README.md) and [`hash()` is not stable across runs](../04_Names_and_Objects/hash_is_not_stable_across_runs/README.md) are page 5's two methods seen from the built-in types.
