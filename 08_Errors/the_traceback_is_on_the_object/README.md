# The traceback is on the object

**Level:** 301 · for Python programmers

> **Stub — an outline, not a lesson.** There is no runnable example behind this page yet, so nothing on it has been through [the check that backs every other claim in this library](../../CONTRIBUTING.md). The bullets below are the questions the finished page has to answer.

**One line:** An exception carries its traceback as `__traceback__`, so a bare `raise` re-raises with the original frames while `raise e` adds the current line, `traceback.format_exc()` gets you the text without printing it, `sys.excepthook` is the one function that prints it for an uncaught exception, and a chained traceback reads bottom-up from *"The above exception was the direct cause"*.

## What the finished page has to answer

- `__traceback__`, `tb_next` and `tb_lineno`, and the frames the object holds alive, which is why [`except Exception` is not `except:`](../except_exception_is_not_except/README.md) section 5 deletes the `as`-name.
- Bare `raise` against `raise e` against `raise e from None`, measured by the number of frames each traceback shows.
- `traceback.print_exc()`, `format_exception()`, and `TracebackException`, which renders the text and drops the frames, for logging without leaking memory.
- `sys.excepthook` and `threading.excepthook`, and the one line `logging.exception()` adds to a handler.
- What newer releases print, as a dated table rather than a key: fine-grained carets since 3.11 (PEP 657), colour since 3.13 and the `PYTHON_COLORS` variable that turns it off, and where a note added with `add_note()` appears.
- Reading a chained traceback: the *first* block printed is the oldest cause, and the last is the exception that escaped.

## See also

- [`except Exception` is not `except:`](../except_exception_is_not_except/README.md): section 6, the links the object carries
- [`traceback` ↗](https://docs.python.org/3/library/traceback.html) and [`sys.excepthook` ↗](https://docs.python.org/3/library/sys.html#sys.excepthook) in the library reference, and [PEP 657 ↗](https://peps.python.org/pep-0657/)
- [Reading a backtrace ↗](https://masiarek.github.io/rust-learning-library/17_Option_and_Result/reading_a_backtrace/index.html) in the Rust library, where the frames belong to the panic and have to be asked for with an environment variable
