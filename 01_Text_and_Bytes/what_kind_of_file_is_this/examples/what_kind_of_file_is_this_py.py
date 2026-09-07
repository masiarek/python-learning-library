"""Four Python APIs answer "what kind of file is this", and they answer
four different questions.

os.lstat asks the filesystem how the thing is stored. mimetypes asks the
FILENAME and never opens anything. Reading the bytes is the only one that
asks what is in the file -- and since 3.13 the standard library has no
module that does it for you. subprocess asks the kernel whether the file
can be launched, which is a fifth thing again.

Nothing here prints a version-dependent fact: the removal of imghdr, and
the case where is_file() swallows a PermissionError, are on the page in
dated tables because no answer key could hold them.

Run:  python3 what_kind_of_file_is_this_py.py
"""

import mimetypes
import os
import pathlib
import shutil
import stat
import subprocess
import tempfile

# The first 33 bytes of a 1x1 PNG: the 8-byte signature, then the IHDR chunk.
PNG = (b"\x89PNG\r\n\x1a\n"
       b"\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00"
       b"\x1f\x15\xc4\x89")

# A magic table, in miniature. This is the part the standard library used to
# ship and no longer does.
MAGIC = [(b"\x89PNG\r\n\x1a\n", "image/png"),
         (b"\x1f\x8b", "application/gzip"),
         (b"%PDF-", "application/pdf"),
         (b"#!", "text/x-shellscript")]


def sniff(path):
    """Ask the bytes. Nothing in the stdlib does this for you any more."""
    with open(path, "rb") as fh:
        head = fh.read(64)
    if not head:
        return "empty"
    for sig, kind in MAGIC:
        if head.startswith(sig):
            return kind
    try:
        head.decode("utf-8")
        return "text/plain"
    except UnicodeDecodeError:
        return "application/octet-stream"


def inode_kind(path):
    """lstat, so a symlink is reported as a symlink rather than followed."""
    mode = os.lstat(path).st_mode
    for name, test in (("directory", stat.S_ISDIR), ("regular file", stat.S_ISREG),
                       ("symlink", stat.S_ISLNK), ("fifo", stat.S_ISFIFO)):
        if test(mode):
            return name
    return "something else"


tmp = tempfile.mkdtemp()
os.chdir(tmp)

with open("liar.txt", "wb") as fh:          # PNG bytes wearing a .txt name
    fh.write(PNG)
with open("real.png", "wb") as fh:          # Polish text wearing a .png name
    fh.write("Zażółć gęślą jaźń\n".encode("utf-8"))
open("empty.png", "wb").close()             # nothing at all, .png name
os.mkdir("adir")
os.symlink("liar.txt", "good_link")
os.symlink("nowhere.txt", "dangling")

print("1. THE FILESYSTEM KNOWS SEVEN KINDS, AND NONE OF THEM IS 'PNG'")
print("   os.lstat() reads the directory entry. It never opens the file, so")
print("   it cannot be fooled by the bytes and cannot see them either.")
for name in ("liar.txt", "adir", "good_link"):
    mode = os.lstat(name).st_mode
    print("   %-10s S_IFMT = %-9s ->  %s"
          % (name, oct(stat.S_IFMT(mode)), inode_kind(name)))
os.chmod("liar.txt", 0o644)
mode = os.lstat("liar.txt").st_mode
print("   The type is those four bits and nothing else. With the permissions")
print("   pinned to 0o644, st_mode splits exactly two ways:")
print("     st_mode        %s" % oct(mode))
print("     S_IFMT(mode)   %-9s the type" % oct(stat.S_IFMT(mode)))
print("     S_IMODE(mode)  %-9s the permissions" % oct(stat.S_IMODE(mode)))

print()
print("2. is_file() FOLLOWS SYMLINKS, AND ANSWERS False FOR SEVERAL REASONS")
print("   %-11s %-10s %-9s %-13s %s"
      % ("path", "is_file()", "is_dir()", "is_symlink()", "exists()"))
for name in ("liar.txt", "adir", "good_link", "dangling", "absent.txt"):
    p = pathlib.Path(name)
    print("   %-11s %-10s %-9s %-13s %s"
          % (name, p.is_file(), p.is_dir(), p.is_symlink(), p.exists()))
print("   Read the last two rows. 'dangling' is a symlink that is really")
print("   there, pointing at a name that is not; 'absent.txt' is nothing at")
print("   all. is_file() says False to both, and exists() says False to both,")
print("   because both follow the link. Only is_symlink() and os.lstat() can")
print("   tell them apart - and os.stat('dangling') raises FileNotFoundError")
print("   about a file whose directory entry you can plainly read.")

print()
print("3. mimetypes ASKS THE NAME AND NOTHING ELSE")
print("   It is a lookup table over the extension. It never opens the file,")
print("   so it is wrong in exactly the cases where the name is:")
for name in ("liar.txt", "real.png", "empty.png", "absent.txt", "notes.dat"):
    print("   %-11s guess_type -> %s" % (name, mimetypes.guess_type(name)[0]))
print("   Note the last two. 'absent.txt' does not exist and still gets an")
print("   answer, because nothing was consulted but the string. 'notes.dat'")
print("   gets None, which means 'no opinion about .dat' - never 'unknown")
print("   kind of file', and never 'this file is unreadable'.")

print()
print("4. ONLY READING THE BYTES ANSWERS THE QUESTION YOU MEANT")
print("   %-11s %-14s %-16s %s" % ("path", "by inode", "by name", "by bytes"))
for name in ("liar.txt", "real.png", "empty.png"):
    by_name = mimetypes.guess_type(name)[0] or "-"
    print("   %-11s %-14s %-16s %s"
          % (name, inode_kind(name), by_name, sniff(name)))
print("   Three columns, three questions, and on liar.txt three different")
print("   answers - none of them wrong. They were asked 'how is it stored',")
print("   'what is it called' and 'what is in it'. Only the third one opened")
print("   the file, and the standard library no longer ships a module that")
print("   does it: sniff() above is thirty lines you now write yourself.")

print()
print("5. subprocess ASKS A FIFTH QUESTION: CAN THE KERNEL LAUNCH IT?")
with open("with_shebang", "w") as fh:
    fh.write("#!/bin/sh\nexit 7\n")
with open("no_shebang", "w") as fh:
    fh.write("exit 7\n")
with open("not_executable", "w") as fh:
    fh.write("#!/bin/sh\nexit 7\n")
os.chmod("with_shebang", 0o755)
os.chmod("no_shebang", 0o755)
os.chmod("not_executable", 0o644)
for name in ("with_shebang", "no_shebang", "not_executable"):
    try:
        done = subprocess.run([os.path.abspath(name)])
        print("   %-15s ran, exit %d" % (name, done.returncode))
    except OSError as exc:
        print("   %-15s refused: %s, errno %d"
              % (name, type(exc).__name__, exc.errno))
print("   All three are regular, non-empty files holding shell script text,")
print("   and file-by-content would call all three the same thing. errno 8 is")
print("   ENOEXEC: the kernel read offset 0, found no '#!' and no ELF header,")
print("   and no handler claimed the bytes. errno 13 is EACCES: the bytes were")
print("   never looked at, because the execute bit was not set.")
print("   Run no_shebang from a shell instead and it works, because the SHELL")
print("   catches ENOEXEC and interprets the file itself. subprocess does not.")

shutil.rmtree(tmp, ignore_errors=True)
