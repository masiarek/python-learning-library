# 03_Numbers — what `==` means between two numbers

**Level:** 201 · for Python programmers, especially ones coming from Rust or C

Python's numbers look like the least surprising part of the language. An `int` never overflows, `1 == 1.0` just works, and nothing needs a cast. Each of those conveniences hides a decision the language made for you, and each one becomes visible the moment you compare two numbers that are not quite what you thought: an integer too big for a double, a decimal fraction binary cannot hold, or a NaN.

This chapter started from *Rust in Action*'s section on comparing numbers, which asks the same questions of a language that refuses to compare two number types at all. The Rust and C libraries answer them for their own languages, and every page here links the matching page there.

| # | Lesson | The question it answers | Status |
|---|---|---|---|
| 1 | [Comparing an `int` with a `float`](comparing_int_and_float/README.md) | Why is `2**53 + 1 == float(2**53 + 1)` `False` in Python, when the cast Rust and C use says they are equal? | written |
| 2 | [Float equality and NaN](float_equality_and_nan/README.md) | Why is `0.1 + 0.2 == 0.3` `False`, why does an epsilon test fail at 2000, and why is `[nan] == [nan]` `True`? | written |

The second page ends with a `## Practice` kata, indexed in [KATAS.md](../KATAS.md).

## What comes next here

Named rather than stubbed, because a folder name is a permanent URL and an empty one is clutter:

- **`round()` is not school rounding**: `round(2.5)` is `2`, and `round(2.675, 2)` is `2.67` for a reason that is not the rounding mode
- **`//` and `%` floor, and C truncates**: why `-7 // 2` is `-4` in Python and `-7 / 2` is `-3` in C and Rust. The Rust side is written: [three ways to divide a negative number ↗](https://masiarek.github.io/rust-learning-library/19_Numbers/other_number_types/big_integers/index.html#three-ways-to-divide-a-negative-number)
- **`Decimal` has a context**: precision, rounding and traps as process-wide state, and what that means for money. The Rust side, where `rust_decimal` has no context, is written: [Decimals ↗](https://masiarek.github.io/rust-learning-library/19_Numbers/other_number_types/decimal_numbers/index.html)
- **`Fraction`, `complex` and an `int` with no ceiling**: the types Python ships and Rust needs a crate for, already run side by side in the Rust library's [Other number types ↗](https://masiarek.github.io/rust-learning-library/19_Numbers/other_number_types/index.html)

## Where this sits relative to the other libraries

The [math library ↗](https://masiarek.github.io/math-learning-library/01_Precision/machine_numbers/index.html) owns the numbers themselves: which values a double can hold, and why the gaps between them grow. The [Rust library's `19_Numbers` ↗](https://masiarek.github.io/rust-learning-library/19_Numbers/index.html) owns the fixed-width types and the casts between them. This chapter owns what Python does with the same doubles, which is often the opposite of what Rust does: it compares exactly where Rust converts, and it raises where Rust returns a NaN.
