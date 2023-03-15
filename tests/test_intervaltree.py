import pytest
import portion as P
import random as r

class TestIntervalTree:

    def create_simple_tree(self):
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

    def test_insert(self):
        tree = self.create_simple_tree()

        assert tree.check_interval_tree() == True
        assert tree.root == P.Node(P.closed(16, 21), 'a')
        assert tree.check_interval_tree() == True
        assert tree.root.left == P.Node(P.closed(9, 10), 'b')
        assert tree.check_interval_tree() == True
        assert tree.root.right == P.Node(P.closed(28, 29), 'c')
        assert tree.check_interval_tree() == True
        assert tree.root.left.left == P.Node(P.closed(4, 5), 'd')
        assert tree.check_interval_tree() == True
        assert tree.root.left.right == P.Node(P.singleton(15), 'e')
        assert tree.check_interval_tree() == True
        assert tree.root.right.left == P.Node(P.openclosed(21, 23), 'f')
        assert tree.check_interval_tree() == True
        assert tree.root.right.right == P.Node(P.closedopen(30, 32), 'g')
        assert tree.check_interval_tree() == True
        assert tree.root.right.left.right == P.Node(P.singleton(24), 'h')
        assert tree.check_interval_tree() == True
        assert tree.root.right.right.right == P.Node(P.singleton(40), 'i')
        assert tree.check_interval_tree() == True

    def test_delete(self):
        tree = self.create_simple_tree()

        tree.delete(tree.root)
        assert tree.check_interval_tree() == True
        assert tree.root == P.Node(P.openclosed(21, 23), 'f')

        tree.delete(tree.root.left.left)
        assert tree.check_interval_tree() == True
        assert tree.root.left.left.is_nil()

        tree.delete(tree.root.right.right)
        assert tree.check_interval_tree() == True
        assert tree.root.right.right == P.Node(P.singleton(40), 'i')

    def test_insert_interval_case1(self):
        tree = self.create_simple_tree()
        tree.insert_interval(P.Node(P.singleton(24), 'j'))
        assert tree.root.right.left.right == P.Node(P.singleton(24), 'j')
        assert tree.check_interval_tree() == True

    def test_insert_interval_case2(self):
        tree = self.create_simple_tree()
        tree.insert_interval(P.Node(P.closed(18,20), 'a'))
        assert tree.root == P.Node(P.closed(18,20), 'a')
        assert tree.check_interval_tree() == True

    def test_insert_interval_case3(self):
        tree = self.create_simple_tree()
        tree.insert_interval(P.Node(P.closed(18,20), 'j'))
        assert tree.root == P.Node(P.closed(18,20), 'j')
        assert tree.root.left.right.right == P.Node(P.closedopen(16,18), 'a')
        assert tree.root.right.left.left == P.Node(P.openclosed(20,21), 'a')
        assert tree.check_interval_tree() == True

    def test_insert_interval_case4(self):
        # probably more case to test for case 4
        tree = self.create_simple_tree()
        tree.insert_interval(P.Node(P.closed(22,30),'g'))
        assert tree.root.right == P.Node(P.closedopen(22,32),'g')
        assert tree.root.right.left == P.Node(P.open(21,22),'f')
        assert tree.root.right.left.right == tree.nil
        assert tree.root.right.right == P.Node(P.singleton(40),'i')
        assert tree.check_interval_tree() == True

    def test_insert_interval_case5and6(self):
        tree = self.create_simple_tree()
        tree.insert_interval(P.Node(P.closed(29,32),'g'))
        assert tree.root.right == P.Node(P.closedopen(28,29),'c')
        assert tree.root.right.right == P.Node(P.closed(29,32),'g')
        assert tree.root.right.right.right == P.Node(P.singleton(40),'i')
        assert tree.check_interval_tree() == True

    def generate(self,length):
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
