import pytest
import portion as P


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
        assert tree.root.left == P.Node(P.closed(9, 10), 'b')
        assert tree.root.right == P.Node(P.closed(28, 29), 'c')
        assert tree.root.left.left == P.Node(P.closed(4, 5), 'd')
        assert tree.root.left.right == P.Node(P.singleton(15), 'e')
        assert tree.root.right.left == P.Node(P.openclosed(21, 23), 'f')
        assert tree.root.right.right == P.Node(P.closedopen(30, 32), 'g')
        assert tree.root.right.left.right == P.Node(P.singleton(24), 'h')
        assert tree.root.right.right.right == P.Node(P.singleton(40), 'i')

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
