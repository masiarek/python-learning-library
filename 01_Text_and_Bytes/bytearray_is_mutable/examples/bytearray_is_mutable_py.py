"""bytearray is the one built-in binary type you can write into."""

import io
import struct


def attempt(label, action):
    """Run a one-liner and print either its result or the error it raised."""
    try:
        action()
        print(f"     {label:<28} ok")
    except Exception as exc:
        print(f"     {label:<28} {type(exc).__name__}: {exc}")


print("1. THERE IS NO bytearray LITERAL")
print(f"     b'AB'                        -> {b'AB'!r:<22} {type(b'AB').__name__}")
for expression, value in [
    ("bytearray(b'AB')", bytearray(b"AB")),
    ("bytearray([65, 66])", bytearray([65, 66])),
    ("bytearray('Łódź', 'utf-8')", bytearray("Łódź", "utf-8")),
    ("bytearray(4)", bytearray(4)),
]:
    print(f"     {expression:<28} -> {value!r}")
attempt("bytearray('Łódź')", lambda: bytearray("Łódź"))
print("\n     Every one of them is a function call. The literal is the bytes;")
print("     a bytearray is something you wrap around one.")
print("     bytearray(4) is the trap -- it is a SIZE, not the byte 4.")

print("\n2. WHAT MUTABLE MEANS: TWO NAMES, ONE BUFFER")
frozen = b"ab"
frozen_alias = frozen
frozen += b"c"
print(f"     bytes:      frozen = {frozen!r:<20} alias = {frozen_alias!r}")
buffer = bytearray(b"ab")
buffer_alias = buffer
buffer += b"c"
print(f"     bytearray:  buffer = {buffer!r:<20} alias = {buffer_alias!r}")
print(f"     alias is the same object: {buffer_alias is buffer}")
print("\n     += is not one operation. On bytes it rebinds a name and leaves")
print("     every other name pointing at the old value. On bytearray it edits")
print("     the object all of those names are looking at.")

print("\n3. THE FIVE THINGS bytes REFUSES")
DATA = b"abc"
BUF = bytearray(b"abc")


def bytes_setitem():
    DATA[0] = 65


def bytes_delitem():
    del DATA[0]


def bytes_slice_assign():
    DATA[0:2] = b"XYZ"


print("     on bytes:")
attempt("data[0] = 65", bytes_setitem)
attempt("del data[0]", bytes_delitem)
attempt("data[0:2] = b'XYZ'", bytes_slice_assign)
attempt("data.append(33)", lambda: DATA.append(33))
attempt("data.extend(b'de')", lambda: DATA.extend(b"de"))
print("     on bytearray:")
BUF[0] = 65
print(f"     {'buf[0] = 65':<28} -> {BUF!r}")
del BUF[1]
print(f"     {'del buf[1]':<28} -> {BUF!r}")
was = len(BUF)
BUF[0:2] = b"XYZ"
print(f"     {'buf[0:2] = b\'XYZ\'':<28} -> {BUF!r}   len {was} -> {len(BUF)}, slice assignment RESIZES")
BUF.append(33)
BUF.extend(b"de")
print(f"     {'buf.append(33); .extend()':<28} -> {BUF!r}")
print("\n     One byte on the left of = is an int, never a bytes:")
attempt("buf[0] = b'A'", lambda: BUF.__setitem__(0, b"A"))
attempt("buf[0] = 256", lambda: BUF.__setitem__(0, 256))
attempt("buf[99] = 1", lambda: BUF.__setitem__(99, 1))

print("\n4. WHAT MUTABILITY COSTS: THE HASH")
print(f"     bytearray(b'ab') == b'ab'    -> {bytearray(b'ab') == b'ab'}")
print(f"     b'ab' works as a dict key    -> {b'ab' in {b'ab': 1}}")
attempt("hash(bytearray(b'ab'))", lambda: hash(bytearray(b"ab")))
print("\n     Equal, and only one of them can be a dict key or a set member.")
print("     Same bargain as tuple against list: a hash has to keep its word,")
print("     and a buffer you can edit cannot make that promise.")

print("\n5. WHY IT EXISTS: SOMETHING ELSE WRITES INTO IT")
buf = bytearray(4)
n = io.BytesIO(b"WXYZ!!").readinto(buf)
print(f"     BytesIO(...).readinto(buf)   -> {n} bytes, buf = {buf!r}")
struct.pack_into(">I", buf, 0, 1000)
print(f"     struct.pack_into('>I', ...)  -> buf = {buf.hex(' ')}   ({int.from_bytes(buf, 'big')})")
view = memoryview(buf)
view[0:2] = b"ab"
print(f"     memoryview(buf)[0:2] = b'ab' -> buf = {buf!r}   (no copy)")
attempt("memoryview(b'abcd')[0:1]=b'a'", lambda: memoryview(b"abcd").__setitem__(slice(0, 1), b"a"))
print("\n     readinto, recv_into and pack_into all need a buffer the caller owns")
print("     and the callee may write. That is the job bytearray was added for;")
print("     being able to edit it yourself is the means, not the point.")
