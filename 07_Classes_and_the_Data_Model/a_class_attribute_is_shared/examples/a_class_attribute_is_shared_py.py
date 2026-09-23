"""A name assigned in a class body is one object, seen through every instance."""

from dataclasses import dataclass, fields

# Every statement below is run through exec() and every expression through
# eval(), so the label printed IS the code that ran. An exception prints its
# type name only: the message is not API.
NS = {"dataclass": dataclass, "fields": fields}


def do(stmt):
    """Run a statement and print it; print the exception type if it raised."""
    try:
        exec(stmt, NS)
        for line in stmt.splitlines():
            print(f"     {line}")
    except Exception as exc:
        first, *rest = stmt.splitlines()
        print(f"     {first:<32} {type(exc).__name__}")
        for line in rest:
            print(f"     {line}")


def ask(expr, note=""):
    """Evaluate an expression and print it beside its value."""
    try:
        val = repr(eval(expr, NS))
    except Exception as exc:
        val = type(exc).__name__
    print(f"     {expr:<32} {val:<18} {note}".rstrip())


print("1. ONE LIST ON THE CLASS, SEEN THROUGH EVERY INSTANCE")
do("class Team:\n    members = []\n    def join(self, name):\n        self.members.append(name)")
do("a, b = Team(), Team()")
do("a.join('ada')")
ask("b.members", "nobody joined b: the list belongs to the class")
ask("a.members is Team.members")
ask("vars(a)", "the instance holds nothing of its own")

print("\n2. A READ FALLS THROUGH TO THE CLASS; A WRITE DOES NOT")
do("class Counter:\n    count = 0")
do("c = Counter()")
ask("c.count", "not on c, so found on the class")
do("c.count = 1")
ask("Counter.count", "the write went to c, not through to the class")
ask("vars(c)")
ask("c.count", "and now the read stops at c")
do("del c.count")
ask("c.count", "delete c's own, and the class's shows again")
do("c.count += 1")
ask("(Counter.count, vars(c))", "+= reads through, then writes to c")

print("\n3. THE FIX: MAKE THE OBJECT IN __init__")
do("class Team:\n    def __init__(self):\n        self.members = []\n    def join(self, name):\n        self.members.append(name)")
do("a, b = Team(), Team()")
do("a.join('ada')")
ask("b.members", "each __init__ ran self.members = [] once, for its own instance")
ask("a.members is b.members")

print("\n4. WHEN SHARING IS THE POINT")
do("class Node:\n    made = 0\n    def __init__(self):\n        Node.made += 1")
do("for _ in range(3): Node()")
ask("Node.made", "written through the class name, so it is one counter")
ask("vars(Node())", "and no instance ever gets its own copy")

print("\n5. A DATACLASS FIELD IS PER INSTANCE; AN UNANNOTATED NAME IS NOT")
do("@dataclass\nclass Bag:\n    items: list = []")
do("@dataclass\nclass Bag:\n    items = []")
do("x, y = Bag(), Bag()")
do("x.items.append(1)")
ask("y.items", "no annotation, so not a field: a plain class attribute")
ask("fields(Bag)", "the dataclass machinery never saw it")

print("\n6. __slots__: A NAMESPACE THAT IS NOT A DICT")
do("class P:\n    __slots__ = ('x',)")
do("p = P()")
do("p.x = 1")
do("p.y = 2")
ask("vars(p)", "no __dict__ to hold a stray attribute")
do("class Q:\n    __slots__ = ('x',)\n    x = 0")
