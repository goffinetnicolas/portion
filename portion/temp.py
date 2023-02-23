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


if __name__ == "__main__":

    '''
    a = intervaltree.Node(p.closed(10, 11), "a")
    b = intervaltree.Node(p.closed(9, 10), "b")
    c = intervaltree.Node(p.closed(4, 8), "c")
    print(a.interval - b.interval)
    '''

    tree = intervaltree.IntervalTree()

    a = intervaltree.Node(p.closed(16, 21), 'a')
    b = intervaltree.Node(p.closed(9, 10), 'b')
    c = intervaltree.Node(p.closed(28, 29), 'c')
    d = intervaltree.Node(p.closedopen(4, 5), 'd')
    e = intervaltree.Node(p.singleton(15), 'e')
    f = intervaltree.Node(p.openclosed(21, 23), 'f')
    g = intervaltree.Node(p.closedopen(30, 32), 'g')
    h = intervaltree.Node(p.singleton(24), 'h')
    i = intervaltree.Node(p.singleton(40), 'i')

    tree.insert(a)
    tree.insert(b)
    tree.insert(c)
    tree.insert(d)
    tree.insert(e)
    tree.insert(f)
    tree.insert(g)
    tree.insert(h)
    tree.insert(i)

    print(tree)

    tree.delete(f)
    tree.delete(h)
    tree.delete(g)

    print(tree)