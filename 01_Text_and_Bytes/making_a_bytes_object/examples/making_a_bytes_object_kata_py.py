"""Answer key: eight calls into the four-job constructor.

Exceptions print as type(exc).__name__ -- CPython rewords the message after it
between releases and this output is compared byte for byte.
"""


def evaluate(source):
    """(len, repr) of `source`, or ('--', the exception's type name)."""
    try:
        value = eval(source, {})
    except Exception as exc:  # noqa: BLE001 -- the kata is about which one
        return "--", type(exc).__name__
    return str(len(value)), repr(value)


CALLS = [
    ("bytes(3)", "the allocator: a SIZE, zero-filled"),
    ("bytes([3])", "one datum: the number 3, as a byte"),
    ("bytes('3', 'ascii')", "encode(), written backwards"),
    ("bytes.fromhex('03')", "the named door to the same thing as line 2"),
    ("bytes(True)", "bool is an int, so this is the allocator again"),
    ("bytes('3')", "no default encoding exists, so it refuses"),
    ("bytes([300])", "range(0, 256), and nothing is truncated"),
    ("bytes(3.0)", "a float has no __bytes__, no __index__, no buffer"),
]

print(f"     {'call':<22} {'len':>3}  {'result':<15} which job")
print("     " + "-" * 77)
for source, note in CALLS:
    length, value = evaluate(source)
    print(f"     {source:<22} {length:>3}  {value:<15} {note}")

print()
print("     WHICH TWO ARE EQUAL?")
print("     Lines 2 and 4. bytes([3]) and bytes.fromhex('03') are both the")
print("     single byte 0x03; everything else on the list is a different")
print("     length, a different value, or an exception.")
print()
pairs = [
    ("bytes([3])", "bytes.fromhex('03')"),
    ("bytes(3)", "bytes([3])"),
    ("bytes(True)", "bytes([1])"),
    ("bytes('3', 'ascii')", "bytes([3])"),
]
for left, right in pairs:
    same = eval(left, {}) == eval(right, {})
    print(f"     {left:<22} == {right:<22} {same}")

print()
print("     The third line is the one worth staring at. bytes(True) is not")
print("     b'\\x01' -- True is an int, the int branch is the allocator, and")
print("     the value you passed was used as a COUNT and then thrown away.")
print()
print("     THE ONE-LINE RULE")
print("     bytes(x) reads the TYPE of x, not the value. A number means")
print("     'this many zero bytes'. Everything named -- .encode(),")
print("     .fromhex(), .to_bytes() -- says in the call what bytes() says")
print("     only in the type of its argument, which is the whole argument")
print("     for preferring them.")
print()
print(f"     'Za'.encode('utf-8')      {'Za'.encode('utf-8')!r}")
print(f"     bytes.fromhex('5a61')     {bytes.fromhex('5a61')!r}")
print(f"     (23137).to_bytes(2, 'big') {(23137).to_bytes(2, 'big')!r}")
print("     Three spellings of the same two bytes, and none of them could")
print("     be mistaken for an allocation.")
