# 09_The_Standard_Library — the modules whose names promise more than they do

**Level:** 201 → 301 · for Python programmers

A module's name is a promise, and the promises the standard library makes are narrower than they sound. `json` writes JSON, which has six types and none of them is a tuple. A `Path` is not a string. An `Enum` member is not its value. A `defaultdict` creates a key when you only meant to look. `lru_cache` keys on the call as written. `logging` is a tree, and a record climbs it. Each page here is one such name and the gap between what it says and what it does, measured.

| # | Lesson | The question it answers | Status |
|---|---|---|---|
| 1 | [`json` is not Python](json_is_not_python/README.md) | Why did my tuple come back a list, my `int` key a `str`, and my Polish text as `Ł` — and why did none of that raise? | written |
| 2 | [A `Path` is not a string](a_path_is_not_a_string/README.md) | Why is `path + '.bak'` a `TypeError` — and which `Path` methods touch the disk? | stub |
| 3 | [An `Enum` member is not its value](an_enum_member_is_not_its_value/README.md) | Why is `Color.RED == 1` `False` — and why did two members turn out to be one? | stub |
| 4 | [`defaultdict` creates on read](defaultdict_creates_on_read/README.md) | Why did my dict grow during a loop that only read from it? | stub |
| 5 | [`lru_cache` keys on the call](lru_cache_keys_on_the_call/README.md) | Why are `f(1)` and `f(x=1)` two cache entries — and why did my objects stop being garbage-collected? | stub |
| 6 | [`logging` is a tree](logging_is_a_tree/README.md) | Why is every line printed twice — and why did `basicConfig()` do nothing? | stub |

## Where this sits relative to the other libraries

The modules other libraries own are not here. `re` belongs to the [regex library ↗](https://masiarek.github.io/regex-learning-library/), `codecs` to the encodings library through chapter 1's [The codecs registry](../01_Text_and_Bytes/the_codecs_registry/README.md), and `threading`, `asyncio`, `multiprocessing` and `concurrent.futures` to the [concurrency library ↗](https://masiarek.github.io/concurrency-learning-library/). For page 1 the Rust library's [data chapter ↗](https://masiarek.github.io/rust-learning-library/06_Data/index.html) is the typed alternative, where the type is the schema and a round trip is an identity.
