import pytest
import portion as P


class TestIntervalTree:

    def check_nil_color(self, tree):
        """
        Check if the tree is well-structured with respect to the nil node (must always be black)
        """

        current = tree.root.minimum
        while not current.is_nil:
            if current.left.is_nil:
                if current.left.color == True:
                    return False
            if current.right.is_nil:
                if current.right.color == True:
                    return False
            current = tree.successor(current)
        return True

    def check_red_colors(self, tree):
        """
        Check if the tree is well-structured with respect to the red nodes
        If a node is red, then both its children are black
        """

        current = tree.root.minimum
        while not current.is_nil:
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

        current = tree.root.minimum
        while not current.is_nil:
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

        current = x.minimum
        paths = []
        while current != tree.successor(x.maximum):
            if current.left.is_nil:
                path = self.create_path(current, x, tree)
                paths.append(path)
            if current.right.is_nil:
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

        if tree.root.is_nil:
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

        if tree.root.is_nil:
            return True

        visited = []
        current = tree.root.minimum
        while not current.is_nil:
            for v in visited:
                if v.interval.overlaps(current.interval):
                    return False
            visited.append(current)
            current = tree.successor(current)
        return self.check_rb_tree(tree)

    def check_min_max(self,tree):
        current = tree.root.minimum
        while not current.is_nil:
            if current.maximum != current.maximum:
                print(current)
                return False
            if current.minimum != current.minimum:
                print(current)
                return False
            current = tree.successor(current)
        return True

    def minimum(self,x):
        if x.is_nil:
            raise TypeError("cannot compute minimum of empty tree")
        while not x.left.is_nil:
            x = x.left
        return x

    def maximum(self,x):
        if x.is_nil:
            raise TypeError("cannot compute minimum of empty tree")
        while not x.right.is_nil:
            x = x.right
        return x

    def check_size(self, tree):
        current = tree.root.minimum
        while not current.is_nil:
            if current.size != current.left.size + current.right.size + 1:
                return False
            current = tree.successor(current)
        return True

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

    def create_simple_tree2(self):
        tree = self.create_simple_tree()
        tree.insert_interval(P.Node(P.closed(0, 1), 'j'))
        tree.insert_interval(P.Node(P.closed(2, 3), 'k'))
        tree.insert_interval(P.Node(P.singleton(7), 'l'))
        tree.insert_interval(P.Node(P.closed(12, 13), 'm'))
        tree.insert_interval(P.Node(P.closed(25, 26), 'n'))
        tree.insert_interval(P.Node(P.closed(42, 43), 'o'))
        tree.insert_interval(P.Node(P.closed(44, 45), 'p'))
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

        assert self.check_min_max(tree) == True


    def test_delete_case1(self):
        tree = self.create_simple_tree()

        tree.delete(tree.root.right.left)
        assert self.check_interval_tree(tree) == True
        assert tree.root.right.left == P.Node(P.singleton(24), 'h')
        assert self.check_min_max(tree) == True

    def test_delete_case2(self):
        tree = self.create_simple_tree()
        tree.insert(P.Node(P.singleton(12), 'j'))

        tree.delete(tree.root.left.right)
        assert self.check_interval_tree(tree) == True
        assert tree.root.left.right == P.Node(P.singleton(12), 'j')
        assert self.check_min_max(tree) == True

    def test_delete_case3(self):
        tree = self.create_simple_tree()
        tree.delete(tree.root)
        assert self.check_interval_tree(tree) == True
        assert tree.root == P.Node(P.openclosed(21, 23), 'f')
        assert self.check_min_max(tree) == True


    def test_insert_interval_case2(self):
        tree = self.create_simple_tree()
        tree.root.left.interval = P.closed(8,12)
        tree.insert_interval(P.Node(P.closed(9, 10), 'a'))
        assert tree.root.left == P.Node(P.closed(9, 10), 'a')
        assert self.check_interval_tree(tree) == True
        assert self.check_min_max(tree) == True

    def test_insert_interval_case3(self):
        tree = self.create_simple_tree()
        tree.insert_interval(P.Node(P.closed(18, 20), 'j'))
        assert tree.root == P.Node(P.closed(18, 20), 'j')
        assert tree.root.left.right.right == P.Node(P.closedopen(16, 18), 'a')
        assert tree.root.right.left.left == P.Node(P.openclosed(20, 21), 'a')
        assert self.check_interval_tree(tree) == True
        assert self.check_min_max(tree) == True

    def test_insert_interval_case4_1(self):
        # probably more case to test for case 4
        tree = self.create_simple_tree()
        tree.insert_interval(P.Node(P.closed(22, 30), 'g'))
        assert tree.root.right == P.Node(P.closedopen(22, 32), 'g')
        assert tree.root.right.left == P.Node(P.open(21, 22), 'f')
        assert tree.root.right.left.right == tree.nil
        assert tree.root.right.right == P.Node(P.singleton(40), 'i')
        assert self.check_interval_tree(tree) == True
        assert self.check_min_max(tree) == True

    def test_insert_interval_case4_2(self):
        tree = self.create_simple_tree()
        tree.insert_interval(P.Node(P.closed(16, 44), 'j'))
        assert tree.root.right.left == P.Node(P.singleton(15), 'e')
        assert tree.root == P.Node(P.closed(9, 10), 'b')
        assert tree.root.left == P.Node(P.closed(4, 5), 'd')
        assert tree.root.right == P.Node(P.closed(16, 44), 'j')
        assert self.check_interval_tree(tree) == True
        assert self.check_min_max(tree) == True

    def test_insert_interval_case4_3(self):
        tree = self.create_simple_tree2()
        tree.insert_interval(P.Node(P.closed(7, 30), 'g'))
        assert tree.root == P.Node(P.closed(4, 5), 'd')
        assert tree.root.left == P.Node(P.closed(2, 3), 'k')
        assert tree.root.left.left == P.Node(P.closed(0, 1), 'j')
        assert tree.root.right == P.Node(P.singleton(40), 'i')
        assert tree.root.right.left == P.Node(P.closedopen(7, 32), 'g')
        assert tree.root.right.right == P.Node(P.closed(42, 43), 'o')
        assert tree.root.right.right.right == P.Node(P.closed(44, 45), 'p')
        assert self.check_interval_tree(tree) == True
        assert self.check_min_max(tree) == True

    def test_insert_interval_case4_4(self):
        tree = self.create_simple_tree2()
        tree.insert_interval(P.Node(P.closed(15, 24), 'z'))
        assert tree.root == P.Node(P.closed(15, 24), 'z')
        assert tree.root.left == P.Node(P.closed(9, 10), 'b')
        assert tree.root.right == P.Node(P.closed(28, 29), 'c')
        assert self.check_interval_tree(tree) == True
        assert self.check_min_max(tree) == True

    def test_insert_interval_case4_5(self):
        tree = self.create_simple_tree2()
        tree.delete(tree.root.left)
        tree.delete(tree.root.left)
        tree.delete(tree.root.left)
        tree.delete(tree.root.left)
        tree.insert_interval(P.Node(P.closed(21, 45), 'z'))
        assert self.check_interval_tree(tree) == True
        assert self.check_min_max(tree) == True

    def test_insert_interval_case4_6(self):
        tree = self.create_simple_tree2()
        tree.delete(tree.root.right)
        tree.delete(tree.root.right)
        tree.delete(tree.root.right)
        tree.delete(tree.root.right)
        tree.delete(tree.root.right)
        tree.insert_interval(P.Node(P.closed(0, 15), 'z'))
        assert self.check_interval_tree(tree) == True
        assert self.check_min_max(tree) == True


    def test_insert_interval_case5and6(self):
        tree = self.create_simple_tree()
        tree.insert_interval(P.Node(P.closed(29, 32), 'g'))
        assert tree.root.right == P.Node(P.closedopen(28, 29), 'c')
        assert tree.root.right.right == P.Node(P.closed(29, 32), 'g')
        assert tree.root.right.right.right == P.Node(P.singleton(40), 'i')
        assert self.check_interval_tree(tree) == True
        assert self.check_min_max(tree) == True

    def test_subtree_enclosure(self):
        tree = self.create_simple_tree()
        assert tree.root.subtree_enclosure == P.closed(4, 40)
        assert tree.root.left.subtree_enclosure == P.closed(4, 15)
        assert tree.root.left.left.subtree_enclosure == P.closed(4, 5)
        assert tree.root.left.right.subtree_enclosure == P.singleton(15)
        assert tree.root.right.subtree_enclosure == P.openclosed(21,40)
        assert tree.root.right.left.subtree_enclosure == P.openclosed(21,24)
        assert tree.root.right.right.subtree_enclosure == P.closed(30,40)
        assert tree.root.right.left.right.subtree_enclosure == P.singleton(24)
        assert tree.root.right.right.right.subtree_enclosure == P.singleton(40)

    def test_left_rotation(self):
        tree = self.create_simple_tree()
        tree.left_rotate(tree.root)
        assert self.check_min_max(tree) == True
        tree.left_rotate(tree.root)
        assert self.check_min_max(tree) == True
        tree.left_rotate(tree.root)
        assert self.check_min_max(tree) == True

    def test_right_rotation(self):
        tree = self.create_simple_tree()
        tree.right_rotate(tree.root)
        assert self.check_min_max(tree) == True
        assert self.check_size(tree) == True
        tree.right_rotate(tree.root)
        assert self.check_min_max(tree) == True

    def test_delete_interval(self):
        tree = self.create_simple_tree()
        tree.delete_interval(P.closed(18,22))
        assert tree.root == P.Node(P.closedopen(16,18), 'a')
        assert tree.root.right.left == P.Node(P.openclosed(22,23), 'f')
        assert self.check_interval_tree(tree) == True

    def test_get(self):
        tree = self.create_simple_tree()
        assert tree.get(P.closed(14,25)) == [(P.singleton(15), 'e'), (P.closed(16,21), 'a'), (P.openclosed(21,23), 'f'), (P.singleton(24), 'h')]

    def test_items(self):
        tree = self.create_simple_tree()
        tree.insert_interval(P.Node(P.closed(50, 55), 'a'))
        assert tree.items() == [(P.closed(4, 5), 'd'), (P.closed(9,10), 'b'), (P.singleton(15), 'e'), (P.closed(16, 21) | P.closed(50,55), 'a'), (P.openclosed(21, 23), 'f'), (P.singleton(24), 'h'), (P.closed(28, 29), 'c'), (P.closedopen(30, 32), 'g'), (P.singleton(40), 'i')]

    def test_keys(self):
        tree = self.create_simple_tree()
        assert tree.keys() == [P.closed(4, 5), P.closed(9,10), P.singleton(15), P.closed(16, 21), P.openclosed(21, 23), P.singleton(24), P.closed(28, 29), P.closedopen(30, 32), P.singleton(40)]

    def test_values(self):
        tree = self.create_simple_tree()
        assert tree.values() == ['d', 'b', 'e', 'a', 'f', 'h', 'c', 'g', 'i']

    def test_bug_insertion(self):
        tree = P.IntervalTree()
        tree.insert_interval(P.Node(P.closed(0, 2), 'a'))
        tree.insert_interval(P.Node(P.closed(0, 1), 'a'))
        assert tree.root == P.Node(P.closed(0, 2), 'a')

