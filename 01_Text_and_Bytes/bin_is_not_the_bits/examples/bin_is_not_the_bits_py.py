"""bin() prints a sign and a magnitude. The bits appear only once you choose a width."""

print("1. THREE FUNCTIONS, ONE FORMAT SPEC")
print("     bin(n) is format(n, '#b'); oct(n) is '#o'; hex(n) is '#x'.")
print()
print(f"     {'n':>5}   {'bin(n)':<14} {'oct(n)':<9} hex(n)")
print("     " + "-" * 40)
for n in (0, 9, 230, -9):
    print(f"     {n:>5}   {bin(n)!r:<14} {oct(n)!r:<9} {hex(n)!r}")
same = all(
    bin(n) == format(n, "#b") and oct(n) == format(n, "#o") and hex(n) == format(n, "#x")
    for n in range(-1000, 1001)
)
print()
print(f"     equal to format(n, '#b' / '#o' / '#x') for every n in -1000..1000:  {same}")
print(f"     bin(True)   {bin(True)!r}   a bool is an int, so it has __index__")
try:
    bin(1.0)
except TypeError as exc:
    print(f"     bin(1.0)    {type(exc).__name__}   a float has no __index__")

print("\n2. A NEGATIVE NUMBER PRINTS A SIGN, NOT ITS BITS")
print(f"     bin(9)      {bin(9)!r}")
print(f"     bin(-9)     {bin(-9)!r}   <- the same four digits, and a minus sign")
print()
print("     A Python int has no width. In two's complement -9 is ...11110111")
print("     with the ones running left forever -- that is the model &, | and")
print("     >> use -- so there is no finite pattern for bin() to print. It")
print("     prints the one finite thing it has: a sign, and the digits of |n|.")
print(f"     -9 >> 1000  = {-9 >> 1000}    <- a thousand places right, and still all ones")

print("\n3. CHOOSE A WIDTH AND THE BITS APPEAR")
print(f"     format(-9, '08b')          {format(-9, '08b')!r}   <- padded, still sign and magnitude")
print(f"     format(-9 & 0xFF, '08b')   {format(-9 & 0xFF, '08b')!r}   <- masked to eight bits first")
print()
print(f"     {'width':>5}   {'-9 & mask':>10}   the bits")
for width in (8, 16, 32):
    value = -9 & ((1 << width) - 1)
    print(f"     {width:>5}   {value:>10}   {value:0{width}b}")
raw = (-9).to_bytes(1, "big", signed=True)
print()
print(f"     raw = (-9).to_bytes(1, 'big', signed=True)   {raw!r}   = {raw[0]:08b}")
print("     Every width shows a different number of ones, and none of them is")
print("     wrong. The width is a decision -- a mask or a byte count -- and")
print("     the int never made it.")

print("\n4. READING IT BACK")
back = [
    ("int('0b1001', 0)", lambda: int("0b1001", 0), "base 0 reads the prefix"),
    ("int('0b1001', 2)", lambda: int("0b1001", 2), "and so does base 2"),
    ("int('-0b1001', 0)", lambda: int("-0b1001", 0), "the sign comes back too"),
    ("int('0b1001', 10)", lambda: int("0b1001", 10), "base 10 has no prefix to read"),
    ("int('11110111', 2)", lambda: int("11110111", 2), "the eight bits of -9, read as 247"),
    ("int.from_bytes(raw, 'big', signed=True)", lambda: int.from_bytes(raw, "big", signed=True), "told the width AND the sign"),
]
for label, call, note in back:
    try:
        got = repr(call())
    except ValueError as exc:
        got = type(exc).__name__
    print(f"     {label:<40} {got:<11} {note}")
print()
print("     bin() and int(s, 0) are inverses, sign included. The bits of -9")
print("     are not: read as base 2 they are 247, because a width and a")
print("     signedness went into them that the string does not carry.")

print("\n5. TWO METHODS THAT READ THE MAGNITUDE")
print(f"     {'n':>4}   {'bin(n)':<10} {'bit_length()':>12} {'bit_count()':>12}")
for n in (9, -9, 1, 0):
    print(f"     {n:>4}   {bin(n)!r:<10} {n.bit_length():>12} {n.bit_count():>12}")
print()
print("     -9 and 9 answer both the same way: both count |n|, the digits")
print("     bin() prints. The ones in a chosen width are another question:")
print(f"     (-9 & 0xFF).bit_count() = {(-9 & 0xFF).bit_count()}")
print()
print("     The docs define bit_length() as len(bin(n).lstrip('-0b')). lstrip")
print("     removes a SET of characters, not the prefix -- it works here only")
print("     because the digits left over start with 1, or are all zeros:")
print(f"     bin(0).lstrip('-0b') = {bin(0).lstrip('-0b')!r}, and (0).bit_length() = {(0).bit_length()}")
