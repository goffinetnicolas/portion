import pytest
import portion as P


class TestIntervalTree:

    def check_nil_color(self, tree):
        """
        Check if the tree is well-structured with respect to the nil node (must always be black)
        """

        current = tree.minimum(tree.root)
        while not current.is_nil():
            if current.left.is_nil():
                if current.left.color == True:
                    return False
            if current.right.is_nil():
                if current.right.color == True:
                    return False
            current = tree.successor(current)
        return True

    def check_red_colors(self, tree):
        """
        Check if the tree is well-structured with respect to the red nodes
        If a node is red, then both its children are black
        """

        current = tree.minimum(tree.root)
        while not current.is_nil():
            if current.color == True:
                if current.left.color == True or current.right.color == True:
                    return False
            current = tree.successor(current)
        return True

    def check_each_nodes_black_colors(self, tree):
        """
        Check if the tree is well-structured with respect to the black nodes
        For each node, all simple paths from the node to descendant leaves contain the same number of black nodes
        """

        current = tree.minimum(tree.root)
        while not current.is_nil():
            if not self.check_black_colors(current, tree):
                return False
            current = tree.successor(current)
        return True

    def create_path(self, x, p, tree):
        """
        Used to verify if all the paths have the same number of black nodes
        """
        path = [tree.nil]
        while x != p.p:
            path.append(x)
            x = x.p
        return path

    def check_black_colors(self, x, tree):
        """
        Check for a single node if all simple paths from the node
        to descendant leaves contain the same number of black nodes
        """

        current = tree.minimum(x)
        paths = []
        while current != tree.successor(tree.maximum(x)):
            if current.left.is_nil():
                path = self.create_path(current, x, tree)
                paths.append(path)
            if current.right.is_nil():
                path = self.create_path(current, x, tree)
                paths.append(path)
            current = tree.successor(current)
        num_black1 = 0
        for node in paths[0]:
            if node.color == False:
                num_black1 += 1
        for path in paths:
            num_black2 = 0
            for node in path:
                if node.color == False:
                    num_black2 += 1
            if num_black1 != num_black2:
                return False
        return True

    def check_rb_tree(self, tree):
        """
        Check if the tree respect the red black tree properties
        """

        if tree.root.is_nil():
            return True

        # The root is black.
        a = tree.root.color == False

        # Every leaf (NIL) is black.
        b = self.check_nil_color(tree)

        # If a node is red, then both its children are black.
        c = self.check_red_colors(tree)

        # For each node, all simple paths from the node to descendant leaves contain the same number of black nodes.
        d = self.check_each_nodes_black_colors(tree)

        return a and b and c and d

    def check_interval_tree(self, tree):
        """
        Check if the tree respect the interval tree properties (no overlapping intervals)
        """

        if tree.root.is_nil():
            return True

        visited = []
        current = tree.minimum(tree.root)
        while not current.is_nil():
            for v in visited:
                if v.interval.overlaps(current.interval):
                    return False
            visited.append(current)
            current = tree.successor(current)
        return self.check_rb_tree(tree)

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

        assert self.check_interval_tree(tree) == True
        assert tree.root == P.Node(P.closed(16, 21), 'a')
        assert self.check_interval_tree(tree) == True
        assert tree.root.left == P.Node(P.closed(9, 10), 'b')
        assert self.check_interval_tree(tree) == True
        assert tree.root.right == P.Node(P.closed(28, 29), 'c')
        assert self.check_interval_tree(tree) == True
        assert tree.root.left.left == P.Node(P.closed(4, 5), 'd')
        assert self.check_interval_tree(tree) == True
        assert tree.root.left.right == P.Node(P.singleton(15), 'e')
        assert self.check_interval_tree(tree) == True
        assert tree.root.right.left == P.Node(P.openclosed(21, 23), 'f')
        assert self.check_interval_tree(tree) == True
        assert tree.root.right.right == P.Node(P.closedopen(30, 32), 'g')
        assert self.check_interval_tree(tree) == True
        assert tree.root.right.left.right == P.Node(P.singleton(24), 'h')
        assert self.check_interval_tree(tree) == True
        assert tree.root.right.right.right == P.Node(P.singleton(40), 'i')
        assert self.check_interval_tree(tree) == True

    def test_delete_case1(self):
        tree = self.create_simple_tree()

        tree.delete(tree.root.right.left)
        assert self.check_interval_tree(tree) == True
        assert tree.root.right.left == P.Node(P.singleton(24), 'h')

    def test_delete_case2(self):
        tree = self.create_simple_tree()
        tree.insert(P.Node(P.singleton(12), 'j'))

        tree.delete(tree.root.left.right)
        assert self.check_interval_tree(tree) == True
        assert tree.root.left.right == P.Node(P.singleton(12), 'j')

    def test_delete_case3(self):
        tree = self.create_simple_tree()

        tree.delete(tree.root)
        assert self.check_interval_tree(tree) == True
        assert tree.root == P.Node(P.openclosed(21, 23), 'f')

    def test_insert_interval_case1(self):
        tree = self.create_simple_tree()
        tree.insert_interval(P.Node(P.singleton(24), 'j'))
        assert tree.root.right.left.right == P.Node(P.singleton(24), 'j')
        assert self.check_interval_tree(tree) == True

    def test_insert_interval_case2(self):
        tree = self.create_simple_tree()
        tree.insert_interval(P.Node(P.closed(18, 20), 'a'))
        assert tree.root == P.Node(P.closed(18, 20), 'a')
        assert self.check_interval_tree(tree) == True

    def test_insert_interval_case3(self):
        tree = self.create_simple_tree()
        tree.insert_interval(P.Node(P.closed(18, 20), 'j'))
        assert tree.root == P.Node(P.closed(18, 20), 'j')
        assert tree.root.left.right.right == P.Node(P.closedopen(16, 18), 'a')
        assert tree.root.right.left.left == P.Node(P.openclosed(20, 21), 'a')
        assert self.check_interval_tree(tree) == True

    def test_insert_interval_case4(self):
        # probably more case to test for case 4
        tree = self.create_simple_tree()
        tree.insert_interval(P.Node(P.closed(22, 30), 'g'))
        assert tree.root.right == P.Node(P.closedopen(22, 32), 'g')
        assert tree.root.right.left == P.Node(P.open(21, 22), 'f')
        assert tree.root.right.left.right == tree.nil
        assert tree.root.right.right == P.Node(P.singleton(40), 'i')
        assert self.check_interval_tree(tree) == True

    def test_insert_interval_case5and6(self):
        tree = self.create_simple_tree()
        tree.insert_interval(P.Node(P.closed(29, 32), 'g'))
        assert tree.root.right == P.Node(P.closedopen(28, 29), 'c')
        assert tree.root.right.right == P.Node(P.closed(29, 32), 'g')
        assert tree.root.right.right.right == P.Node(P.singleton(40), 'i')
        assert self.check_interval_tree(tree) == True

    def test_left_rotate(self):
        tree = P.IntervalTree()
        tree.insertNode(P.closed(16, 21), 'a')
        tree.insertNode(P.closed(9, 10), 'b')
        tree.insertNode(P.closed(4, 5), 'd')
        tree.insertNode(P.singleton(15), 'e')
        tree.insertNode(P.openclosed(21, 23), 'f')
        print(tree)