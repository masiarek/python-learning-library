"""-c runs its code as a script, not at the prompt -- and the shell reads it first."""

import code
import contextlib
import io
import shlex
import subprocess
import sys
import tempfile
from pathlib import Path

# Every command below starts a fresh python3. Three flags keep the machine out of
# the answers: -E ignores PYTHON* variables, -s skips the user site-packages, and
# -X utf8 fixes the encoding of what the child prints. None of them changes what
# -c does, so the commands are shown without them.
FLAGS = ["-E", "-s", "-X", "utf8"]
EURO = "chr(0x20AC)"


def python3(*args, stdin="", cwd=None):
    """Run a child python3; return what it wrote to stdout and stderr, and its exit status."""
    proc = subprocess.run(
        [sys.executable, *FLAGS, *args],
        input=stdin.encode("utf-8"),
        capture_output=True,
        cwd=cwd,
    )
    return proc.stdout.decode("utf-8"), proc.stderr.decode("utf-8"), proc.returncode


def shown(*args, stdin=""):
    """The command as you would type it, with the program in single quotes."""
    words = []
    for i, arg in enumerate(args):
        word = shlex.quote(arg)
        if i > 0 and args[i - 1] == "-c" and not word.startswith("'"):
            word = f"'{arg}'"
        words.append(word.replace("\n", "⏎"))
    line = "python3 " + " ".join(words)
    if stdin:
        line = f"echo {shlex.quote(stdin.rstrip(chr(10)))} | {line}"
    return line


def error_type(stderr):
    """The exception's name, from the last line of a traceback -- never its message."""
    return stderr.strip().splitlines()[-1].split(":")[0]


def result(value, note, width=24):
    """One indented result line, with the note beside it or, if it will not fit, under it."""
    if len(value) < width:
        print(f"         {value:<{width}} {note}")
    else:
        print(f"         {value}")
        print(f"         {'':<{width}} {note}")


print("-c IS NOT THE PROMPT")
print("Each command starts a fresh python3, and the columns are what it wrote.")
print("(Every one also gets -E -s -X utf8, so nothing in your environment can")
print("change an answer. None of the three changes what -c does.)")

print("\n1. THE SAME LINE, FOUR WAYS IN")
ways = [
    (("-c", EURO), ""),
    (("-",), EURO + "\n"),
    (("-i", "-q"), EURO + "\n"),
    (("-c", f"print({EURO})"), ""),
]
print(f"     {'command':<38} {'stdout':<10} exit")
print("     " + "-" * 53)
for args, stdin in ways:
    out, err, status = python3(*args, stdin=stdin)
    print(f"     {shown(*args, stdin=stdin):<38} {out!r:<10} {status}")
    if args[0] == "-i":
        prompt_err = err
print()
print(f"     The prompt wrote its two '>>> ' to stderr, not stdout: {prompt_err!r}")
print()
print("     All four computed the euro sign, and only the prompt showed it")
print("     without being asked. -i starts the prompt even when the input is")
print("     a pipe; the other three ran the same line as a SCRIPT, and a")
print("     script does nothing with the value of a bare expression. It is")
print("     computed, then dropped -- exit 0, because nothing went wrong.")
print("     print() is the one spelling that works all four ways.")
print()
print("     The prompt's quotes are part of what it printed: it shows repr()")
print("     of a value, where print() shows str().")

print("\n2. THE DIFFERENCE IS A COMPILE MODE")
print(f"     src = {EURO!r}")
print()
for mode in ("exec", "single"):
    captured = io.StringIO()
    with contextlib.redirect_stdout(captured):
        exec(compile(EURO, "<string>", mode), {})
    label = f"exec(compile(src, '<string>', '{mode}'))"
    print(f"     {label:<45} prints   {captured.getvalue()!r}")
value = eval(compile(EURO, "<string>", "eval"))
label = "eval(compile(src, '<string>', 'eval'))"
print(f"     {label:<45} returns  {value!r}")
captured = io.StringIO()
with contextlib.redirect_stdout(captured):
    code.InteractiveInterpreter().runsource(EURO)
label = "code.InteractiveInterpreter().runsource(src)"
print(f"     {label:<45} prints   {captured.getvalue()!r}")
print()
print("     Python compiles source in one of three modes before running it.")
print("     'exec' is a module: a file, the -c argument, a pipe into python3 -.")
print("     'eval' is one expression, and hands its value back to whoever")
print("     asked. 'single' is one statement typed at >>>, and it is the only")
print("     mode that passes the value of an expression statement to")
print("     sys.displayhook -- which is what prints it. The standard library's")
print("     own prompt, the code module, compiles in 'single' too. -c never does.")

