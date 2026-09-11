"""Kata answers: eight one-liners, and the only one that prints quotes."""

import shlex
import subprocess
import sys

# -E, -s and -X utf8 keep your environment out of the answers; the commands are
# shown without them because none of the three changes what -c does.
FLAGS = ["-E", "-s", "-X", "utf8"]

ROWS = [
    (("-c", "chr(0x20AC)"), "", "computed, then dropped"),
    (("-c", "x = chr(0x20AC); x"), "", "a bare name is an expression too"),
    (("-i", "-q"), "x = chr(0x20AC); x\n", "the prompt shows it -- as repr()"),
    (("-i", "-q"), "print(chr(0x20AC))\n", "and never shows the None print() returned"),
    (("-c", "import sys; print(sys.argv[1:])", "-v", "x"), "", "after the program, -v is the program's"),
    (("-c", 'for c in "ab": print(c); print("-")'), "", "both prints are the loop's body"),
    (("-c", 'import sys; for c in "ab": print(c)'), "", "a for cannot follow a ;"),
    (("-c", 'import sys; sys.exit("bad")'), "", "and 'bad' went to stderr"),
]


def shown(args, stdin):
    words = []
    for i, arg in enumerate(args):
        word = shlex.quote(arg)
        if i > 0 and args[i - 1] == "-c" and not word.startswith("'"):
            word = f"'{arg}'"
        words.append(word)
    line = "python3 " + " ".join(words)
    if stdin:
        line = f"echo {shlex.quote(stdin.rstrip(chr(10)))} | {line}"
    return line


for n, (args, stdin, note) in enumerate(ROWS, 1):
    proc = subprocess.run(
        [sys.executable, *FLAGS, *args], input=stdin.encode("utf-8"), capture_output=True
    )
    out = proc.stdout.decode("utf-8")
    err = proc.stderr.decode("utf-8")
    if proc.returncode and err.startswith(("Traceback", "  File")):
        what = err.strip().splitlines()[-1].split(":")[0]
    else:
        what = f"stdout {out!r}"
    print(f"     {n}. {shown(args, stdin)}")
    print(f"          {what:<24} exit {proc.returncode}   {note}")

print()
print("     THE RULE")
print("     Only lines 3 and 4 reached the prompt, and only the prompt shows a")
print("     value you did not print -- as repr(), which is where line 3's")
print("     quotes come from. It never shows None, which is why line 4 has no")
print("     second line. Everywhere else a bare expression is computed and")
print("     dropped: lines 1 and 2 print nothing, and exit 0 because nothing")
print("     went wrong.")
print()
print("     THE ONE THAT LOOKS LIKE A FLAG")
print("     Line 5's -v comes after the program, and everything after the")
print("     program belongs to it. Put -v before -c and it is Python's.")
