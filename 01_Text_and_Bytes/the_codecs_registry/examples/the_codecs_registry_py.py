#!/usr/bin/env python3
"""The codecs registry: what str.encode and bytes.decode cannot reach.

Three things live in the registry that the two methods have no door to:
codecs that are not text codecs, codecs as *objects* that hold state across
calls, and error handlers you write yourself. The middle one is where the
stream bugs are.

Deterministic: every chunk boundary below is chosen in this program. Nothing
is read from a socket, a file or a clock.
"""

import codecs
import unicodedata

TEXT = "Zażółć"
RAW = TEXT.encode("utf-8")

# A backslash may not appear inside an f-string expression before Python
# 3.12, so anything with an escape in it is built here and interpolated
# by name. This file must run on 3.11, the floor.
NL = "\n"


def rule(n, title):
    print()
    print(f"{n}. {title}")
    print("-" * 72)


print("THE CODECS REGISTRY")
print("=" * 72)
print("  str.encode / bytes.decode are two doors into a registry that has")
print("  more rooms than they can reach. This is a tour of the other rooms.")

# ---------------------------------------------------------------------------
rule(1, "NOT EVERY CODEC IN THE REGISTRY IS A TEXT CODEC")
print("   A CodecInfo carries a flag saying whether .encode()/.decode() may")
print("   use it. It is the flag, not a missing codec, that decides.")
print()
print(f"     {'name asked':12} {'canonical':12} {'text codec?':>11}   direction")
for name in ["utf-8", "latin-1", "rot13", "base64", "zlib", "hex"]:
    info = codecs.lookup(name)
    flag = "yes" if info._is_text_encoding else "no"
    direction = "str <-> bytes" if info._is_text_encoding else "not str <-> bytes"
    print(f"     {name:12} {info.name:12} {flag:>11}   {direction}")

print()
print("   So the two methods refuse them -- by name, and the message names")
print("   the door that does work:")
print()
for label, call in [
    ("'abc'.encode('rot13')", lambda: "abc".encode("rot13")),
    ("b'YWJj'.decode('base64')", lambda: b"YWJj".decode("base64")),
]:
    try:
        call()
    except LookupError as exc:
        print(f"     {label}")
        print(f"       {type(exc).__name__}: {exc}")

print()
print("   Through codecs.encode / codecs.decode the same names work, and")
print("   each one has its own pair of types:")
print()
for label, call in [
    ("codecs.encode('abc', 'rot13')", lambda: codecs.encode("abc", "rot13")),
    ("codecs.decode('nop', 'rot13')", lambda: codecs.decode("nop", "rot13")),
    ("codecs.encode(b'abc', 'base64')", lambda: codecs.encode(b"abc", "base64")),
    ("codecs.encode(b'abc', 'hex')", lambda: codecs.encode(b"abc", "hex")),
    ("codecs.encode('abc', 'base64')", lambda: codecs.encode("abc", "base64")),
]:
    try:
        print(f"     {label:34} -> {call()!r}")
    except TypeError as exc:
        print(f"     {label:34} !! {type(exc).__name__}")

print()
print("   rot13 is str->str. base64, hex and zlib are bytes->bytes.")
print("   Neither shape fits through a door typed str->bytes.")

# ---------------------------------------------------------------------------
rule(2, "A CHUNK BOUNDARY IS NOT A CHARACTER BOUNDARY")
print(f"   {TEXT!r} is {len(TEXT)} characters and {len(RAW)} UTF-8 bytes:")
print()
print(f"     {RAW.hex(' ')}")
print()
CUT = 3
print(f"   Read it in two chunks with the cut at byte {CUT}, which lands in")
print("   the middle of the two bytes that spell 'ż':")
print()
chunks = [RAW[:CUT], RAW[CUT:]]
for i, c in enumerate(chunks):
    print(f"     chunk {i}  {c.hex(' ')}")

print()
print("   Decoding each chunk on its own -- the obvious loop -- is wrong:")
print()
try:
    "".join(c.decode("utf-8") for c in chunks)
except UnicodeDecodeError as exc:
    print(f"     [c.decode('utf-8') for c in chunks]")
    print(f"       {type(exc).__name__}, reason: {exc.reason}")

print()
print("   And the usual reflex for that exception makes it worse, because")
print("   it stops raising and starts lying:")
print()
loud = "".join(c.decode("utf-8", "replace") for c in chunks)
print(f"     with errors='replace'  -> {loud!r}")
print(f"       characters: {len(loud)}, expected {len(TEXT)}")
print(f"       equal to the original text? {loud == TEXT}")
print("       no exception was raised. One character became two U+FFFD.")

