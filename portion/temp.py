import portion as p
import intervaltree
import random as r


def generate(length):
    num = r.randint(0, 4)
    a = r.randint(-2147483648, 2147483647)
    b = a + length
    if num == 0:
        return intervaltree.Node(p.open(a, b))
    if num == 1:
        return intervaltree.Node(p.closed(a, b))
    if num == 2:
        return intervaltree.Node(p.openclosed(a, b))
    if num == 3:
        return intervaltree.Node(p.closedopen(a, b))
    if num == 4:
        return intervaltree.Node(p.singleton(a))


a = intervaltree.Node(p.closed(10, 11), "a")
b = intervaltree.Node(p.closed(9, 10), "b")
c = intervaltree.Node(p.closed(4, 8), "c")
print(a.interval - b.interval)
