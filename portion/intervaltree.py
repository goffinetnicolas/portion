import random

from portion import Bound, Interval


class Node:
    def __init__(self, interval, value, color=True):

        self.interval = interval
        self.value = value

        self.p = None
        self.left = None
        self.right = None

        self.min = None
        self.max = None

        # False = black
        # True = red
        self.color = color

    def is_nil(self):
        return self.interval == "NIL"

    def __eq__(self, other):
        if isinstance(other, Node):
            return self.interval == other.interval and self.value == other.value and self.color == other.color
        return NotImplemented

    def __repr__(self):
        if self.color is True:
            return f'interval: {self.interval}, value: {self.value}, color: red'
        if self.color is False:
            return f'interval: {self.interval}, value: {self.value}, color: black'


class IntervalTree:
    def __init__(self, root):

        # define NIL node
        self.nil = Node("NIL", "NIL", False)

        if root == None:
            # define empty root
            self.root = self.nil
        else:
            self.root = root

    def from_subtree(self, x):
        tree = IntervalTree()
        tree.root = x
        return tree


    def __repr__(self):
        return self.display(self.root)

    def display(self, x, level=0):
        tree = "\t" * level + repr(x) + "\n"
        if not x.is_nil():
            tree += self.display(x.left, level + 1)
            tree += self.display(x.right, level + 1)
        return tree

    def recursive_search(self, x, k):
        if x.is_nil() or x.interval.contains(k):
            return x
        if k < x.interval:
            return self.recursive_search(x.left, k)
        else:
            return self.recursive_search(x.right, k)

    def iterative_search(self, x, k):
        while not x.is_nil() and not x.key.contains(k):
            if k < x.key:
                x = x.left
            else:
                x = x.right
        return x

    def minimum(self, x):
        if x.is_nil():
            raise TypeError("cannot compute minimum of empty tree")
        while not x.left.is_nil():
            x = x.left
        return x

    def maximum(self, x):
        if x.is_nil():
            raise TypeError("cannot compute minimum of empty tree")
        while not x.right.is_nil():
            x = x.right
        return x

    def successor(self, x):
        if not x.right.is_nil():
            return self.minimum(x.right)
        y = x.p
        while not y.is_nil() and x == y.right:
            x = y
            y = y.p
        return y

    def check_nil_color(self):
        current = self.minimum(self.root)
        while not current.is_nil():
            if current.left.is_nil():
                if current.left.color == True:
                    return False
            if current.right.is_nil():
                if current.right.color == True:
                    return False
            current = self.successor(current)
        return True

    def check_red_colors(self):
        current = self.minimum(self.root)
        while not current.is_nil():
            if current.color == True:
                if current.left.color == True or current.right.color == True:
                    return False
            current = self.successor(current)
        return True

    def check_node_black_colors(self):
        current = self.minimum(self.root)
        while not current.is_nil():
            if not self.black_colors(current):
                return False
            current = self.successor(current)
        return True

    def create_path(self, x, p):
        path = [self.nil]
        while x != p.p:
            path.append(x)
            x = x.p
        return path

    """
    check for a single node, all simple paths from the node to descendant leaves contain the same number of black nodes
    """

    def check_black_colors(self, x):
        current = self.minimum(x)
        paths = []
        while current != self.successor(self.maximum(x)):
            if current.left.is_nil():
                path = self.create_path(current, x)
                paths.append(path)
            if current.right.is_nil():
                path = self.create_path(current, x)
                paths.append(path)
            current = self.successor(current)
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

    def check_rb_tree(self):

        if self.root.is_nil():
            return True

        # The root is black.
        a = self.root.color == False

        # Every leaf (NIL) is black.
        b = self.check_nil_color()

        # If a node is red, then both its children are black.
        c = self.check_red_colors()

        # For each node, all simple paths from the node to descendant leaves contain the same number of black nodes.
        d = self.check_black_colors()

        return a and b and c and d

    def check_interval_tree(self):

        if self.root.is_nil():
            return True

        # check if the tree doesn't have overlapping intervals
        visited = []
        current = self.minimum(self.root)
        while not current.is_nil():
            for v in visited:
                if v.interval.overlaps(current.interval):
                    return False
            visited.append(current)
            current = self.successor(current)
        return self.check_rb_tree()

    def check_left_right(self):
        current = self.minimum(self.root)
        while not current.is_nil():
            if not current.left.is_nil():
                if current.left.interval > current.interval:
                    return False
            if not current.right.is_nil():
                if current.right.interval < current.interval:
                    return False
            current = self.successor(current)
        return True

    def left_rotate(self, x):
        y = x.right
        x.right = y.left
        if not y.left.is_nil():
            y.left.p = x
        y.p = x.p
        if x.p.is_nil():
            self.root = y
        elif x == x.p.left:
            x.p.left = y
        else:
            x.p.right = y
        y.left = x
        x.p = y

    def right_rotate(self, x):
        y = x.left
        x.left = y.right
        if not y.right.is_nil():
            y.right.p = x
        y.p = x.p
        if x.p.is_nil():
            self.root = y
        elif x == x.p.right:
            x.p.right = y
        else:
            x.p.left = y
        y.right = x
        x.p = y

    def rb_insert_fixup(self, z):
        while z.p.color == True:
            if z.p == z.p.p.left:
                y = z.p.p.right
                if y.color == True:
                    z.p.color = False
                    y.color = False
                    z.p.p.color = True
                    z = z.p.p
                else:
                    if z == z.p.right:
                        z = z.p
                        self.left_rotate(z)
                    z.p.color = False
                    z.p.p.color = True
                    self.right_rotate(z.p.p)
            else:
                y = z.p.p.left
                if y.color == True:
                    z.p.color = False
                    y.color = False
                    z.p.p.color = True
                    z = z.p.p
                else:
                    if z == z.p.left:
                        z = z.p
                        self.right_rotate(z)
                    z.p.color = False
                    z.p.p.color = True
                    self.left_rotate(z.p.p)
        self.root.color = False

    def insert(self, z):
        y = self.nil
        x = self.root
        while not x.is_nil():
            y = x
            if z.interval < x.interval:
                x = x.left
            else:
                x = x.right
        z.p = y
        if y.is_nil():
            self.root = z
        elif z.interval < y.interval:
            y.left = z
        else:
            y.right = z
        z.left = self.nil
        z.right = self.nil
        z.color = True
        self.rb_insert_fixup(z)

    def rb_transplant(self, u, v):
        if u.p.is_nil():
            self.root = v
        elif u == u.p.left:
            u.p.left = v
        else:
            u.p.right = v
        v.p = u.p

    def rb_delete_fixup(self, x):
        while x != self.root and x.color == False:
            if x == x.p.left:
                w = x.p.right
                if w.color == True:
                    w.color = False
                    x.p.color = True
                    self.left_rotate(x.p)
                    w = x.p.right
                if w.left.color == False and w.right.color == False:
                    w.color = True
                    x = x.p
                else:
                    if w.right.color == False:
                        w.left.color = False
                        w.color = True
                        self.right_rotate(w)
                        w = x.p.right
                    w.color = x.p.color
                    x.p.color = False
                    w.right.color = False
                    self.left_rotate(x.p)
                    x = self.root
            else:
                w = x.p.left
                if w.color == True:
                    w.color = False
                    x.p.color = True
                    self.right_rotate(x.p)
                    w = x.p.left
                if w.right.color == False and w.left.color == False:
                    w.color = True
                    x = x.p
                else:
                    if w.left.color == False:
                        w.right.color = False
                        w.color = True
                        self.left_rotate(w)
                        w = x.p.left
                    w.color = x.p.color
                    x.p.color = False
                    w.left.color = False
                    self.right_rotate(x.p)
                    x = self.root
        x.color = False

    def delete(self, z):
        if z.is_nil():
            return
        y = z
        y_original_color = y.color
        if z.left.is_nil():
            x = z.right
            self.rb_transplant(z, z.right)
        elif z.right.is_nil():
            x = z.left
            self.rb_transplant(z, z.left)
        else:
            y = self.minimum(z.right)
            y_original_color = y.color
            x = y.right
            if y.p == z:
                x.p = y
            else:
                self.rb_transplant(y, y.right)
                y.right = z.right
                y.right.p = y
            self.rb_transplant(z, y)
            y.left = z.left
            y.left.p = y
            y.color = z.color
        if y_original_color == False:
            self.rb_delete_fixup(x)

    def join(self, l, k, r):
        pass

    def split(self, x, k):
        if x.is_nil():
            return IntervalTree(), False, IntervalTree()
        if k == x.interval:
            return IntervalTree(x.left), True, IntervalTree(x.right)
        if k < x.interval:
            (l, b, r) = self.split(x.left, k)
            return l, b, self.join(r, x.interval, x.right)
        (l, b, r) = self.split(x.right, k)
        return self.join(x.left, x.interval, l), b, x.right

    def delete_subtree1(self, x, y):
        min = y.min
        max = y.max
        split1 = self.split(x.root, min)

    def delete_subtree2(self, x, y):
        if y.size > x / 2:
            # create new tree
            pass
        else:
            # delete all nodesd in y
            current = self.minimum(y)
            next = self.successor(current)
            while current != self.successor(self.maximum(y)):
                self.delete(current)
                current = next
                next = self.successor(next)

    def check_overlap(self, x, z):
        if x.is_nil():
            return
        elif z.interval <= x.interval:
            pass
        elif z.interval >= x.interval:
            pass
        elif z.interval.contains(x):
            pass
        elif z < x.interval:
            self.recurse(x.left, z)
        elif z > x.interval:
            self.recurse(x.right, z)
        else:
            raise TypeError("unexpected error")

    def insertInterval(self, z):
        if z.interval.empty:
            return
        y = self.nil
        x = self.root
        while not x.is_nil():
            y = x
            if z.interval < x.interval:
                x = x.left
            elif z.interval > x.interval:
                x = x.right
            elif x.interval == z.interval:
                x.value = z.value
                return
            elif z.interval in x.interval:
                # must be tested
                if z.value == x.value:
                    # x = [16,21] and value is "red"
                    # z = [17,20] or [16,20] or [17,21] and value is "red"
                    x.value = z.value
                else:
                    # x = [16,21] and value is "red"
                    # z = [17,20] or [16,20] or [17,21] and value is "blue"
                    x.interval = z.interval
                    x.value = z.value
                    new_intervals = x.interval - z.interval
                    for interval in new_intervals:
                        self.insertInterval(Node(interval, x.value))
                return
            elif z.interval <= x.interval:
                # must be tested
                if x.value == z.value:
                    # extend x value
                    x.interval = x.interval | z.interval
                    self.check_overlap(x.left, z)
                else:
                    # cut x value
                    x.interval = x.interval - z.interval
                    pass
                x = x.left
            elif z.interval >= x.interval:
                # must be tested
                if x.value == z.value:
                    # extend x value
                    x.interval = x.interval | z.interval
                    self.check_overlap(x.right, z)
                    return
                else:
                    # cut x value
                    x.interval = x.interval - z.interval
                    x = x.right
            elif x.interval in z.interval:
                # must be tested
                # special case
                x.interval = z.interval
                x.value = z.value
                self.check_overlap(x.right, z)
                self.check_overlap(x.left, z)
                return
            else:
                raise TypeError("unexpected error")

        # normal insertion (red-black tree insertion)
        z.p = y
        if y.is_nil():
            self.root = z
        elif z.interval < y.interval:
            y.left = z
        else:
            y.right = z
        z.left = self.nil
        z.right = self.nil
        z.color = True
        self.rb_insert_fixup(z)
