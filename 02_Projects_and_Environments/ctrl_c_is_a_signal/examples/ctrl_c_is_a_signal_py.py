#!/usr/bin/env python3
"""Ctrl-C is a signal, and KeyboardInterrupt is only what the default handler does with it.

Everything here is delivered on purpose with signal.raise_signal() and
signal.setitimer(), so the run is a real signal arriving at a real process and
nothing waits for a key. No clocks are printed: section 5 needs one to ask
whether a sleep was cut short, and prints the answer to that question rather
than the number behind it.
"""

import io
import signal
import sys
import threading
import time

line = "-" * 62


def rule(n, title):
    print()
    print("{}. {}".format(n, title))
    print(line)


# ---------------------------------------------------------------- 1
rule(1, "Before you touch anything, SIGINT already has a handler")

before = signal.getsignal(signal.SIGINT)
print("signal.getsignal(signal.SIGINT) ......... {}".format(before))
print("...is signal.default_int_handler ........ {}".format(before is signal.default_int_handler))
print("SIGINT's number ......................... {}".format(int(signal.SIGINT)))
print()
print("It is an ordinary callable, so we can just call it ourselves:")
try:
    signal.default_int_handler(signal.SIGINT, None)
except BaseException as exc:
    print("    it raised ........................... {}".format(type(exc).__name__))
print()
print("So KeyboardInterrupt is not what Ctrl-C does. It is what THIS function")
print("does, and this function is replaceable.")


# ---------------------------------------------------------------- 2
rule(2, "Replacing it")

seen = []


def handler(signum, frame):
    seen.append((signum, type(frame).__name__, frame.f_code.co_name))
    print("    I got a SIGINT, but I am not stopping")


previous = signal.signal(signal.SIGINT, handler)
print("signal.signal() returns the OLD handler . {}".format(previous))
print("...which is the one from section 1 ...... {}".format(previous is before))
print("keep it, and you can put it back.")


# ---------------------------------------------------------------- 3
rule(3, "A real SIGINT, delivered to ourselves")

print("signal.raise_signal(signal.SIGINT) is what the terminal does when you")
print("press Ctrl-C, minus the terminal:")
print()
signal.raise_signal(signal.SIGINT)
print()
print("...and the next line still runs. Nothing was raised, nothing unwound.")
print("A handler that returns normally resumes the code it interrupted, which")
print("is why a `while True:` loop keeps counting.")


# ---------------------------------------------------------------- 4
rule(4, "What the handler is handed, and the name that shadows a module")

signum, frame_type, frame_func = seen[0]
print("arg 1, signum ........................... {} ({})".format(signum, signal.Signals(signum).name))
print("arg 2, a frame object ................... {}".format(frame_type))
print("        it was executing ................ {}".format(frame_func))
print()
print("The second parameter is a FRAME: the line that was running when the")
print("signal arrived. Name it `time` and the module is gone inside the handler:")
print()


def shadowing_handler(signum, time):
    try:
        time.sleep(0)
    except Exception as exc:
        print("    time.sleep(0) inside it ............. {}".format(type(exc).__name__))
    else:
        print("    time.sleep(0) inside it ............. worked")


signal.signal(signal.SIGINT, shadowing_handler)
signal.raise_signal(signal.SIGINT)
signal.signal(signal.SIGINT, handler)
print()
print("The loop outside keeps working, because its `time` is the global one.")
print("The trap is local to the handler, and only springs if the handler ever")
print("needs the module -- to time a shutdown, say.")


# ---------------------------------------------------------------- 5
rule(5, "A signal that arrives in the middle of time.sleep()")

if not hasattr(signal, "setitimer"):
    print("no signal.setitimer on this platform -- section skipped")
