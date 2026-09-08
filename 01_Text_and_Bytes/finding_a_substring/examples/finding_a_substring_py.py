"""Four ways to ask where a substring is. They agree on the hit and disagree on the miss."""

LINE = "spam, spam, eggs and spam"
MISSING = "Lancelot"
TITLE = "Monty Python"


def failure(call):
    """Run call() and report the exception type and message, or the value."""
    try:
        return repr(call())
    except Exception as exc:
        return f"{type(exc).__name__}: {exc}"


def failure_type(call):
    """Same, but the type name only -- for a message CPython has reworded."""
    try:
        return repr(call())
    except Exception as exc:
        return type(exc).__name__


print("1. FOUR WAYS TO ASK, ONE ANSWER")
print(f"     line                     {LINE!r}")
print(f"     'eggs' in line           {'eggs' in LINE!r}")
print(f"     line.find('eggs')        {LINE.find('eggs')!r}")
print(f"     line.index('eggs')       {LINE.index('eggs')!r}")
print(f"     line.partition('eggs')   {LINE.partition('eggs')!r}")
print()
print("     All four found the same thing in the same place. Nothing on")
print("     this page is about the hit.")

print("\n2. THE SAME FOUR ON A MISS -- THIS IS THE WHOLE LESSON")
print(f"     the needle is {MISSING!r}, which is not in the line")
print()
print(f"     {MISSING!r} in line          {MISSING in LINE!r:<8} a bool, and you have to test it")
print(f"     line.find({MISSING!r})       {LINE.find(MISSING)!r:<8} an int -- and a valid index")
print(f"     line.index({MISSING!r})      {failure(lambda: LINE.index(MISSING))}")
print(f"     line.partition({MISSING!r})  {LINE.partition(MISSING)!r}")
print()
print("     One of the four says so out loud. Two hand back a value that")
print("     the next line of code will happily use. And 'in' cannot be")
print("     misread, because False is the only thing it knows how to say.")

print("\n3. THE TRUTH VALUE OF find() IS EXACTLY BACKWARDS")
print("     0 means 'found, at the very start' and is falsy.")
print("     -1 means 'not there at all' and is truthy.")
print()
print(f"     {'needle':<12} {'find':>5} {'bool(r)':>8} {'r > 0':>7} {'r > -1':>7} {'r >= 0':>7}")
print("     " + "-" * 50)
for needle in ("spam", "eggs", MISSING):
    r = LINE.find(needle)
    print(f"     {needle!r:<12} {r:>5} {bool(r)!r:>8} {r > 0!r:>7} {r > -1!r:>7} {r >= 0!r:>7}")
print()
print("     Read bool(r) against the last two columns. Only a comparison")
print("     with a number agrees with 'in' on all three rows:")
print()
print("       if line.find(needle):          WRONG -- False at position 0,")
print("                                      and True on a miss. Both ways.")
print("       if line.find(needle) > 0:      WRONG -- False at position 0.")
print("       if line.find(needle) > -1:     right")
print("       if line.find(needle) >= 0:     right")
print("       if needle in line:             right, and it says what it means")
print()
print("     The first one is not one bug, it is two: it misses a match at")
print("     the start and it accepts a miss anywhere.")

print("\n4. -1 IS A VALID INDEX, WHICH IS WHY THE MISS STAYS QUIET")
at = LINE.find(MISSING)
print(f"     at = line.find({MISSING!r})   ->  {at!r}")
print(f"     line[at:]   {LINE[at:]!r}")
print("                 -- the last character, not ''")
print(f"     line[:at]   {LINE[:at]!r}")
print("                 -- everything except the last character")
print(f"     line[at]    {LINE[at]!r}")
print("                 -- no IndexError either: -1 counts from the end")
print()
found = LINE.find("eggs")
print(f"     On a hit (at = {found}) the same line is what you meant:")
print(f"     line[at:]   {LINE[found:]!r}")
print()
print("     Nothing raised. Nothing logged. A search that found nothing")
print("     returned the last character of the string. That is the bug")
print("     the docs are steering you away from when they say to use")
print("     find only if you need the position.")
print(f"     line.index({MISSING!r}) would have stopped here instead:")
print(f"       {failure(lambda: LINE.index(MISSING))}")

