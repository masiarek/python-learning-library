# Mutating what you iterate

**Level:** 201 · for Python programmers

> **Stub — an outline, not a lesson.** There is no runnable example behind this page yet, so nothing on it has been through [the check that backs every other claim in this library](../../CONTRIBUTING.md). The bullets below are the questions the finished page has to answer.

**One line:** Removing from a list while looping over it skips the element after each removal and raises nothing, while adding a key to a dict or a set during iteration raises `RuntimeError` at the next step — two different failures for one mistake, and the fix for both is to loop over a copy or build a new collection.

## What the finished page has to answer

- The list case, measured: `for x in lst: if cond(x): lst.remove(x)` leaves every other match in place, because the list iterator is an index and the removal shifted the next element into the slot it just read.
- Appending while iterating a list, and why the loop can run forever; a bounded version for the page.
- The dict and set case: `RuntimeError` on the next `next()`, named by type, and the rule that changing a dict's *values* during iteration is allowed while adding or removing *keys* is not.
- The fixes: `for k in list(d)`, a comprehension that builds the new collection, `lst[:] = […]` when other names hold the list, which is [Assignment does not copy](../../04_Names_and_Objects/assignment_does_not_copy/README.md) applied on purpose.
- What a dict looks like after a delete and a re-insert: insertion order puts the key at the end.

## See also

- [An iterator is used up](../an_iterator_is_used_up/README.md): the list iterator as a position
- [Assignment does not copy](../../04_Names_and_Objects/assignment_does_not_copy/README.md): why `lst = […]` inside the loop does not help the other names
- [The `for` statement ↗](https://docs.python.org/3/reference/compound_stmts.html#the-for-statement) in the language reference, which has a note about exactly this, and [dictionary view objects ↗](https://docs.python.org/3/library/stdtypes.html#dictionary-view-objects)
