import portion as P
import random as r
import timeit as t

def generate(length):
    num = r.randint(0, 4)
    a = r.randint(-2147483648, 2147483647)
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


def test_insert_correct(self):
    tree = P.IntervalTree()
    values = ["a", "b", "c"]
    for i in range(1000):
        node = P.Node(self.generate(10000000), r.choice(values))
        tree.insert_interval(node)
        print("inserting : ", node)
        assert tree.check_interval_tree() == True
    print(tree)

def test():
    print(t.timeit(""))


if __name__ == "__main__":

    x = P.intervaltree.Node(P.closed(42, 48), "a")
    r = P.intervaltree.Node(P.closed(40, 50), "b")
    print(x.interval <= r.interval)
    print(x.interval in r.interval)



