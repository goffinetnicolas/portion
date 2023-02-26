import portion as p
import intervaltree
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
    tree = intervaltree.IntervalTree()
    for k,v in d:
        tree.insertInterval(intervaltree.Node(k,v))
    return tree

def dict_interval_list_test_insert(l):
    return p.IntervalDict(l)

def test():
    print(t.timeit(""))


if __name__ == "__main__":

    '''
    a = intervaltree.Node(p.closed(10, 11), "a")
    b = intervaltree.Node(p.closed(9, 10), "b")
    c = intervaltree.Node(p.closed(4, 8), "c")
    print(a.interval - b.interval)
    

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

    tree.root.left=tree.nil
    tree.left_rotate(tree.root)
    tree.rb_delete_fixup(tree.root.right)
    print(tree)
    '''
