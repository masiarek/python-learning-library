"""Answer key: eight calls, and the one that is right by accident."""

CALLS = [
    ("'Arthur: three!'.lstrip('Arthur: ')", "the bag ate 'thr' as well"),
    ("'Arthur: three!'.removeprefix('Arthur: ')", "what everyone meant"),
    ("'aaab'.lstrip('a')", "lstrip REPEATS until it stops matching"),
    ("'aaab'.removeprefix('a')", "removeprefix runs ONCE, always"),
    ("'report.txt'.rstrip('.txt')", "the bag is {'.', 't', 'x'}"),
    ("'data.txt'.rstrip('.txt')", "right, and right by accident"),
    ("'abc'.strip('')", "an empty bag removes nothing"),
    ("'\\x1cabc\\u2028'.strip()", "a FILE SEPARATOR and a LINE SEPARATOR"),
]

print(f"     {'call':<44} {'result':<12} why")
print("     " + "-" * 96)
for source, note in CALLS:
    print(f"     {source:<44} {eval(source, {})!r:<12} {note}")

print()
print("     THREE DIFFERENCES, NOT ONE")
print("     They get collapsed into 'set versus prefix'. Lines 1-4 hold all")
print("     three, and each one can bite on its own:")
print("       (a) lstrip repeats, removeprefix runs once      (lines 3, 4)")
print("       (b) lstrip splits its argument into characters  (lines 1, 2)")
print("       (c) neither says anything when nothing matched  (below)")
print()
for source in ["'three!'.lstrip('Q: ')", "'three!'.removeprefix('Q: ')"]:
    print(f"     {source:<32} {eval(source, {})!r}")
print("     Same value as 'the prefix was there and I removed it' would")
print("     give. You cannot tell the two cases apart from the result, so if")
print("     the distinction matters -- and for a protocol or a filename it")
print("     does -- ask separately with startswith.")

print("\n     WHY ORDER AND REPEATS IN THE ARGUMENT MEAN NOTHING")
LINE = "Arthur: three!"
for spelling in ["Arthur: ", " :Arthu", "rrrAAA uth:", " :Ahrtu"]:
    print(f"     lstrip({spelling!r:<14}) -> {LINE.lstrip(spelling)!r}")
print("     Four spellings of one set, one answer. If the argument were a")
print("     prefix, only the first of those could possibly match. That is")
print("     the fastest proof available that it is a bag of characters.")

print("\n     THE ONE THAT SHIPS: LINE 6 IS RIGHT BY ACCIDENT")
print(f"     {'filename':<14} {'rstrip(.txt)':<14} {'removesuffix':<14} agree?")
print("     " + "-" * 56)
correct = 0
names = ["report.txt", "data.txt", "text.txt", "extract.txt"]
for name in names:
    stripped, suffixed = name.rstrip(".txt"), name.removesuffix(".txt")
    correct += stripped == suffixed
    print(f"     {name:<14} {stripped!r:<14} {suffixed!r:<14} {stripped == suffixed}")
print()
print(f"     {correct} of {len(names)} agree. 'data' survives because it happens to end")
print("     in a letter that is not in the bag -- nothing about the code")
print("     was right. That is the worst possible outcome: it passes whichever")
print("     example you tried first and fails on a filename you have not")
print("     seen yet. removesuffix is correct on all four, and")
print("     pathlib.Path(name).stem is correct on all four AND stops in the")
print("     right place on 'archive.tar.gz'.")

print("\n     WHAT LINE 8 REMOVED")
subject = "\x1cabc\u2028"   # a raw U+2028 here would be invisible to the author
print(f"     {subject!r}.strip()  ->  {subject.strip()!r}")
spaces = [chr(c) for c in range(0x110000) if chr(c).isspace()]
print(f"     code points where str.isspace() is True: {len(spaces)}")
print("     " + " ".join(f"U+{ord(c):04X}" for c in spaces[:10]))
print("     " + " ".join(f"U+{ord(c):04X}" for c in spaces[10:20]))
print("     " + " ".join(f"U+{ord(c):04X}" for c in spaces[20:]))
print()
print("     strip() with no argument means 'everything str.isspace() calls")
print("     whitespace' -- the ten line boundaries, the tab, the unit")
print("     separator and seventeen space characters. Not the four you can")
print("     type on a keyboard. That is usually what you want when cleaning")
print("     a CSV field, and it is worth knowing that it is what happened:")
print("     'I stripped whitespace' and 'I removed four specific characters'")
print("     are different claims about your data.")