# ---------------------------------------------------------------------------
rule(3, "A CODEC IS AN OBJECT, AND THE OBJECT REMEMBERS")
print("   codecs.getincrementaldecoder returns a class. An instance of it")
print("   keeps whatever it could not finish and uses it on the next call.")
print()
dec = codecs.getincrementaldecoder("utf-8")()
print(f"     fresh decoder, getstate() = {dec.getstate()}")
first = dec.decode(chunks[0])
print(f"     .decode(chunk 0) -> {first!r}      <- 'ż' is NOT here yet")
print(f"     getstate()        = {dec.getstate()}      <- it is here, held back")
second = dec.decode(chunks[1])
print(f"     .decode(chunk 1) -> {second!r}")
joined = first + second
print()
print(f"     joined -> {joined!r}   equal to the original? {joined == TEXT}")

print()
print("   The state is one incomplete sequence, so the chunk size does not")
print("   matter at all. One byte at a time is the worst case and it works:")
print()
dec = codecs.getincrementaldecoder("utf-8")()
per_byte = "".join(dec.decode(RAW[i:i + 1]) for i in range(len(RAW)))
nonempty = sum(1 for i in range(len(RAW)) if RAW[i:i + 1])
print(f"     {len(RAW)} calls of one byte each -> {per_byte!r}")
print(f"     equal to the original? {per_byte == TEXT}")

# ---------------------------------------------------------------------------
rule(4, "final=True IS THE OTHER HALF OF THE CONTRACT")
print("   Holding bytes back is right in the middle of a stream and wrong at")
print("   the end of one. The decoder cannot tell which it is in, so you say.")
print()
truncated = RAW[:-1]
print(f"     a truncated stream: {truncated.hex(' ')}")
dec = codecs.getincrementaldecoder("utf-8")()
print(f"     .decode(truncated)        -> {dec.decode(truncated)!r}")
print("       no error: a held byte is normal, more input may be coming")
try:
    dec.decode(b"", final=True)
except UnicodeDecodeError as exc:
    print(f"     .decode(b'', final=True)  !! {type(exc).__name__}")
    print(f"       reason: {exc.reason}")
print()
print("   Forget final=True and a truncated file decodes clean, one")
print("   character short, with nothing anywhere reporting it.")

# ---------------------------------------------------------------------------
rule(5, "THE ENCODER IS STATEFUL TOO, AND ITS BUG IS SILENT")
print("   The same split on the way out has no exception to warn you at all.")
print("   utf-16 begins with a byte order mark. One per stream -- but the")
print("   one-shot encoder does not know it is in a stream.")
print()
parts = ["Za", "żółć"]
naive = b"".join(p.encode("utf-16") for p in parts)
enc = codecs.getincrementalencoder("utf-16")()
incremental = b"".join(enc.encode(p) for p in parts)
one_shot = "".join(parts).encode("utf-16")
print(f"     join of per-part .encode()  {naive.hex(' ')}")
print(f"     incremental encoder         {incremental.hex(' ')}")
print(f"     one-shot, whole string      {one_shot.hex(' ')}")
print()
print(f"     incremental == one-shot?  {incremental == one_shot}")
print(f"     naive       == one-shot?  {naive == one_shot}")
print()
print(f"   The naive one is {len(naive) - len(one_shot)} bytes longer -- exactly one more mark --")
print("   and it decodes without error. What it decodes to is the problem:")
print()
smuggled = naive.decode("utf-16")
print(f"     {smuggled!r}")
for i, ch in enumerate(smuggled):
    if ord(ch) == 0xFEFF:
        print(f"       index {i} is U+{ord(ch):04X} {unicodedata.name(ch)}")
print(f"     equal to the original text? {smuggled == ''.join(parts)}")
print("     A second BOM in mid-stream is not a BOM. It is a zero-width")
print("     character in your data, and it prints as nothing.")

# ---------------------------------------------------------------------------
rule(6, "THE SAME SHAPE IS NOT THE SAME PROMISE")
print("   Every codec in the registry offers the incremental interface, non-")
print("   text ones included. Offering it and honouring it are different.")
print()
data = b"abcdefgh"
b64_one = codecs.encode(data, "base64")
enc = codecs.getincrementalencoder("base64")()
b64_chunked = enc.encode(data[:5]) + enc.encode(data[5:], final=True)
print(f"     base64 of {data!r} in one call  {b64_one!r}")
print(f"     the same bytes as 5 + 3          {b64_chunked!r}")
print(f"     identical?                       {b64_chunked == b64_one}")
try:
    back = codecs.decode(b64_chunked, "base64")
except Exception:
    back = None
