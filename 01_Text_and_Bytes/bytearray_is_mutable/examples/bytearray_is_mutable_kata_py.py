"""Answer key: what += did to the other name, and what mutability costs.

Exceptions print as type(exc).__name__ -- CPython rewords the message after it
between releases and this output is compared byte for byte.
"""

print("1. THE ALIAS")
frozen = b"abc"
buf = bytearray(b"abc")
alias_frozen, alias_buf = frozen, buf
frozen += b"d"
buf += b"d"
print(f"     frozen        {frozen!r}")
print(f"     alias_frozen  {alias_frozen!r:<20} <- unchanged")
print(f"     buf           {buf!r}")
print(f"     alias_buf     {alias_buf!r:<20} <- changed, and nobody touched it")
print()
print("     += is not one operation. On bytes it BUILDS a new object and")
print("     rebinds your name; every other name still points at the old")
print("     value. On bytearray it EDITS the object all of those names are")
print("     looking at. Same operator, two mechanisms.")
print(f"     alias_buf is buf   {alias_buf is buf}")

print("\n2. THE LENGTH YOU MEASURED A LINE AGO")
print(f"     buf            {buf!r}   len {len(buf)}")
buf[0:2] = b"XYZ"
print(f"     buf[0:2] = b'XYZ'   -> {buf!r}   len {len(buf)}")
print()
print("     Two bytes out, three in, and the buffer grew. Slice assignment")
print("     resizes -- which a fixed-length byte array in Java, C or")
print("     JavaScript cannot do, and which means len() is not a property")
print("     of the buffer you can cache.")

print("\n3. THE LOOKUP THAT RAISES")
table = {b"key": "the value"}
print(f"     bytearray(b'key') == b'key'   {bytearray(b'key') == b'key'}")
try:
    table[bytearray(b"key")]
except Exception as exc:  # noqa: BLE001 -- the kata is about which one
    print(f"     table[bytearray(b'key')]      raises {type(exc).__name__}")
print()
print("     Equal, and only one of them can be a dict key. This is not")
print("     'the key is missing' -- it is 'that object cannot be a key at")
print("     all', which is why it raises instead of returning a default.")
print("     A hash is a promise about future comparisons, and a buffer you")
print("     can edit cannot make it. Same bargain as tuple against list.")
print("     .get() does not save you either:")
try:
    table.get(bytearray(b"key"))
except Exception as exc:  # noqa: BLE001
    print(f"     table.get(bytearray(b'key'))  raises {type(exc).__name__}")

print("\n4. THE CONSTRUCTOR IT INHERITED")
for source in ["bytearray(2)", "bytearray([2])", "bytearray(b'2')"]:
    value = eval(source, {})
    print(f"     {source:<18} {value!r:<24} len {len(value)}")
print()
print("     The same four-job dispatch bytes() has: a number is a SIZE, a")
print("     list is data, and b'2' is the digit -- the byte 0x32, not 2.")
print("     Three spellings, three different buffers, and only one of them")
print("     holds anything you typed.")

print("\n5. WHICH OF THE FOUR ANSWERS THE 'WHY DOES IT EXIST' QUESTION?")
print("     Section 1. Everything else on this page is a consequence of")
print("     one capability: something that is not you can write into the")
print("     buffer. readinto, recv_into and pack_into need a buffer the")
print("     caller owns and the callee may fill, and that is the job the")
print("     type was added for. Being able to edit it yourself is the")
print("     means, not the point -- and the hash in section 3 is the price.")