print("\n3. -c IS A SCRIPT IN EVERY OTHER WAY TOO")
facts = [
    (("-c", "import sys; print(sys.argv)", "a", "-v"), "'-c' stands where a script's name would"),
    (("-c", "print(__name__)"), "the name a script run directly gets"),
    (("-c", 'print("__file__" in globals())'), "no file, so no __file__"),
    (("-c", "import sys; print(repr(sys.path[0]))"), "the current directory, searched first"),
    (("-c", "import sys; print(sys.orig_argv[-1])"), "the program's only copy is this string"),
]
for args, note in facts:
    out, err, status = python3(*args)
    print(f"     {shown(*args)}")
    result(out.strip(), note)
print()
print("     Everything after the program belongs to the program: the -v in the")
print("     first line went into sys.argv, not to Python's verbose flag.")
print()
print("     The empty string in sys.path[0] is the one to remember. In a")
print("     folder that holds a file called json.py:")
print()
with tempfile.TemporaryDirectory() as folder:
    Path(folder, "json.py").write_text('print("(the json.py in this folder ran)")\n', encoding="utf-8")
    for args in (("-c", "import json"), ("-P", "-c", "import json"), ("-I", "-c", "import json")):
        out, err, status = python3(*args, cwd=folder)
        print(f"         {shown(*args):<30} {out!r}")
print()
print("     sys.path[0] is the directory you ran the command from, and it is")
print("     searched before the standard library. -P, new in 3.11, leaves it")
print("     out, and so does -I.")

print("\n4. ONE LINE HOLDS SIMPLE STATEMENTS ONLY")
lines = [
    (("-c", "import sys; for a in sys.argv[1:]: print(a)", "x"), "a for cannot follow a ;"),
    (("-c", 'for c in "xy": print(c); print("-")'), "both prints are the loop's body"),
    (("-c", "import sys\nfor a in sys.argv[1:]: print(a)", "x", "-v"), "a newline where the ; was"),
]
for args, note in lines:
    out, err, status = python3(*args)
    print(f"     {shown(*args)}")
    result(f"exit {status}, {error_type(err)}" if status else repr(out), note)
print()
print("     A ; joins simple statements: an import, an assignment, a call. A")
print("     compound statement -- for, if, with, def -- may START the line, and")
print("     then everything after its colon is its body; it may not follow a ;.")
print("     The way out is a real newline inside the quotes, the ⏎ above.")

print("\n5. THE EXIT STATUS IS THE WHOLE REPORT")
checks = [
    ("-c", EURO),
    ("-c", "1/0"),
    ("-c", 'import sys; sys.exit("bad")'),
    ("-c", "raise SystemExit(3)"),
    ("-c",),
]
for args in checks:
    out, err, status = python3(*args)
    if status == 0:
        note = "nothing printed, nothing wrong"
    elif status == 2:
        note = "no program: Python refused the line"
    elif err.startswith("Traceback"):
        note = f"{error_type(err)}; traceback on stderr"
    elif err:
        note = f"stderr {err!r}"
    else:
        note = "whatever number you raise"
    print(f"     {shown(*args):<41} exit {status}   {note}")
print()
print("     A shell sees nothing but the exit status. 0 means the program ran")
print("     to the end, printed or not. 1 is an uncaught exception, or")
print("     sys.exit() with a message. 2 comes from Python itself, before any")
print("     of your code has run.")

print("\n6. THE SHELL READS THE LINE BEFORE PYTHON DOES")
print("     A shell cuts the line into words before python3 starts, and -c")
print("     takes exactly one of them. shlex, told to treat ( and ) the way a")
print("     shell does, cuts the two lines like this:")
print()
for line in ("python3 -c chr(0x20AC)", "python3 -c 'print(chr(0x20AC))'"):
    words = list(shlex.shlex(line, posix=True, punctuation_chars=True))
    print(f"     {line}")
    print(f"         {words}")
print()
print("     Unquoted, the parentheses are not part of any word: they are shell")
print("     syntax, so the shell deals with them itself and python3 never")
print("     starts. Quoted, the whole program is one word.")
print()
print("     shlex.quote() writes that word for you:")
print()
for program in ("print(chr(0x20AC))", 'print("it' + chr(39) + 's")'):
    quoted = shlex.quote(program)
    back = shlex.split(quoted) == [program]
    print(f"         {program:<20} ->  {quoted:<22}  one word again: {back}")
print()
print("     A single quote cannot appear inside single quotes, so quote()")
print("     closes them, writes the quote inside double quotes, and opens them")
print("     again. Or keep the character away from the shell altogether: in a")
print("     Python string \\x27 is a quote and \\x5c is a backslash, and single")
print("     quotes pass those four characters through untouched.")
print()
for program in (r'print("it\x27s")', r'print(len("\x5c"))'):
    out, err, status = python3("-c", program)
    print(f"         {shown('-c', program):<34} {out!r}")
