"""open() makes four decisions, and only one of them is the encoding.

mode, buffering, encoding and newline are four separate questions with four
separate defaults, and the three that are not the encoding cause most of the
surprises: the file is destroyed at open() rather than at the first write,
tell() in text mode hands back a number that is not a position, and whether
stdout is a terminal decides the order your own two print() calls come out in.

Everything here is measured. Nothing that differs between machines is printed
as a value: locale.getencoding() answers 'US-ASCII' on macOS and
'ANSI_X3.4-1968' on Linux under the identical LC_ALL=C, and
io.DEFAULT_BUFFER_SIZE went from 8192 to 131072 in 3.14 -- both are on the
page in dated tables instead. What IS printed is the flag those answers
depend on, so a reader can see which way this particular run was leaning.

Everything written goes into one temporary directory, which is removed at the
end. Nothing outside it is touched.

Run:  python3 opening_a_file_py.py
"""

import io
import os
import pty
import shutil
import stat
import subprocess
import sys
import tempfile
import warnings

TMP = tempfile.mkdtemp()

# alpha ends with \n, beta with a lone \r, gamma with \r\n, and the last line
# has no terminator at all. U+2028 LINE SEPARATOR sits inside it.
MIXED = "alpha\nbeta\rgamma\r\ndelta epsilon"

CHILD = (
    "import sys\n"
    "print('1 stdout')\n"
    "print('2 stderr', file=sys.stderr)\n"
    "print('3 stdout')\n"
    "print('isatty', sys.stdout.isatty(),"
    " 'line_buffering', sys.stdout.line_buffering)\n"
)


def path(name):
    return os.path.join(TMP, name)


def write_bytes(name, raw):
    with open(path(name), "wb") as fh:
        fh.write(raw)
    return path(name)


def cookies(p, encoding, newline):
    """Every value tell() reports while reading the file one character at a time."""
    out = []
    with open(p, encoding=encoding, newline=newline) as fh:
        while True:
            here = fh.tell()
            char = fh.read(1)
            out.append((here, char))
            if not char:
                return out


print("1. open() MAKES FOUR DECISIONS, AND ONLY ONE OF THEM IS THE ENCODING")
print("   open(path, mode, buffering, encoding, errors, newline)")
print("     mode       what you may do -- and whether the file survives being opened")
print("     buffering  when your bytes actually leave the process")
print("     encoding   which table turns characters into bytes")
print("     newline    which byte sequences count as the end of a line")
print("   Every one of those defaults is a decision somebody made for you. Only")
print("   the third changes what your program MEANS rather than when or how fast,")
print("   and it is the one this page hands off: the sibling library owns it.")
empty = write_bytes("empty.txt", b"")
with open(empty, encoding="utf-8") as fh:
    named = fh.encoding
with open(empty) as fh:
    unnamed = fh.encoding
print("     open(p, encoding='utf-8').encoding  = %s      you decided" % named)
print("     open(p).encoding                    = %s      the machine decided"
      % unnamed)
print("   What the machine decided it on, this run:")
print("     sys.flags.utf8_mode = %d      sys.flags.isolated = %d"
      % (sys.flags.utf8_mode, sys.flags.isolated))
print("   Read those two together. The answer-key runner sets PYTHONUTF8=1 and")
print("   then starts Python with -I, which implies -E and throws every PYTHON*")
print("   variable away. UTF-8 mode is on for the other reason -- LC_ALL=C, which")
print("   PEP 540 turns into UTF-8 mode by itself. Under a pl_PL.ISO8859-2 locale")
print("   the second line above reads ISO8859-2 and every unnamed open() in your")
print("   program silently changes meaning. That is the argument for typing the")
print("   encoding: not that the default is wrong, but that it is not yours.")

print()
print("2. THE TRUNCATION HAPPENS AT open(), NOT AT THE FIRST WRITE")
target = path("data.txt")


def restore():
    with open(target, "w", encoding="utf-8") as fh:
        fh.write("important\n")
    os.chmod(target, 0o644)


restore()
print("   before                              : %d bytes" % os.path.getsize(target))
handle = open(target, "w", encoding="utf-8")
print("   after open(p, 'w'), nothing written : %d bytes  <-- already gone"
      % os.path.getsize(target))