print("\n5. partition AND rpartition FAIL IN MIRROR IMAGE")
print(f"     {TITLE!r}.partition('-')    {TITLE.partition('-')!r}")
print(f"     {TITLE!r}.rpartition('-')   {TITLE.rpartition('-')!r}")
print()
print("     Neither raised. The separator field is empty in both, and")
print("     that is the only field that tells you anything went wrong.")
print("     The string itself moved from the FIRST slot to the THIRD.")
print()
h1, s1, t1 = TITLE.partition("-")
h2, s2, t2 = TITLE.rpartition("-")
print(f"     head, sep, tail = title.partition('-')    head {h1!r:<16} tail {t1!r}")
print(f"     head, sep, tail = title.rpartition('-')   head {h2!r:<16} tail {t2!r}")
print("     Two lines that differ by one letter put your data in")
print("     different variables, and neither one complains.")
print()
print("     They differ on a hit too -- first separator against last:")
print(f"       'a-b-c'.partition('-')    {'a-b-c'.partition('-')!r}")
print(f"       'a-b-c'.rpartition('-')   {'a-b-c'.rpartition('-')!r}")

print("\n6. THE MIRROR IS DELIBERATE: EACH ONE IS RIGHT FOR ITS OWN JOB")
print("     partition splits off the FIRST field and keeps the rest:")
for setting in ("timeout=30", "DEBUG"):
    key, _, value = setting.partition("=")
    print(f"       {setting!r:<14} key {key!r:<12} value {value!r}")
print("       A flag with no '=' is a key with no value. Right answer.")
print()
print("     rpartition splits off the LAST field and keeps the rest:")
for path in ("usr/share/doc/spam.txt", "spam.txt"):
    parent, _, name = path.rpartition("/")
    print(f"       {path!r:<26} dir {parent!r:<20} name {name!r}")
print("       A bare filename is a name with no directory. Right answer.")
print()
print("     In both cases the whole string lands in the field that wanted")
print("     it. Pick by which end you are scanning from -- and then read")
print("     the separator field, because it is the one that knows.")

print("\n7. THE UNPACK THAT RAISES, AND THE ONE THAT NEVER DOES")


def split_unpack():
    key, value = "DEBUG".split("=", 1)
    return key, value


print("     key, value      = 'DEBUG'.split('=', 1)")
print(f"       {failure(split_unpack)}")
print("     key, sep, value = 'DEBUG'.partition('=')")
print(f"       {'DEBUG'.partition('=')!r}")
print()
print("     Same job, two failure styles. partition's tuple is three")
print("     long whatever happens, so the unpack is total and the")
print("     traceback never arrives. The separator field is falsy on a")
print("     miss and truthy on a hit -- 'if not sep' is the test, and")
print("     no other field in the tuple can answer the question.")

print("\n8. start AND end ARE SLICE NOTATION -- THE RESULT IS NOT")
S = "spam, spam"
print(f"     s = {S!r}")
print(f"     s.find('sp', 5)     {S.find('sp', 5):>3}   an offset into s")
print(f"     s[5:].find('sp')    {S[5:].find('sp'):>3}   an offset into the slice")
print(f"     s[5:] is {S[5:]!r}")
print()
print("     The window is s[start:end]; the number handed back is an")
print("     index into s. That is the useful half -- you can slice with it.")
print()
print("     Out-of-range and negative behave like slicing, not like errors:")
print(f"       s.find('sp', -4)    {S.find('sp', -4):>3}")
print(f"       s.find('sp', 99)    {S.find('sp', 99):>3}")
print(f"       s.find('a', -100)   {S.find('a', -100):>3}")
print()
print("     And 'end' can cut a match in half:")
print(f"       s.find('am', 0, 3)  {S.find('am', 0, 3):>3}   s[0:3] is {S[0:3]!r}")
print(f"       s.find('am', 0, 4)  {S.find('am', 0, 4):>3}   s[0:4] is {S[0:4]!r}")
print("     'am' sits at index 2 in both. It is the window that moved.")

