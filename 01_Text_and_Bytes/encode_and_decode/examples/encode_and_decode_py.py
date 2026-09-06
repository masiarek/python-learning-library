"""encode() and decode() are directions, and errors= decides what gets thrown away."""

WORD = "Zażółć"          # Polish, and every letter of it is a decision

print("1. THE TWO DIRECTIONS")
print("     str  --encode()-->  bytes      leaving Python")
print("     bytes --decode()-->  str       entering Python\n")
data = WORD.encode("utf-8")
print(f"     {WORD!r}.encode('utf-8')   = {data!r}")
print(f"     {data!r}.decode('utf-8') = {data.decode('utf-8')!r}")

print("\n2. THE SAME TEXT IN FOUR ENCODINGS")
print("   Not four representations of one thing -- four different files.\n")
for codec in ("utf-8", "utf-16-le", "utf-32-le", "cp1250"):
    try:
        raw = WORD.encode(codec)
        print(f"     {codec:<10} {len(raw):>2} bytes  {' '.join(f'{b:02X}' for b in raw)}")
    except UnicodeEncodeError as exc:
        print(f"     {codec:<10} refused: {exc.reason} ({exc.object[exc.start]!r})")

print("\n3. WHAT A TABLE CANNOT HOLD")
print("   cp1250 is the Windows Central European table. It has Polish.")
print("   latin-1 does not, and says so rather than guessing:\n")
for codec in ("cp1250", "latin-1"):
    try:
        raw = WORD.encode(codec)
        print(f"     {codec:<10} ok    {raw!r}")
    except UnicodeEncodeError as exc:
        bad = exc.object[exc.start:exc.end]
        print(f"     {codec:<10} raises UnicodeEncodeError on {bad!r} at index {exc.start}")

print("\n4. THE errors= POLICIES, AND WHAT EACH ONE COSTS")
print("   Encoding 'Zażółć' to latin-1, which cannot represent it:\n")
for policy in ("strict", "ignore", "replace", "xmlcharrefreplace", "backslashreplace", "namereplace"):
    try:
        raw = WORD.encode("latin-1", errors=policy)
        print(f"     {policy:<20} {raw!r}")
    except UnicodeEncodeError:
        print(f"     {policy:<20} raises -- the default, and the only one that loses nothing")

print("\n5. THE ASYMMETRY WORTH KNOWING")
print("   'replace' on the way OUT writes '?'. On the way IN it writes U+FFFD.")
print("   Neither is reversible: the original is gone, and the file now says so.\n")
broken = b"Za\xff\xfe\xc3\xb3"
print(f"     {broken!r}")
print(f"       .decode('utf-8', 'replace')          -> {broken.decode('utf-8', 'replace')!r}")
print(f"       .decode('utf-8', 'ignore')           -> {broken.decode('utf-8', 'ignore')!r}")
print(f"       .decode('utf-8', 'backslashreplace') -> {broken.decode('utf-8', 'backslashreplace')!r}")
print(f"       .decode('latin-1')                   -> {broken.decode('latin-1')!r}")
print("\n     latin-1 never raises: every byte 00-FF is a character in it. That")
print("     makes it useful as a byte-preserving codec and lethal as a guess.")

print("\n6. THE ONE POLICY THAT IS REVERSIBLE")
print("   surrogateescape hides undecodable bytes in a private range and puts")
print("   them back byte-for-byte on the way out. This is how Python survives")
print("   a filename that is not valid UTF-8.\n")
smuggled = broken.decode("utf-8", "surrogateescape")
print(f"     decoded  -> {smuggled!r}")
print(f"     re-encoded -> {smuggled.encode('utf-8', 'surrogateescape')!r}")
print(f"     identical to the original: {smuggled.encode('utf-8', 'surrogateescape') == broken}")
