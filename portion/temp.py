import portion as P
import random as r
import timeit as t

def generate_interval(length):
    num = r.randint(0, 4)
    a = r.randint(0, 100)
    b = a + length
    if num == 0:
        return P.open(a, b)
    if num == 1:
        return P.closed(a, b)
    if num == 2:
        return P.openclosed(a, b)
    if num == 3:
        return P.closedopen(a, b)
    if num == 4:
        return P.singleton(a)

def generate_singletons():
    return P.singleton(r.randint(0, 10000))

def test_insert_correct():
    tree = P.IntervalTree()
    values = ["a", "b", "c"]
    l=[]
    for i in range(10000):
        s = generate_singletons()
        if s not in l:
            l.append(s)
    for s in l:
        node = P.Node(s, r.choice(values))
        tree.insert(node)
        print("inserting : ", node)
        print(tree)
        if check_size(tree) == False:
            print("size not correct")
            return False

def test_delete_correct():
    tree = P.IntervalTree()
    values = ["a", "b", "c"]
    l=[]
    nodes = []
    for i in range(1000):
        s = generate_singletons()
        if s not in l:
            l.append(s)
    for s in l:
        node = P.Node(s, r.choice(values))
        nodes.append(node)
        tree.insert(node)
    while len(nodes) != 0:
        n = r.choice(nodes)
        print(tree)
        print("deleting : ", n)
        tree.delete(n)
        print(tree)
        nodes.remove(n)
        if not tree.root.is_nil():
            if check_size(tree) == False:
                print("size not correct")
                return False

def test_insert_interval_correct():
    tree = P.IntervalTree()
    values = ["a", "b", "c"]
    for i in range(5000):
        s = generate_interval(10)
        node = P.Node(s, r.choice(values))
        tree.insert(node)
        print("inserting : ", node)
        print(tree)

def test_delete_interval_correct():
    tree = P.IntervalTree()
    values = ["a", "b", "c"]
    nodes=[]
    for i in range(5000):
        s = generate_interval(10)
        node = P.Node(s, r.choice(values))
        nodes.append(node)
        tree.insert(node)
    while len(nodes) != 0:
        n = r.choice(nodes)
        print(tree)
        print("deleting : ", n)
        tree.delete(n)
        nodes.remove(n)


def test():
    print(t.timeit(""))

def check_size(tree):
    current = tree.minimum(tree.root)
    while not current.is_nil():
        if current.size != current.left.size + current.right.size + 1:
            return False
        current = tree.successor(current)
    return True

def create_simple_tree():
    tree = P.IntervalTree()
    a = P.Node(P.closed(16, 21), 'a')
    b = P.Node(P.closed(9, 10), 'b')
    c = P.Node(P.closed(28, 29), 'c')
    d = P.Node(P.closed(4, 5), 'd')
    e = P.Node(P.singleton(15), 'e')
    f = P.Node(P.openclosed(21, 23), 'f')
    g = P.Node(P.closedopen(30, 32), 'g')
    h = P.Node(P.singleton(24), 'h')
    i = P.Node(P.singleton(40), 'i')

    tree.insert(a)
    tree.insert(b)
    tree.insert(c)
    tree.insert(d)
    tree.insert(e)
    tree.insert(f)
    tree.insert(g)
    tree.insert(h)
    tree.insert(i)

    return tree


if __name__ == "__main__":
    test_delete_correct()
    # x = P.intervaltree.Node(P.closed(42, 48), "a")
    # r = P.intervaltree.Node(P.closed(40, 50), "b")
    # print(x.interval <= r.interval)
    # print(x.interval in r.interval


