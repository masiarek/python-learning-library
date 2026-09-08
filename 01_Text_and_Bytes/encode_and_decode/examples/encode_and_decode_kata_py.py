"""Answer key: seven crossings of the boundary, and which of them lose data.

Exceptions print as type(exc).__name__ -- CPython rewords the message after it
between releases and this output is compared byte for byte.
"""


def evaluate(source):
    """repr of `source`, or 'raises <ExceptionType>'."""
    try:
        return repr(eval(source, {}))
    except Exception as exc:  # noqa: BLE001 -- the kata is about which one
        return f"raises {type(exc).__name__}"


CROSSINGS = [
    ("'€'.encode('cp1252')", "out", "cp1252 has the euro, at one byte"),
    ("'€'.encode('latin-1')", "out", "latin-1 predates it, and says so"),
    ("'€'.encode('ascii', 'replace')", "out", "'?' -- the euro is gone"),
    ("b'\\xff'.decode('latin-1')", "in", "latin-1 NEVER raises: 256 of 256"),
    ("b'\\xff'.decode('utf-8')", "in", "0xff cannot start a UTF-8 sequence"),
    ("b'\\xff'.decode('utf-8', 'replace')", "in", "U+FFFD -- a permanent record"),
    ("b'\\xff'.decode('utf-8', 'ignore')", "in", "the byte is simply gone"),
]

print(f"     {'expression':<36} {'dir':<4} {'result':<25} note")
print("     " + "-" * 97)
for source, direction, note in CROSSINGS:
    print(f"     {source:<36} {direction:<4} {evaluate(source):<25} {note}")

print()
print("     The 'dir' column is the half people get backwards, and there is")
print("     nothing to memorise: .encode() is only on str and .decode() is")
print("     only on bytes, so the method you can REACH tells you which type")
print("     you are already holding. Text lives inside Python; bytes are")
print("     what travel. Out is encode, in is decode.")

print("\n     WHICH ONES LOSE INFORMATION?")
original = "€"
for spec in ["'€'.encode('cp1252')", "'€'.encode('ascii', 'replace')"]:
    data = eval(spec, {})
    back = data.decode("cp1252") if "cp1252" in spec else data.decode("ascii")
    print(f"     {spec:<32} -> {data!r:<8} -> {back!r:<5} same: {back == original}")
print()
print("     Only one policy on the list is reversible, and it is not on the")
print("     list -- because it is the one nobody reaches for:")
raw = b"Za\xff\xfe\xc3\xb3"
decoded = raw.decode("utf-8", "surrogateescape")
reencoded = decoded.encode("utf-8", "surrogateescape")
print(f"     b'Za\\xff\\xfe\\xc3\\xb3'.decode('utf-8', 'surrogateescape')")
print(f"       -> {decoded!r}")
print(f"       -> re-encoded {reencoded!r}")
print(f"       -> identical to the original: {reencoded == raw}")
print()
print("     'replace' and 'ignore' are decisions to destroy data quietly.")
print("     'strict' is the default and the only one that loses nothing by")
print("     raising. 'surrogateescape' is the only one that loses nothing")
print("     by keeping -- which is how Python survives a filename that is")
print("     not valid UTF-8.")

print("\n     THE TRAP IN LINE 4")
print("     b'\\xff'.decode('latin-1') did not fail, and it was not right.")
print("     Every one of the 256 byte values is a character in latin-1, so")
print("     the call always succeeds -- which makes it genuinely useful as")
print("     a byte-preserving round trip and lethal as a guess. It turns")
print("     'I do not know this encoding' into 'here is some text' with no")
print("     error anywhere. If you have ever seen 'Ã³' where 'ó' belonged,")
print("     this is the mechanism:")
mojibake = "ó".encode("utf-8").decode("latin-1")
print(f"     'ó'.encode('utf-8').decode('latin-1')   {mojibake!r}")
print(f"     and back again                         "
      f"{mojibake.encode('latin-1').decode('utf-8')!r}")
