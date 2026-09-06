"""str and bytes are two types, and Python 3 will not mix them for you."""

TEXT = "Łódź"                      # a str: four characters
DATA = TEXT.encode("utf-8")        # a bytes: seven bytes

print("1. TWO TYPES, ONE WORD")
print(f"     {TEXT!r:<24} {type(TEXT).__name__:<6} len = {len(TEXT)}")
print(f"     {DATA!r:<24} {type(DATA).__name__:<6} len = {len(DATA)}")
print("\n     Same word. Different length. len() is not one question.")

print("\n2. WHAT len() COUNTS")
print("     str   -> code points")
print("     bytes -> bytes\n")
for ch in TEXT:
    n = ch.encode("utf-8")
    print(f"     {ch}  U+{ord(ch):04X}  {len(n)} byte(s)  {' '.join(f'{b:02X}' for b in n)}")

print("\n3. INDEXING GIVES YOU DIFFERENT THINGS")
print(f"     TEXT[0] = {TEXT[0]!r:<10} a one-character str")
print(f"     DATA[0] = {DATA[0]!r:<10} an int -- the number 0-255")
print(f"     DATA[0:1] = {DATA[0:1]!r:<8} slicing bytes gives bytes")
print("\n     Iterating bytes gives ints, not one-byte bytes. This is the")
print("     single most surprising line in the whole type.")

print("\n4. THE BOUNDARY PYTHON REFUSES TO CROSS")
for expression, run in [
    ('"a" + b"b"',        lambda: "a" + b"b"),
    ('"Łódź" == b"\\xc5\\x81\\xc3\\xb3d\\xc5\\xba"', lambda: TEXT == DATA),
    ('b"x".startswith("x")', lambda: b"x".startswith("x")),
]:
    try:
        result = run()
        print(f"     {expression:<44} -> {result!r}")
    except TypeError as exc:
        print(f"     {expression:<44} -> TypeError: {exc}")

print("\n     The middle one is the trap: it does not raise, it just says False.")
print("     A str is never equal to a bytes, however identical they look.")

print("\n5. THE ONLY TWO DOORS BETWEEN THEM")
print(f"     TEXT.encode('utf-8')  -> {TEXT.encode('utf-8')!r}")
print(f"     DATA.decode('utf-8')  -> {DATA.decode('utf-8')!r}")
print(f"     round trip is exact:     {DATA.decode('utf-8') == TEXT}")
print("\n     .encode() is only on str. .decode() is only on bytes. The method")
print("     you can reach tells you which type you are holding.")