handle.close()
print("   The name is the trap. 'w' does not mean write; it means truncate now,")
print("   and then let you write. A crash on the next line leaves an empty file.")
print()
print("   Opening a 10-byte file six ways, and looking at it before writing:")
print("     mode   the file, immediately after open()   tell()")
for mode in ("r", "w", "x", "a", "r+", "w+"):
    restore()
    try:
        with open(target, mode, encoding="utf-8") as fh:
            print("     %-6r %-36s %d"
                  % (mode, "%d bytes" % os.path.getsize(target), fh.tell()))
    except OSError as exc:
        print("     %-6r %-36s -" % (mode, type(exc).__name__))
print("   'w' and 'w+' show 0 because the file was emptied on the way in, before")
print("   the with-block began. 'x' is the only mode that refuses rather than")
print("   proceeding, and it is the one to reach for when overwriting would be a")
print("   bug. 'a' is the only one that starts anywhere but 0.")
print()
restore()
with open(target, "a", encoding="utf-8") as fh:
    fh.seek(0)
    reported = fh.tell()
    fh.write("Z")
print("   In 'a', seek(0) then write: tell() says %d and the byte lands at the" % reported)
print("   end anyway -- %r. Append is a property of the file" % open(target, encoding="utf-8").read())
print("   descriptor, not of the position, so tell() is not lying so much as")
print("   answering a question you did not ask.")

print()
print("3. tell() IN TEXT MODE IS A COOKIE, NOT A POSITION")
zed = write_bytes("zed.txt", "aż\nbc\n".encode("utf-8"))
print("   The file is 7 bytes and 6 characters: %r" % open(zed, "rb").read())
print("   Reading it one character at a time, what tell() reports before each:")
for label, enc, nl in (("utf-8", "utf-8", ""),
                       ("utf-16", "utf-16", ""),
                       ("utf-8-sig", "utf-8-sig", "")):
    p = path("z_" + label)
    with open(p, "w", encoding=enc, newline=nl) as fh:
        fh.write("aż\nbc\n")
    seen = cookies(p, enc, nl)
    print("     %-10s %2d bytes on disk   %s"
          % (label, os.path.getsize(p), [c for c, _ in seen]))
print("   So far those look like byte offsets, and for a stateless codec reading")
print("   a file with no translation to do, that is exactly what they are. Now")
print("   give the decoder something to remember:")
crlf = write_bytes("crlf.txt", b"a\r\nb\r\n")
for label, enc, nl in (("newline=''", "utf-8", ""),
                       ("newline=None", "utf-8", None)):
    seen = cookies(crlf, enc, nl)
    print("     6-byte file, %-13s %s" % (label, [c for c, _ in seen]))
    print("     %-26s %s" % ("", [ch for _, ch in seen]))
jp = path("jp.txt")
with open(jp, "w", encoding="iso-2022-jp", newline="") as fh:
    fh.write("aあb\n")
seen = cookies(jp, "iso-2022-jp", "")
print("     %d-byte file, iso-2022-jp  %s" % (os.path.getsize(jp), [c for c, _ in seen]))
print("     %-26s [%s]" % ("", ", ".join(ascii(ch) for _, ch in seen)))
print("   A 39-digit number for a 6-byte file. CPython packs the byte position,")
print("   the decoder's state, how many bytes to re-feed and how many characters")
print("   to skip into one integer -- because after '\\r' the decoder does not yet")
print("   know whether it has seen one line ending or the first half of one, and")
print("   a plain offset cannot hold that. The number is not a position; it is a")
print("   receipt. The only thing you may do with it is hand it back:")
with open(crlf, encoding="utf-8", newline="") as fh:
    fh.read(2)
    receipt = fh.tell()
    once = fh.read()
    fh.seek(receipt)
    twice = fh.read()
print("     seek(cookie) then read() -> %r, same as the first read: %s"
      % (twice, once == twice))
