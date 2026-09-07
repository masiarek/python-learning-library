"""bytes() is several constructors sharing one name, and the argument's type picks."""

TEXT = "Łódź"


def show(expression, call, width=34):
    """Print an expression next to what it evaluates to -- or the error it raises."""
    try:
        print(f"     {expression:<{width}} -> {call()!r}")
    except Exception as exc:            # the exception IS the lesson on three lines below
        print(f"     {expression:<{width}} !! {type(exc).__name__}: {exc}")


print("1. ONE NAME, FOUR JOBS")
show("bytes()", lambda: bytes())
show("bytes(5)", lambda: bytes(5))
show("bytes([5])", lambda: bytes([5]))
show("bytes('hi', 'utf-8')", lambda: bytes("hi", "utf-8"))
print("\n     Nothing in the call says which job you wanted. The TYPE of the")
print("     argument chose it, and the four answers have nothing in common:")
print("     empty, a buffer, one datum, and an encoding.")

print("\n2. THE TWO THAT LOOK ALIKE")
show("bytes(5)", lambda: bytes(5))
show("bytes([5])", lambda: bytes([5]))
show("str(5)", lambda: str(5))
show("bytes(True)", lambda: bytes(True))
show("bytes(-1)", lambda: bytes(-1))
print("\n     bytes(5) is FIVE zero bytes -- a buffer of that size. bytes([5])")
print("     is ONE byte holding 5 -- a value. str(5) is the digit, which is")
print("     what a reader expects bytes(5) to be. And True is an int, so")
print("     bytes(True) is one zero byte and never b'\\x01'.")

print("\n3. PYTHON WILL NOT GUESS AN ENCODING")
show("bytes('Łódź')", lambda: bytes(TEXT))
show("bytes('Łódź', 'utf-8')", lambda: bytes(TEXT, "utf-8"))
show("bytes('Łódź', 'latin-1')", lambda: bytes(TEXT, "latin-1"))
show("bytes('Łódź', 'ascii', 'replace')", lambda: bytes(TEXT, "ascii", "replace"))
show("'Łódź'.encode()", lambda: TEXT.encode())
print("\n     The two-argument form is .encode() written backwards, and the")
print("     third argument is errors=. The bare call is the only one of the")
print("     four jobs Python refuses outright: there is no default encoding.")

print("\n4. THE ITERABLE FORM CHECKS EVERY VALUE")
show("bytes([72, 105])", lambda: bytes([72, 105]))
show("bytes(range(5))", lambda: bytes(range(5)))
show("bytes(x * 2 for x in [1, 2])", lambda: bytes(x * 2 for x in [1, 2]))
show("bytes([256])", lambda: bytes([256]))
show("bytes([-1])", lambda: bytes([-1]))
show("bytes([1.0])", lambda: bytes([1.0]))
print("\n     Every element has to be an int in range(0, 256). Nothing is")
print("     truncated, rounded or wrapped -- the call fails instead.")


class Bytesish:
    def __bytes__(self):
        return b"__bytes__ ran"


class Indexish:
    def __index__(self):
        return 3


class Both:
    def __bytes__(self):
        return b"__bytes__ won"

    def __index__(self):
        return 3


print("\n5. HOW THE JOB IS CHOSEN")
show("bytes(Bytesish())   __bytes__", lambda: bytes(Bytesish()))
show("bytes(Indexish())   __index__", lambda: bytes(Indexish()))
show("bytes(Both())       both", lambda: bytes(Both()))
show("bytes(3.0)          neither", lambda: bytes(3.0))
print("\n     The ladder: an encoding argument means 'encode this str'; then")
print("     __bytes__ if the object has one; then __index__ for the zero-fill;")
print("     then the buffer protocol; then any iterable of ints. A float has")
print("     none of those, so it is not 'rounded' -- it is refused.")

print("\n6. THE OTHER DOORS INTO bytes")
show("bytes.fromhex('c5 81')", lambda: bytes.fromhex("c5 81"))
show("(321).to_bytes(2, 'big')", lambda: (321).to_bytes(2, "big"))
show("bytes(bytearray(b'ab'))", lambda: bytes(bytearray(b"ab")))
show("bytes(memoryview(b'mv'))", lambda: bytes(memoryview(b"mv")))
print("\n     Three of these say in their names what bytes() says only in the")
print("     type of its argument. That is the whole argument for preferring")
print("     them: .encode() cannot be mistaken for an allocation.")