print(f"     does it round-trip?              {back == data}")
print()
print("     Each chunk was padded as if it were the end of the stream, so")
print("     the result is malformed base64. What a decoder then does with")
print("     it is not even stable across Python versions: 3.11 and 3.12")
print("     return b'abcde' and report success, dropping three bytes;")
print("     3.13 and later raise binascii.Error. Only the line above is")
print("     true on all of them, which is why it is the one printed.")
print()
zdata = b"abc" * 40
enc = codecs.getincrementalencoder("zlib")()
z_chunked = enc.encode(zdata[:50]) + enc.encode(zdata[50:], final=True)
print(f"     zlib, same treatment: identical? "
      f"{z_chunked == codecs.encode(zdata, 'zlib')}")
print(f"     does it round-trip?              "
      f"{codecs.decode(z_chunked, 'zlib') == zdata}")
print()
print("   zlib streams. base64 does not. The type signature is identical.")

# ---------------------------------------------------------------------------
rule(7, "THE NINTH ERROR HANDLER IS THE ONE YOU WRITE")
print("   Python ships eight named policies. The list is a registry too, and")
print("   PEP 293 made it open. A handler is a function of one argument.")
print()
builtin = ["strict", "ignore", "replace", "xmlcharrefreplace",
           "backslashreplace", "namereplace", "surrogateescape",
           "surrogatepass"]
print(f"     built in: {len(builtin)}")
for n in builtin:
    print(f"       {n:20} {codecs.lookup_error(n).__name__}")

log = []


def audit(exc):
    """Replace what cannot be carried -- and record where it was."""
    if isinstance(exc, UnicodeDecodeError):
        bad = bytes(exc.object[exc.start:exc.end])
        log.append(("decode", exc.start, bad))
        return ("<" + bad.hex() + ">", exc.end)
    if isinstance(exc, UnicodeEncodeError):
        bad = exc.object[exc.start:exc.end]
        names = "+".join("U+%04X" % ord(c) for c in bad)
        log.append(("encode", exc.start, bad))
        return ("[" + names + "]", exc.end)
    raise exc


codecs.register_error("audit", audit)
print()
print("   Ten lines, and it is now a name like any other:")
print()
print(f"     codecs.lookup_error('audit') -> {codecs.lookup_error('audit').__name__}")
print()
decoded = b"caf\xe9 \xff au lait".decode("utf-8", "audit")
encoded = "Zażółć".encode("latin-1", "audit")
print(f"     b'caf\\xe9 \\xff au lait'.decode('utf-8', 'audit')")
print(f"       -> {decoded!r}")
print(f"     'Zażółć'.encode('latin-1', 'audit')")
print(f"       -> {encoded!r}")
print()
print("   One name, both directions, and the argument is a different")
print("   exception class each way. A handler that assumes one of them")
print("   raises AttributeError the first time it meets the other.")
print()
print("     the log the built-in handlers cannot give you:")
for entry in log:
    print(f"       {entry[0]:7} at {entry[1]:2}  {entry[2]!r}")

# ---------------------------------------------------------------------------
rule(8, "TWO THINGS THE CONTRACT REQUIRES THAT NOTHING ANNOUNCES")
print("   A handler returns (replacement, resume position). Both halves have")
print("   a rule, and neither is checked until it is broken.")
print()
calls = []


def counted(exc):
    calls.append((exc.start, exc.end, exc.object[exc.start:exc.end]))
    return ("?", exc.end)


codecs.register_error("counted", counted)
result = "Zażółć".encode("latin-1", "counted")
print("   First: it is called once per RUN, not once per character.")
print()
print(f"     'Zażółć'.encode('latin-1', 'counted') -> {result!r}")
print(f"     unencodable characters: 3, handler calls: {len(calls)}")
for start, end, obj in calls:
    print(f"       [{start}:{end}] {obj!r}")
print("     Returning one character for a run of two shortens the string,")
print("     which is how a 'replacement' loses a character count.")

print()
print("   Second: the position must move forward, or nothing ends.")
print()
n = [0]


def stuck(exc):
    n[0] += 1
    if n[0] > 3:
        raise RuntimeError("handler called %d times on one bad byte" % n[0])
    return ("", exc.start)


codecs.register_error("stuck", stuck)
try:
    b"a\xffb".decode("utf-8", "stuck")
except RuntimeError as exc:
    print(f"     a handler returning exc.start instead of exc.end:")
    print(f"       {type(exc).__name__}: {exc}")
print("     Uncaught, that is not an exception. It is a hang.")

print()
print("=" * 72)
print("Two methods reach the text codecs, one shot at a time, with the eight")
print("policies. Everything else in the registry -- the non-text codecs, the")
print("stateful objects, the ninth handler -- is reached through the module.")
