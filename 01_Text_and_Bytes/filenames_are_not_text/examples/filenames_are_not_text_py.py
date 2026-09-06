"""A filename is a bag of bytes. Python hands it to you as a str anyway.

Everything here is pure string and bytes work — no file is created, nothing is
written to disk. That is deliberate: what a *filesystem* accepts is the one
thing about filenames that is not portable, so the lesson page states those
answers in a dated table instead of recording them as an answer key.
"""

import os
import sys
import unicodedata
from pathlib import Path

print("1. WHAT IS ACTUALLY FORBIDDEN IN A NAME")
forbidden = [b for b in range(256) if bytes([b]) in (b"/", b"\x00")]
print(f"     byte values a POSIX name component may not contain: {len(forbidden)} of 256")
print(f"     they are: {forbidden}  =  {'/'!r} and NUL")
print("     Everything else is legal. Not 'legal text' -- legal.")
print()

print("2. SO A NAME NEED NOT BE TEXT AT ALL")
raw = b"caf\xe9"  # Latin-1 e-acute. Not valid UTF-8 in any position.
print(f"     raw name from the kernel   {raw!r}")
print(f"     sys.getfilesystemencoding()  {sys.getfilesystemencoding()!r}"
      f"  errors={sys.getfilesystemencodeerrors()!r}")
name = os.fsdecode(raw)
print(f"     os.fsdecode(raw)           {name!r}")
print("     U+DCE9 is a lone surrogate -- a code point with no character,")
print("     parked there to hold byte 0xE9 until someone asks for it back.")
print()

print("3. THE ROUND TRIP THAT IS GUARANTEED")
survived = sum(os.fsencode(os.fsdecode(bytes([b]))) == bytes([b]) for b in range(256))
print(f"     fsencode(fsdecode(b)) == b   for {survived} of 256 possible bytes")
print("     That is the whole promise: no name is lost by being decoded.")
print()

print("4. BUT THAT STR IS NOT A STRING YOU CAN USE")
try:
    name.encode("utf-8")
except UnicodeEncodeError as exc:
    print(f"     name.encode('utf-8')       raises {type(exc).__name__}")
print(f"     Path(name)                 {str(Path(name))!r}")
print("     pathlib holds a str, so it holds the surrogate too. open() and")
print("     os.stat() take it happily -- print(), json.dumps() and a socket")
print("     do not. The name is safe to *use* and unsafe to *display*.")
print()

print("5. AND 'THE SAME NAME' IS A FILESYSTEM'S OPINION")
nfc = "café"
nfd = unicodedata.normalize("NFD", nfc)
print(f"     nfc  {nfc!r:12} {len(nfc)} code points  {nfc.encode().hex()}")
print(f"     nfd  {nfd!r:12} {len(nfd)} code points  {nfd.encode().hex()}")
print(f"     nfc == nfd                 {nfc == nfd}")
print("     Two different byte strings. Whether they name two different files")
print("     is not Python's decision and not POSIX's -- see the table on the")
print("     page: one filesystem says yes, another says no.")
