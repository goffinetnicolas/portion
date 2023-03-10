import portion as p
import random as r
import timeit as t

def generate(length):
    num = r.randint(0, 4)
    a = r.randint(-2147483648, 2147483647)
    b = a + length
    if num == 0:
        return p.open(a, b)
    if num == 1:
        return p.closed(a, b)
    if num == 2:
        return p.openclosed(a, b)
    if num == 3:
        return p.closedopen(a, b)
    if num == 4:
        return p.singleton(a)

def dic_interval_tree_test_insert(d):
    tree = p.IntervalTree()
    for k,v in d:
        tree.insertInterval(p.Node(k,v))
    return tree

def dict_interval_list_test_insert(l):
    return p.IntervalDict(l)

def test():
    print(t.timeit(""))


if __name__ == "__main__":

    '''
    x = intervaltree.Node(p.closed(42, 48), "a")
    r = intervaltree.Node(p.closed(40, 50), "b")
    print(x.interval <= r.interval)
    print(x.interval in r.interval)
    '''
    

    tree = p.IntervalTree()

    a = p.Node(p.closed(16, 21), 'a')
    b = p.Node(p.closed(9, 10), 'b')
    c = p.Node(p.closed(28, 29), 'c')
    d = p.Node(p.closed(4, 5), 'd')
    e = p.Node(p.singleton(15), 'e')
    f = p.Node(p.openclosed(21, 23), 'f')
    g = p.Node(p.closedopen(30, 32), 'g')
    h = p.Node(p.singleton(24), 'h')
    i = p.Node(p.singleton(40), 'i')

    tree.insertInterval(a)
    tree.insertInterval(b)
    tree.insertInterval(c)
    tree.insertInterval(d)
    tree.insertInterval(e)
    tree.insertInterval(f)
    tree.insertInterval(g)
    tree.insertInterval(h)
    tree.insertInterval(i)

    #print(tree)

    tree.insertInterval(p.Node(p.closed(0,30), 'g'))

    print(tree)