print("\n9. THE EMPTY NEEDLE IS EVERYWHERE -- EXCEPT PAST THE END")
E = "spam"
empty_rows = [
    ("'' in 'spam'", "'' in E", "" in E, ""),
    ("'spam'.find('')", "find", E.find(""), ""),
    ("'spam'.rfind('')", "rfind", E.rfind(""), "len(s): a slice bound, not an index"),
    ("'spam'.count('')", "count", E.count(""), "n + 1 gaps between n characters"),
    ("'spam'.find('', 2)", "find", E.find("", 2), ""),
    ("'spam'.find('', 99)", "find", E.find("", 99), "even '' can be reported missing"),
]
for label, _, value, note in empty_rows:
    print(f"     {label:<20} {value!r:>5}   {note}".rstrip())
print()
print("     The separator families refuse it outright:")
for method in ("partition", "rpartition", "split"):
    print(f"       {E!r}.{method}('')".ljust(30) + failure(lambda m=method: getattr(E, m)("")))
print()
print("     So partition is not 'the one that never raises'. It never")
print("     raises about the DATA. It still raises about the SEPARATOR.")

print("\n10. ON bytes, AN INT IS A NEEDLE")
B = b"spam"
print(f"     b'sp' in b'spam'     {b'sp' in B!r}")
print(f"     115 in b'spam'       {115 in B!r}   115 is ord('s')")
print(f"     b'spam'.find(115)    {B.find(115)!r}")
print(f"     115 in 'spam'        {failure(lambda: 115 in E)}")
print(f"     'spam'.find(115)     {failure_type(lambda: E.find(115))}   (message reworded in 3.13)")
print()
print("     The same expression means different things on the two types.")
print("     On bytes an int asks about one byte VALUE; on str it is")
print("     refused, because a str has no members that are not strings.")

print("\n11. THE OFFSET COUNTS CODE POINTS, NOT BYTES")
Z = "żółw"
print(f"     s = {Z!r}   {len(Z)} characters, {len(Z.encode())} bytes in UTF-8")
print(f"     s.find('w')            {Z.find('w'):>3}   code points")
print(f"     s.encode().find(b'w')  {Z.encode().find(b'w'):>3}   bytes")
print(f"     s[3:] is {Z[3:]!r}")
print()
print("     Both numbers are right; they answer different questions.")
print("     Python's str search counts characters, which is the number a")
print("     person means -- and is not the number a byte buffer wants.")

print("\n12. WHY THERE ARE TWO NAMES FOR ONE SEARCH")
print(f"     {'type':<12} {'.find':>7} {'.index':>7}")
print("     " + "-" * 28)
for sample, label in ((["a"], "list"), (("a",), "tuple"), (range(1), "range"),
                      ("a", "str"), (b"a", "bytes"), (bytearray(b"a"), "bytearray")):
    print(f"     {label:<12} {hasattr(sample, 'find')!r:>7} {hasattr(sample, 'index')!r:>7}")
print()
print("     index belongs to the sequence protocol, and every sequence")
print("     that has it answers a miss the same way:")
print(f"       [1, 2].index(9)     {failure_type(lambda: [1, 2].index(9))}")
print(f"       (1, 2).index(9)     {failure_type(lambda: (1, 2).index(9))}")
print(f"       range(2).index(9)   {failure_type(lambda: range(2).index(9))}")
print(f"       'spam'.index('9')   {failure_type(lambda: E.index('9'))}")
print("     (the type only: CPython reworded two of those four in 3.14,")
print("      which is why an answer key prints the type and not the text)")
print()
print("     find is text-only: it is the convenience that trades the")
print("     exception for a sentinel. There is no list.find, so there")
print("     is nowhere else in the language to write the -1 bug.")
print()
print("     One more asymmetry in the same direction:")
print(f"       'spam'.startswith(('sp', 'eg'))   {E.startswith(('sp', 'eg'))!r}   a tuple of alternatives")
print(f"       'spam'.find(('sp', 'eg'))         {failure_type(lambda: E.find(('sp', 'eg')))}   (message reworded in 3.13)")
print("     startswith and endswith take a tuple. find, index, count,")
print("     partition and 'in' all take exactly one needle.")
