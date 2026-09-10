"""Kata answers: eight one-liners about bin(), and the two that were given a width."""

ROWS = [
    ("bin(-1)", "a sign, and a magnitude of one"),
    ("bin(-1 & 0xFF)", "masked to eight bits: now it is the bits"),
    ("bin(True)", "a bool is an int, so it has __index__"),
    ("format(-5, '08b')", "the zeros go AFTER the sign"),
    ("int('-0b101', 0)", "base 0 reads the sign and the prefix"),
    ("int('0b101', 10)", "base 10 has no prefix to read"),
    ("(128).to_bytes(1, 'big', signed=True)", "a signed byte stops at 127"),
    ("(-5).bit_count()", "the ones of |n|, and 5 is 101"),
]

print(f"     {'expression':<40} {'result':<14} note")
print("     " + "-" * 86)
for source, note in ROWS:
    try:
        result = repr(eval(source))
    except (ValueError, OverflowError) as exc:
        result = type(exc).__name__
    print(f"     {source:<40} {result:<14} {note}")

print()
print("     THE RULE")
print("     Lines 2 and 7 are the only two that were given a width -- a mask")
print("     and a byte count. One prints eight bits; the other refuses 128,")
print("     because a signed byte stops at 127. Every other line writes or")
print("     reads a minus sign and the digits of |n|, which is all an int")
print("     without a width has to offer.")
print()
print("     THE ONE THAT LOOKS RIGHT")
print("     format(-5, '08b') is eight characters wide, which is the shape of")
print("     a byte, and it is not one: it is a minus sign and seven digits of")
print("     5. A width in a format spec pads the TEXT; only a mask or")
print("     to_bytes() chooses a width for the NUMBER.")