else:
    alarms = []
    signal.signal(signal.SIGALRM, lambda s, f: alarms.append(s))
    asked = 0.25
    signal.setitimer(signal.ITIMER_REAL, 0.05)
    start = time.monotonic()
    time.sleep(asked)
    elapsed = time.monotonic() - start
    signal.setitimer(signal.ITIMER_REAL, 0)
    signal.signal(signal.SIGALRM, signal.SIG_DFL)
    print("an alarm was set for 0.05s into a 0.25s sleep")
    print("the handler ran ......................... {}".format(bool(alarms)))
    print("time.sleep() raised ..................... False")
    print("the sleep still lasted its full 0.25s ... {}".format(elapsed >= asked))
    print()
    print("PEP 475 (Python 3.5): a syscall interrupted by a signal is RETRIED")
    print("with the time that was left, once the handler returns. Before 3.5 the")
    print("sleep returned early and you had to loop around it yourself.")


# ---------------------------------------------------------------- 6
rule(6, "Putting the default back")

signal.signal(signal.SIGINT, signal.default_int_handler)
print("signal.signal(SIGINT, signal.default_int_handler)")
print()
try:
    signal.raise_signal(signal.SIGINT)
except BaseException as exc:
    print("the same raise_signal now ............... {}".format(type(exc).__name__))
print()
print("Three things can go in that second argument:")
print("    a function of yours ................. Python calls it")
print("    signal.SIG_DFL ...................... the kernel's default: die")
print("    signal.SIG_IGN ...................... thrown away, not delivered")
print()
print("SIG_DFL for SIGINT kills the process without a traceback and without")
print("running `finally:` blocks. default_int_handler is what gives you the")
print("traceback -- it is Python's politeness, not the kernel's.")


# ---------------------------------------------------------------- 7
rule(7, 'The counter that overwrites itself: "\\r" and when it reaches the screen')

print('print("\\r{}".format(i), end="") rewinds to the left margin and prints')
print("over what is already there, so one line counts up instead of a thousand")
print("lines scrolling. Whether you SEE it count depends on buffering:")
print()

for label, line_buffered in (("line_buffering=True  (a terminal)", True),
                             ("line_buffering=False (a pipe)", False)):
    sink = io.BytesIO()
    out = io.TextIOWrapper(sink, line_buffering=line_buffered)
    out.write("41")
    after_digits = bytes(sink.getvalue())
    out.write("\r")
    after_cr = bytes(sink.getvalue())
    print("{}".format(label))
    print('    after writing "41" .................. {!r}'.format(after_digits))
    print('    after writing "\\r" .................. {!r}'.format(after_cr))

print()
print("A line-buffered stream flushes on \\r as well as on \\n -- which is the")
print("only reason that counter animates without flush=True. Down a pipe there")
print("is no line buffering at all and the whole count arrives at exit.")
print()
print("This run's own stdout:")
print("    sys.stdout.isatty() ................. {}".format(sys.stdout.isatty()))
print("    sys.stdout.line_buffering ........... {}".format(sys.stdout.line_buffering))
print("    (the recorded key is captured, so both read False;")
print("     run this in a terminal and both flip to True)")


# ---------------------------------------------------------------- 8
rule(8, "Two rules about threads")

failed = []


def try_from_a_thread():
    try:
        signal.signal(signal.SIGINT, signal.SIG_DFL)
    except Exception as exc:
        failed.append(type(exc).__name__)


t = threading.Thread(target=try_from_a_thread, name="worker")
t.start()
t.join()
print("signal.signal() from another thread ..... {}".format(failed[0]))

ran_in = []
signal.signal(signal.SIGINT, lambda s, f: ran_in.append(threading.current_thread().name))


def raise_from_a_thread():
    signal.raise_signal(signal.SIGINT)


t = threading.Thread(target=raise_from_a_thread, name="worker")
t.start()
t.join()
for _ in range(1000):
    if ran_in:
        break
    time.sleep(0.001)
print("a SIGINT raised by the worker ran in ..... {}".format(ran_in[0] if ran_in else "(not yet)"))
print()
print("Only the main thread may install a handler, and every handler runs in")
print("the main thread -- whichever thread the kernel happened to deliver to.")
print("A worker blocked on a socket does not get interrupted; the main thread")
print("gets the callback, and has to tell the worker itself.")

signal.signal(signal.SIGINT, signal.default_int_handler)