print("   And the API says so, by refusing everything else:")
with open(zed, encoding="utf-8") as fh:
    for args in ((0, 1), (1, 1), (0, 2), (-2, 2)):
        try:
            fh.seek(*args)
            print("     seek%-8r -> ok" % (args,))
        except (OSError, ValueError) as exc:
            print("     seek%-8r -> %s" % (args, type(exc).__name__))
print("   Only 'no movement' is allowed relative to anything. Making up a number")
print("   is allowed and is where it bites: byte 2 of this file is the second")
print("   half of z-with-dot-above, so a seek to it starts the decoder in the")
print("   middle of a character --")
with open(zed, encoding="utf-8") as fh:
    fh.seek(2)
    try:
        fh.read()
    except UnicodeDecodeError as exc:
        print("     seek(2); read() -> %s at position %d of what it was handed"
              % (type(exc).__name__, exc.start))
print("   -- and it reports position 0, because as far as the decoder is")
print("   concerned it was handed a fresh file that begins with a stray byte.")

print()
print("4. WHO IS ON THE OTHER END DECIDES WHEN YOUR OUTPUT LEAVES")
child = path("child.py")
with open(child, "w", encoding="utf-8") as fh:
    fh.write(CHILD)
done = subprocess.run([sys.executable, "-I", child],
                      stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
print("   The same five-line program, printing 1 to stdout, 2 to stderr, 3 to")
print("   stdout. Its stdout goes to a pipe:")
for line in done.stdout.decode("utf-8").splitlines():
    print("     %s" % line)
master, slave = pty.openpty()
proc = subprocess.Popen([sys.executable, "-I", child], stdout=slave, stderr=slave)
os.close(slave)
chunks = []
while True:
    try:
        block = os.read(master, 4096)
    except OSError:
        break
    if not block:
        break
    chunks.append(block)
proc.wait()
os.close(master)
seen_raw = b"".join(chunks)
print("   Its stdout goes to a terminal:")
for line in seen_raw.decode("utf-8").splitlines():
    print("     %s" % line)
print("   Nothing about the program changed. Into a pipe stdout is block-")
print("   buffered and holds everything until exit, while stderr is line-")
print("   buffered always -- so message 2 overtakes message 1, and a log read")
print("   top to bottom tells you the warning came first. Into a terminal")
print("   stdout is line-buffered and the order is the one you wrote.")
print("   The fixes, in order of bluntness: print(..., flush=True) for one call,")
print("   sys.stdout.reconfigure(line_buffering=True) for the process, python3 -u")
print("   or PYTHONUNBUFFERED=1 from outside it.")
print("   The terminal changed the bytes too, which is a second lesson for free.")
print("   The line reading '3 stdout', as it arrived:")
print("     from the pipe    %r" % [x for x in done.stdout.splitlines(True) if b"3 " in x][0])
print("     from the pty     %r" % [x for x in seen_raw.splitlines(True) if b"3 " in x][0])
print("   The terminal's line discipline turned '\\n' into '\\r\\n' on the way out,")
print("   so a program that writes Unix line endings is read back with Windows")
print("   ones -- by the terminal, not by Python.")
print()
print("   The same two arguments on a file you opened yourself:")
for mode, buffering in (("w", 0), ("w", 1), ("wb", 0), ("wb", 1)):
    kwargs = {"encoding": "utf-8"} if "b" not in mode else {}
    try:
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            open(path("buf.txt"), mode, buffering=buffering, **kwargs).close()
            note = caught[0].category.__name__ if caught else "accepted"
    except ValueError as exc:
        note = type(exc).__name__
    print("     open(mode=%-4r buffering=%d) -> %s" % (mode, buffering, note))
print("   Unbuffered text is refused outright, because a character is not a unit")
print("   the operating system can write; line buffering in binary mode is")
print("   accepted with a warning and quietly ignored. buffering=0 exists for")
print("   binary only, and it is the one setting that makes write() a syscall.")

print()
print("5. FIVE WAYS TO COUNT THE LINES, AND NO TWO ASK THE SAME QUESTION")
mixed = write_bytes("mixed.txt", MIXED.encode("utf-8"))
raw = open(mixed, "rb").read()
print("   One file, %d bytes: %r" % (len(raw), raw))
with open(mixed, encoding="utf-8") as fh:
    universal = [line for line in fh]
with open(mixed, encoding="utf-8", newline="") as fh:
    untranslated = [line for line in fh]
with open(mixed, "rb") as fh:
    binary = [line for line in fh]
text = open(mixed, encoding="utf-8", newline="").read()
print("     for line in open(p)                     %d" % len(universal))
print("     for line in open(p, newline='')         %d" % len(untranslated))
print("     for line in open(p, 'rb')               %d" % len(binary))
print("     open(p).read().splitlines()             %d" % len(text.splitlines()))
print("     raw.count(b'\\n')  -- what wc -l counts  %d" % raw.count(b"\n"))
print("   They disagree because they are different questions about where a line")
print("   ends. The first two agree on the COUNT and on nothing else:")
print("     universal newlines %r" % universal)
print("     newline=''         %r" % untranslated)
print("     splitlines()       %r" % text.splitlines())
print("   Read the first two together. Universal newlines did not just split the")
print("   file, it REWROTE it: the lone '\\r' after beta came back as '\\n', and so")
print("   did the '\\r\\n' after gamma. Nothing in your program asked for that, and")
print("   it is why csv and any code that re-serialises what it read must pass")
print("   newline=''. splitlines() finds one more boundary than any file reader")
print("   will, because U+2028 ends a line in a str and does not in a file.")

print()
print("6. REPLACING A FILE: WRITE BESIDE IT, THEN RENAME")
config = path("config.txt")


def reset_config():
    with open(config, "w", encoding="utf-8") as fh:
        fh.write("name=old\nport=1\n")
    os.chmod(config, 0o644)


reset_config()
writer = open(config, "w", encoding="utf-8")
print("   Truncating in place, watched by a second reader:")
print("     right after open(p, 'w')  %r" % open(config, encoding="utf-8").read())
writer.write("name=new\n")
writer.flush()
print("     half way through          %r" % open(config, encoding="utf-8").read())
writer.write("port=2\n")
writer.close()
print("     after close()             %r" % open(config, encoding="utf-8").read())
print("   The middle two lines are states the file was never supposed to have.")
print("   Any reader -- another process, a signal handler, your own retry -- can")
print("   see them, and a crash makes one of them permanent.")
print()
reset_config()
fd, temp_name = tempfile.mkstemp(dir=os.path.dirname(config))
with os.fdopen(fd, "w", encoding="utf-8") as fh:
    fh.write("name=new\n")
    print("   Writing beside it instead:")
    print("     half way through          %r" % open(config, encoding="utf-8").read())
    fh.write("port=2\n")
    fh.flush()
    os.fsync(fh.fileno())
os.replace(temp_name, config)
print("     after os.replace()        %r" % open(config, encoding="utf-8").read())
print("   There is no third state. A reader gets all of the old file or all of")
print("   the new one, because os.replace() is rename(2) and the directory entry")
print("   changes in one step. fsync() before the rename is the durability half:")
print("   without it the rename can reach the disk before the bytes do.")
print()
reset_config()
before = stat.S_IMODE(os.stat(config).st_mode)
fd, temp_name = tempfile.mkstemp(dir=os.path.dirname(config))
os.write(fd, b"name=new\nport=2\n")
os.close(fd)
during = stat.S_IMODE(os.stat(temp_name).st_mode)
os.replace(temp_name, config)
after = stat.S_IMODE(os.stat(config).st_mode)
print("   What the rename does NOT carry over:")
print("     the file you are replacing  0o%o" % before)
print("     what mkstemp made           0o%o   (private, on purpose)" % during)
print("     the file afterwards         0o%o   <-- the new file's, not the old" % after)
print("   mkstemp is careful for you, and then you throw the careful thing on top")
print("   of a file everyone could read. Owner, group and ACLs go the same way.")
print("   Copy the mode across with os.chmod before the rename, or shutil.copystat")
print("   for the rest of it. And the temporary file has to be in the SAME")
print("   directory: rename(2) cannot cross a filesystem, so a temp file in /tmp")
print("   makes os.replace() raise OSError with EXDEV instead of being atomic.")

shutil.rmtree(TMP, ignore_errors=True)
