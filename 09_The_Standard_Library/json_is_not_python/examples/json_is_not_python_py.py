"""json.dumps() writes JSON, which has six types, none of which is a tuple, a set or an int key."""

import datetime
import json
from decimal import Decimal

# Every expression below is eval'd, so the label printed IS the code that ran.
# An exception prints its type name only: the message is not API.
NS = {"json": json, "Decimal": Decimal, "datetime": datetime}


def ask(expr, note=""):
    try:
        val = repr(eval(expr, NS))
    except Exception as exc:
        val = type(exc).__name__
    print(f"     {expr:<52} {val:<30} {note}".rstrip())


print("1. THE SPELLINGS CHANGE ON THE WAY OUT, AND DO NOT CHANGE BACK")
ask("json.dumps(True)", "true, not True")
ask("json.dumps(None)")
ask("json.dumps((1, 2))", "a tuple goes out as a list")
ask("json.loads(json.dumps((1, 2)))", "and comes back as one")
ask("json.dumps({1: 'a'})", "an int key becomes a string key")
ask("json.loads(json.dumps({1: 'a'}))", "and stays one")
ask("json.dumps({True: 1, None: 2})")
ask("json.dumps({(1, 2): 'a'})", "a tuple key has no JSON spelling at all")

print("\n2. NOT EVERY VALUE HAS A SPELLING")
ask("json.dumps(b'x')", "bytes: decode first, or base64")
ask("json.dumps({1, 2})", "a set is not a list until you make it one")
ask("json.dumps(Decimal('0.1'))")
ask("json.dumps(datetime.date(2026, 9, 22))")
ask("json.dumps(datetime.date(2026, 9, 22), default=str)", "default= is asked for anything it cannot spell")

print("\n3. THE NUMBERS")
ask("json.dumps(0.1)", "repr(): the shortest string that reads back")
ask("json.dumps(1e16)")
ask("json.dumps(10**20)", "an int of any size goes out exactly")
ask("json.loads('100000000000000000000')", "and reads back exactly; JavaScript rounds it")
ask("json.loads('1e400')", "too big for a double: inf, and no error")
ask("json.dumps(float('nan'))", "NaN is not JSON: RFC 8259 has no such token")
ask("json.dumps(float('nan'), allow_nan=False)")
ask("json.loads('NaN')", "yet the reader accepts it")
ask("json.loads('01')", "a leading zero is not a JSON number")

print("\n4. THE TEXT")
ask("json.dumps('Łódź')", "ensure_ascii: every non-ASCII character escaped")
ask("json.dumps('Łódź', ensure_ascii=False)")
ask("json.loads(json.dumps('Łódź')) == 'Łódź'", "both spellings read back to the same str")
ask("json.loads(b'[1]')", "bytes are accepted: the encoding is sniffed")

print("\n5. THE KEYS")
ask("json.loads('{\"a\": 1, \"a\": 2}')", "a duplicate key: the last one wins, silently")
ask("json.dumps({'b': 1, 'a': 2})", "insertion order is kept")
ask("json.dumps({'b': 1, 'a': 2}, sort_keys=True)", "unless you ask for sorted")

print("\n6. WHAT SURVIVES A ROUND TRIP")
print(f"     {'value':<14} {'json.dumps(value)':<20} {'json.loads(...)':<18} equal?")
for value in [1, 1.0, True, None, "a", [1], (1,), {"k": 1}, {1: "a"}]:
    text = json.dumps(value)
    back = json.loads(text)
    print(f"     {value!r:<14} {text:<20} {back!r:<18} {back == value}")
