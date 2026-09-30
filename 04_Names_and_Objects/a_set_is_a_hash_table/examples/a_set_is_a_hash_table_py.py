#!/usr/bin/env python3
"""A set is a hash table: every surprise in Python's set, checked by running it.

Run:  python3 a_set_is_a_hash_table_py.py

Mathematics gives a set one rule: it is its members and nothing else, so
order and repeats do not exist. Python's set keeps that rule and adds one
of its own, because it is a hash table: membership is decided by hash and
==, so members must be hashable. Almost every gotcha follows from one of
those two rules, or from a third, smaller one: operators insist on sets,
methods accept any iterable. Every set is printed sorted, because its own
iteration order is an accident of storage and changes between runs for
strings. Exceptions are printed by type name only: CPython rewords the
messages between releases.
"""

from collections import deque


def show(s) -> str:
    """A set printed in sorted order, so the output is stable."""
    if not s:
        return "set()"
    return "{" + ", ".join(repr(x) for x in sorted(s, key=lambda x: (str(type(x)), x))) + "}"


def attempt(code: str, env: dict) -> str:
    """Evaluate code and describe the result, or the exception it raised."""
    try:
        value = eval(code, env)
    except Exception as e:
        return type(e).__name__
    if isinstance(value, (set, frozenset)):
        return f"{type(value).__name__} {show(value)}"
    return repr(value)


