"""strip() takes a set of characters. removeprefix() takes a prefix. Not the same."""

import unicodedata

LINE = "Arthur: three!"
PREFIX = "Arthur: "

print("1. THE BUG, IN ONE LINE")
print(f"     line                          {LINE!r}")
print(f"     line.lstrip('Arthur: ')       {LINE.lstrip(PREFIX)!r}   <- not what anyone meant")
print(f"     line.removeprefix('Arthur: ') {LINE.removeprefix(PREFIX)!r}")
print()
print("     The 'thr' went with it. lstrip did not look for the prefix at")
print("     all -- it was handed a bag of characters and it ate every")
print("     leading character that was in the bag.")

print("\n2. THE ARGUMENT IS A SET, SO ORDER AND REPEATS MEAN NOTHING")
bag = sorted(set(PREFIX))
print(f"     'Arthur: ' as a set   {' '.join(repr(c) for c in bag)}")
print(f"     {len(PREFIX)} characters, {len(bag)} distinct")
print()
print("     Scanning from the left, stopping at the first character not in the bag:")
for i, ch in enumerate(LINE):
    verdict = "in the bag, eaten" if ch in PREFIX else "NOT in the bag -- stop"
    print(f"       {i:>2}  {ch!r:<5} {verdict}")
    if ch not in PREFIX:
        break
print()
print("     Every spelling of the same set does the same thing:")
for spelling in [PREFIX, " :Arthu", "rrrAAA uth:", "".join(bag)]:
    print(f"       lstrip({spelling!r:<14}) -> {LINE.lstrip(spelling)!r}")

print("\n3. THREE DIFFERENCES, NOT ONE")
print("     They are usually described as 'set vs prefix'. There are three,")
print("     and each one can bite on its own.")
print()
print(f"     {'':<16} {'lstrip(x)':<18} {'removeprefix(x)':<18} the difference")
print("     " + "-" * 80)
cases = [
    ("'aaab', 'a'", "aaab", "a", "repeats vs once"),
    ("'ababX', 'ab'", "ababX", "ab", "set vs whole string"),
    ("'three!', 'Q: '", "three!", "Q: ", "no match: both silent"),
]
for label, text, arg, note in cases:
    print(f"     {label:<16} {text.lstrip(arg)!r:<18} {text.removeprefix(arg)!r:<18} {note}")
print()
print("     (a) lstrip repeats until it stops matching; removeprefix runs once.")
print("     (b) lstrip splits its argument into characters; removeprefix does not.")
print("     (c) neither says anything when there was nothing to remove -- the")
print("         string comes back unchanged and you cannot tell the two cases")
print("         apart from the result. That is the third difference, and it is")
print("         the one both of them share.")

print("\n4. THE DOCS' OWN EXAMPLE, AND ONE THAT LOOKS SAFE")
print(f"     'www.example.com'.strip('cmowz.')   {'www.example.com'.strip('cmowz.')!r}")
print("     -- six characters, both ends, and 'example' survives because")
print("        'e', 'x', 'a', 'p' and 'l' are not in the bag.")
print()
print("     Now the one people actually write, to drop a file extension:")
for name in ["report.txt", "data.txt", "text.txt", "extract.txt"]:
    print(f"       {name!r:<15}.rstrip('.txt') -> {name.rstrip('.txt')!r:<12} "
          f"removesuffix -> {name.removesuffix('.txt')!r}")
print()
print("     One of the four is right, and it is right by accident: 'data'")
print("     happens to end in a letter that is not in the bag. That is the")
print("     worst possible outcome -- it passes whichever example you tried")
print("     first, and fails on a filename you have not seen yet.")

print("\n5. NO ARGUMENT MEANS str.isspace(), WHICH IS WIDER THAN 'SPACE'")
space_points = [cp for cp in range(0x110000) if chr(cp).isspace()]
print(f"     code points where str.isspace() is True:   {len(space_points)}")
by_cat = {}
for cp in space_points:
    by_cat.setdefault(unicodedata.category(chr(cp)), []).append(cp)
for cat in sorted(by_cat):
    points = [f"U+{cp:04X}" for cp in by_cat[cat]]
    head = f"       {cat}  {len(points):>2}   "
    for start in range(0, len(points), 10):
        print(head + " ".join(points[start:start + 10]))
        head = " " * len(head)
print()
sample = "\x1cshouting into the void "
print(f"     {sample!r}.strip()")
print(f"       -> {sample.strip()!r}")
print("     A file separator and a LINE SEPARATOR, both stripped, neither of")
print("     them a space. strip() with no argument means 'everything that")
print("     str.isspace() calls whitespace': the ten line boundaries, the")
print("     tab, the unit separator and seventeen space characters -- not")
print("     the four you can type on a keyboard.")
print()
print(f"     'abc'.strip('')     {'abc'.strip('')!r}   <- an empty bag removes nothing")
print(f"     'abc'.strip(None)   {'abc'.strip(None)!r}   <- None is the same as no argument")

print("\n6. bytes HAS THE SAME FIVE, AND THE SAME TRAP")
raw = b"Arthur: three!"
print(f"     raw                            {raw!r}")
print(f"     raw.lstrip(b'Arthur: ')        {raw.lstrip(b'Arthur: ')!r}")
print(f"     raw.removeprefix(b'Arthur: ')  {raw.removeprefix(b'Arthur: ')!r}")
print()
print("     Same five methods, same semantics, one difference: on bytes the")
print("     'set' is a set of byte VALUES, so a multi-byte character in the")
print("     argument becomes several independent bytes in the bag.")
polish = "Żubr: 3".encode()
print(f"     'Zubr: 3' with Z-dot, encoded  {polish!r}")
print(f"     .lstrip('Ż'.encode())          {polish.lstrip('Ż'.encode())!r}")
print("     Two bytes went into the bag and both were eaten, which happens")
print("     to be right here -- and would not be if either byte turned up")
print("     on its own inside a different character.")