def main() -> None:
    print("1. CREATING A SET: WHICH OF THESE IS {'a', 'b', 'c'}?")
    target = {"a", "b", "c"}
    for code in ["set('abc')", "set(['a', 'b', 'c'])", "set('a', 'b', 'c')",
                 "{'a', 'b', 'c'}", "{('a', 'b', 'c')}"]:
        result = attempt(code, {})
        try:
            ok = eval(code) == target
        except TypeError:
            ok = False
        print(f"   {code:<24} {'yes' if ok else 'no ':<4} {result}")
    print("   set(x) takes ONE iterable and adds each thing it yields;")
    print("   braces take each thing written between them, whole.")
    print(f"   set('foo') = {show(set('foo'))}      {{'foo'}} = {show({'foo'})}")
    print(f"   type({{}}) = {type({}).__name__}         type(set()) = {type(set()).__name__}"
          "      the empty set has no literal")
    first_set = set()
    for code in ["CP0140.1", "XJ8113.5", "EF3616.3"]:
        first_set.add(code)
    print(f"   built by add(), one at a time:  {show(first_set)}")
    print(f"   comprehension {{2*x for x in [1, 2, 3]}} = {show({2 * x for x in [1, 2, 3]})}")
    print()

    print("2. MEMBERSHIP IS DECIDED BY hash AND ==")
    mixed = {True, 1, 1.0, "1", (1,)}
    print(f"   {{True, 1, 1.0, '1', (1,)}} has {len(mixed)} members, not 5:")
    print(f"   True == 1 == 1.0 is {True == 1 == 1.0}, and hash(True) == hash(1) == hash(1.0) is"
          f" {hash(True) == hash(1) == hash(1.0)}")
    print("   so the three are one member; the first one written is the one kept.")
    for code in ["{[1, 2]}", "{tuple([1, 2, 1])}", "{frozenset({1, 2})}", "{(1, [2])}"]:
        print(f"   {code:<22} -> {attempt(code, {})}")
    s1, s2 = {"a", "b", "c"}, {"c", "d", "e"}
    env = {"s1": set(s1), "s2": s2}
    print(f"   s1.add(s2)             -> {attempt('s1.add(s2)', env)}")
    env = {"s1": set(s1), "s2": s2}
    exec("s1.update(s2)", env)
    print(f"   s1.update(s2)          -> s1 is now {show(env['s1'])}")
    env = {"s1": set(s1), "s2": s2}
    exec("s1.add(frozenset(s2))", env)
    print(f"   s1.add(frozenset(s2))  -> {len(env['s1'])} members: 3 letters and 1 frozenset")
    print("   add() puts in ONE member; update() puts in every member of an iterable.")
    print("   A set can hold a frozenset, never a set: a set can change, so its")
    print("   hash could change after it was filed, and it would be lost.")
    print()

    print("3. OPERATOR OR METHOD: THE SAME ANSWER, DIFFERENT MANNERS")
    a, b = {1, 2, 3, 4}, {3, 4, 5}
    print(f"   a = {show(a)}   b = {show(b)}")
    rows = [
        ("union", "a | b", "a.union(b)"),
        ("intersection", "a & b", "a.intersection(b)"),
        ("difference", "a - b", "a.difference(b)"),
        ("symmetric difference", "a ^ b", "a.symmetric_difference(b)"),
        ("subset", "a <= b", "a.issubset(b)"),
        ("superset", "a >= b", "a.issuperset(b)"),
        ("proper subset", "a < b", "(none)"),
        ("disjoint", "(none)", "a.isdisjoint(b)"),
        ("membership", "3 in a", "a.__contains__(3)"),
    ]
    env = {"a": a, "b": b}
    print(f"   {'operation':<21} {'operator':<9} {'method':<26} result")
    for name, op, method in rows:
        code = op if op != "(none)" else method
        result = attempt(code, env).replace("set ", "")
        if op != "(none)" and method != "(none)":
            assert eval(op, env) == eval(method, env)
        print(f"   {name:<21} {op:<9} {method:<26} {result}")
    print("   Every row with both forms gives the same result for two sets.")
    engineers = {"bob", "sue", "ann", "vic"}
    managers = {"tom", "sue"}
    print(f"   In words, with engineers = {show(engineers)}, managers = {show(managers)}:")
    for code, words in [
        ("'bob' in engineers", "is bob an engineer?"),
        ("engineers & managers", "who is both?"),
        ("engineers | managers", "who is either?"),
        ("engineers - managers", "engineers who are not managers"),
        ("managers - engineers", "managers who are not engineers"),
        ("engineers >= managers", "is every manager an engineer?"),
        ("{'bob', 'sue'} < engineers", "are both engineers, and not all of them?"),
        ("engineers ^ managers", "who is in exactly one of the two?"),
        ("(engineers | managers) - (engineers ^ managers)", "either, minus exactly one: both"),
    ]:
        r = attempt(code, {"engineers": engineers, "managers": managers}).replace("set ", "")
        print(f"     {code:<48} {r:<36} {words}")
    print("   The difference is what they accept. A tuple on the right:")
    env = {"a": a, "t": (3, 4, 5)}
    for code in ["a | t", "a.union(t)", "a <= t", "a.issubset(t)", "a.union([9], 'x', range(2))"]:
        print(f"     {code:<28} -> {attempt(code, env)}")
    print("   Operators need a set (or frozenset) on both sides; methods take any")
    print("   iterable, and several of them at once.")
    print()

    print("4. CLAIMS FROM THE NOTES, CHECKED")
    x1 = {"a", "b", "c"}
    claims = [
        ("'in' works but .__contains__() cannot be used",
         f"x1.__contains__('a') = {x1.__contains__('a')}: it is what 'in' calls. False."),
        ("'-' has no corresponding method",
         f"x1.difference({{'a'}}) = {show(x1.difference({'a'}))}. False."),
        ("issubset and issuperset have no operator (N/A)",
         f"<= and >= are those operators; {{'a'}} <= x1 is {({'a'} <= x1)}. False."),
        ("isdisjoint has no operator",
         f"True; the nearest is 'not (a & b)', which builds a set first."),
        ("the + operator is not supported for sets",
         f"{attempt('x1 + x1', {'x1': x1})}. True; use |."),
        ("s1.add(s2) fails, use update()",
         "True, section 2: a set is unhashable."),
        ("an empty set is falsy",
         f"bool(set()) = {bool(set())}. True."),
        ("issubset() of an empty iterable returns False",
         f"set().issubset([]) = {set().issubset([])}; only a non-empty set gives False. False."),
        ("{0,1,2,3,4} & {0,2,3,4} & {0,2,5}: the only common element is {2}",
         f"it is {show({0, 1, 2, 3, 4} & {0, 2, 3, 4} & {0, 2, 5})}; 0 is in all three. False."),
        ("union takes several sets at once, and so does symmetric_difference",
         f"a.union(b, c) works; {attempt('a.symmetric_difference(b, c)', {'a': {1}, 'b': {2}, 'c': {3}})}."
         " Half true."),
    ]
    for claim, verdict in claims:
        print(f"   claim:  {claim}")
        print(f"           {verdict}")
    print()

    print("5. CHAINING: LEFT TO RIGHT, AND WHAT ^ OF THREE MEANS")
    s1, s2, s3 = {0, 1, 2, 3, 4}, {2, 3, 4}, {2, 5}
    print(f"   s1 = {show(s1)}   s2 = {show(s2)}   s3 = {show(s3)}")
    print(f"   s1 | s2 | s3 = {show(s1 | s2 | s3)}")
    print(f"   s1 & s2 & s3 = {show(s1 & s2 & s3)}")
    print(f"   s1 ^ s2      = {show(s1 ^ s2)}")
    print(f"   s1 ^ s2 ^ s3 = {show(s1 ^ s2 ^ s3)}   = (s1 ^ s2) ^ s3 = {show(s1 ^ s2)} ^ {show(s3)}")
    counts = {x: sum(x in s for s in (s1, s2, s3)) for x in s1 | s2 | s3}
    print("   in how many of the three sets each element is:")
    print("     " + "  ".join(f"{x}:{counts[x]}" for x in sorted(counts)))
    odd = {x for x, c in counts.items() if c % 2 == 1}
    print(f"   elements in an odd number of them:  {show(odd)}   same set: {odd == s1 ^ s2 ^ s3}")
    print("   So ^ over many sets keeps what appears an odd number of times,")
    print("   not 'what is in exactly one'. 2 is in all three and survives.")
    print(f"   s1 - s2 - s3 = {show(s1 - s2 - s3)}  = (s1 - s2) - s3;"
          f"  s1 - (s2 - s3) = {show(s1 - (s2 - s3))}")
    print("   | & ^ are associative, so grouping never matters for them; - is not.")
    s4 = s2 | s1 | s3
    s4 |= {11, 22}
    print(f"   s4 = s2 | s1 | s3;  s4 |= {{11, 22}}  ->  {show(s4)}")
    print("   Every operator has an in-place form: |= &= -= ^= change the left set.")
    print()

    print("6. EQUALITY: == ASKS ABOUT MEMBERS, AND NOTHING ELSE DOES")
    p = {1, 9}
    q = {9, 1}
    print(f"   p = {{1, 9}}   q = {{9, 1}}   list(p) = {list(p)}   list(q) = {list(q)}")
    print(f"   p == q                          {p == q}      the right test")
    print(f"   list(p) == list(q)              {list(p) == list(q)}"
          "     order of iteration is not membership")
    small, big = {1}, {1, 2}
    print(f"   {{1}}.difference({{1, 2}}) == set() {small.difference(big) == set()}"
          "      only says {1} <= {1, 2}")
    print(f"   {{1}} == {{1, 2}}                  {small == big}")
    print(f"   not (p ^ q)                     {not (p ^ q)}      also right: no member on one side only")
    print("   Equality of sets is extensionality run as code: same members, equal.")
    print("   Iteration order depends on how the set was built, so comparing lists")
    print("   of two equal sets can say False; a one-sided difference checks only <=.")
    print()

    print("7. FROZENSET: THE SET THAT CANNOT CHANGE, SO IT CAN BE A MEMBER")
    fs = frozenset([1, 2])
    print(f"   fs.add(3)          -> {attempt('fs.add(3)', {'fs': fs})}")
    print(f"   fs.union([3, 4])   -> {attempt('fs.union([3, 4])', {'fs': fs})}   a new one; fs is unchanged")
    print(f"   {{1}} | frozenset({{2}}) -> {type({1} | frozenset({2})).__name__};"
          f"   frozenset({{2}}) | {{1}} -> {type(frozenset({2}) | {1}).__name__}"
          "   the left operand decides")
    print(f"   frozenset({{1, 2}}) == {{1, 2}}  {frozenset({1, 2}) == {1, 2}}"
          "   equality is still only about members")
    print()

    print("8. SUBSET, PROPER SUBSET, DISJOINT, EMPTY")
    s = {1, 2}
    for code in ["s <= {1, 2}", "s < {1, 2}", "s < {1, 2, 3}", "set() <= s", "set() < set()",
                 "s.isdisjoint({3, 4})", "s.isdisjoint({2, 3})", "set().isdisjoint(set())"]:
        print(f"   {code:<26} {attempt(code, {'s': s})}")
    print("   Every set is a subset of itself, but not a proper one. The empty set")
    print("   is a subset of every set, and disjoint from every set, itself included.")
    t, u = {1, 2, 3}, {5}
    print(f"   if (s <= t, u):   runs, because (s <= t, u) = ({s <= t}, {u}) is a non-empty tuple")
    print(f"   s <= t and s <= u = {s <= t and s <= u}   is what was meant")
    n1, n2, n3 = {0, 1, 2, 3, 4}, {0, 2, 3, 4}, {0, 2, 5}
    print(f"   the notes' version: s1 = {show(n1)}, s2 = {show(n2)}, s3 = {show(n3)}")
    print(f"     if (s1 <= s2, s3):          always taken, tuple ({n1 <= n2}, {show(n3)})")
    print(f"     s1 <= s2 and s1 <= s3       {n1 <= n2 and n1 <= n3}   1 is in s1 and in neither of the others")
    try:
        compile("s2 < = s1", "<notes>", "eval")
        spaced = "accepted"
    except SyntaxError:
        spaced = "SyntaxError"
    print(f"     s2 < = s1                   {spaced}   <= is one token, no space inside")
    print()

    print("9. REMOVING: WHICH ONES RAISE")
    for code in ["s.remove(9)", "s.discard(9)", "set().pop()"]:
        print(f"   {code:<16} -> {attempt(code, {'s': {1, 2}})}")
    print("   remove() insists the member is there; discard() does not care.")
    print("   pop() takes an arbitrary member: a set has no 'first' to take.")
    print()

    print("10. ORDER IS NOT PART OF A SET")
    L = [1, 2, 1, 3, 2, 4, 5]
    print(f"   list(set({L})) = {list(set(L))}   looks sorted, by luck:")
    print(f"   list(set([10, 3, 8]))      = {list(set([10, 3, 8]))}"
          "   small ints land in slot n % table size")
    words = ["pear", "fig", "apple", "fig", "pear", "kiwi"]
    print(f"   words              = {words}")
    print(f"   sorted(set(words)) = {sorted(set(words))}   a list: sets cannot be sorted")
    print(f"   list(dict.fromkeys(words)) = {list(dict.fromkeys(words))}")
    print("   To drop duplicates AND keep first-seen order, use a dict: its keys")
    print("   are a set that remembers insertion order. list(set(words)) comes back")
    print("   in hash order, which for strings changes from one run to the next.")
    mixed = {3, 1, "apple", "orange", 5, "banana"}
    err = attempt('sorted(m)', {'m': mixed}).split(":")[0]
    print(f"   sorted({{3, 1, 'apple', ...}})  -> {err}: Python 3 will not order an int against a str")
    print(f"   key=lambda x: (isinstance(x, str), x)  -> {sorted(mixed, key=lambda x: (isinstance(x, str), x))}")
    print("   numbers first, since False < True, and no int is compared with a str.")
    print()

    print("11. WHAT SETS ARE FOR: MEMBERSHIP, DEDUPLICATION, VISITED NODES")
    graph = {"A": ["B", "C"], "B": ["D"], "C": ["D", "A"], "D": ["B", "E"], "E": []}
    visited, order, queue = {"A"}, [], deque(["A"])
    while queue:
        node = queue.popleft()
        order.append(node)
        for nxt in graph[node]:
            if nxt not in visited:
                visited.add(nxt)
                queue.append(nxt)
    print(f"   graph with cycles A->C->A and B->D->B:  {graph}")
    print(f"   breadth-first from A, skipping nodes already in 'visited': {' -> '.join(order)}")
    print("   Without the set the walk loops forever. With a list, each 'in' test")
    print("   scans the list; with a set it is one hash lookup, whatever the size.")
    customers = {"C001", "C002", "C003", "C004"}
    with_invoices = {"C001", "C002", "C004", "C009"}
    print(f"   customers = {show(customers)}   invoiced = {show(with_invoices)}")
    print(f"   inner join keys     customers & invoiced = {show(customers & with_invoices)}")
    print(f"   outer join keys     customers | invoiced = {show(customers | with_invoices)}")
    print(f"   left anti-join      customers - invoiced = {show(customers - with_invoices)}"
          "   never invoiced")
    print(f"   orphans             invoiced - customers = {show(with_invoices - customers)}"
          "   no such customer")
    print(f"   mismatches          customers ^ invoiced = {show(customers ^ with_invoices)}")
    print("   The keys a join keeps are a set operation on the two key columns;")
    print("   pandas' merge(how='inner'/'outer'/'left') is the same algebra with rows attached.")

    print()

    print("12. DICT VIEWS: A DICT'S KEYS ARE ALREADY A SET")
    stock = {"apple": 3, "fig": 0, "kiwi": 5}
    order = {"fig": 2, "kiwi": 1, "plum": 4}
    print(f"   stock = {stock}")
    print(f"   order = {order}")
    both = stock.keys() & order.keys()
    print(f"   stock.keys() & order.keys() = {show(both)}   type: {type(both).__name__}")
    print(f"   order.keys() - stock.keys() = {show(order.keys() - stock.keys())}   ordered but never stocked")
    print(f"   stock.keys() | ['pear']      = {show(stock.keys() | ['pear'])}   a keys view takes any iterable")
    print(f"   stock.keys() <= set(stock)   = {stock.keys() <= set(stock)}")
    shared = dict(stock.items() & {"fig": 0, "kiwi": 9}.items())
    print(f"   stock.items() & {{'fig': 0, 'kiwi': 9}}.items() = {shared}   same key AND same value")
    print(f"   stock.values() & {{0}}        -> {attempt('v & {0}', {'v': stock.values()})}")
    print("   values can repeat and need not be hashable, so their view is not a set.")
    s = {1, 2}
    s.update({1: "a", 5: "e"})
    print(f"   {{1, 2}}.update({{1: 'a', 5: 'e'}}) -> {show(s)}   iterating a dict yields its keys")
    print(f"   set({{'x': 1, 'y': 2}}) = {show(set({'x': 1, 'y': 2}))}")

    print()

    print("13. A MULTISET IS A Counter, AND ITS SYMMETRIC DIFFERENCE COUNTS COPIES")
    from collections import Counter
    l1 = ["a", "a", "b", "c", "d"]
    l2 = ["a", "b", "c", "f"]
    c1, c2 = Counter(l1), Counter(l2)
    print(f"   l1 = {l1}   l2 = {l2}")
    print(f"   set(l1) ^ set(l2)                   = {show(set(l1) ^ set(l2))}"
          "   copies dropped first, so 'a' is in both")
    print(f"   c1 - c2 = {dict(sorted((c1 - c2).items()))}   c2 - c1 = {dict(sorted((c2 - c1).items()))}")
    multi = sorted((c1 - c2 | c2 - c1).elements())
    print(f"   sorted((c1 - c2 | c2 - c1).elements()) = {multi}")
    print("   l1 has two 'a' and l2 one, so one 'a' is left over: the multiset")
    print("   difference counts copies. '-' binds tighter than '|', so the line")
    print("   is (c1 - c2) | (c2 - c1), and | on Counters keeps the larger count.")
    print(f"   c1 ^ c2  -> {attempt('c1 ^ c2', {'c1': c1, 'c2': c2})}   Counter has no ^; build it from two differences")


if __name__ == "__main__":
    main()
