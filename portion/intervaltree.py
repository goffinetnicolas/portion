class Node:
    """
    represent a node in the interval tree
    """

    def __init__(self, interval, value, color=True):
        """

        :param interval: an atomic interval.
        :param value: a value mapped to the interval.
        :param color: the color in the tree (red or black)
        """

        self.interval = interval
        self.value = value

        # parent of the node
        self.p = None
        # left child
        self.left = None
        # right child
        self.right = None

        # left enclosure (range of all intervals in left subtree of the node)
        self.left_enclosure = interval
        # right enclosure (range of all intervals in right subtree of the node)
        self.right_enclosure = interval

        # nil nodes have self.size = 0
        # leaf nodes have self.size = 1
        # other nodes have size = self.left.size + self.right.size + 1
        self.size = 0

        # False = black
        # True = red
        self.color = color

    def is_nil(self):
        return self.interval == "NIL"

    def __eq__(self, other):
        if isinstance(other, Node):
            return self.interval == other.interval and self.value == other.value
        return NotImplemented

    def __repr__(self):
        if self.color is True:
            return f'interval: {self.interval}, value: {self.value}, color: red, size : {self.size}'
        if self.color is False:
            return f'interval: {self.interval}, value: {self.value}, color: black, size : {self.size}'


class IntervalTree:
    def __init__(self):

        # define NIL node
        self.nil = Node("NIL", "NIL", False)

        # define empty root
        self.root = self.nil

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

    def check_each_nodes_black_colors(self):
        current = self.minimum(self.root)
        while not current.is_nil():
            if not self.check_black_colors(current):
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
        d = self.check_each_nodes_black_colors()

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
        y.size = x.size
        x.size = x.left.size + x.right.size + 1

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
        y.size = x.size
        x.size = x.left.size + x.right.size + 1

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
            x.size = x.size + 1
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
        z.size = 1

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

        # update size
        y.size = z.size
        while not y.is_nil():
            y.size = y.size - 1
            y = y.p

    def delete_using_interval(self, x, interval):
        """
        delete first interval found in the tree
        """

        while not x.is_nil():
            if interval == x.interval:
                self.delete(x)
            if x.interval < interval:
                x = x.right
            else:
                x = x.left

    def delete_using_value(self, value):
        """
        delete all nodes in the tree who has the same value
        """

        current = self.minimum(self.root)
        while not current.is_nil():
            if current.value == value:
                self.delete(current)
            current = self.successor(current)

    def check_overlap(self, x, z, safesubtree, safenode, modify, unsafesubtree, unsafenode):
        if x.is_nil():
            return
        if x.interval < z.interval:
            safesubtree.append(x.left)
            # TODO check right enclosure
            return self.check_overlap(x.right, z, safesubtree, safenode, modify, unsafesubtree, unsafenode)
        elif x.interval > z.interval:
            safesubtree.append(x.right)
            # TODO check left enclosure
            return self.check_overlap(x.left, z, safesubtree, safenode, modify, unsafesubtree, unsafenode)
        elif x.interval in z.interval:
            unsafenode.append(x)
            # TODO check right enclosure
            self.check_overlap(x.right, z, safesubtree, safenode, modify, unsafesubtree, unsafenode)
            # TODO check left enclosure
            self.check_overlap(x.left, z, safesubtree, safenode, modify, unsafesubtree, unsafenode)
            return
        elif x.interval <= z.interval:
            if x.value == z.value:
                if not x.left.is_nil():
                    safesubtree.append(x.left)
                if not x.right.is_nil():
                    unsafesubtree.append(x.right)
                modify.append(x)
                unsafenode.append(x)
                return
            else:
                x.interval = x.interval - z.interval
                safenode.append(x)
                if not x.right.is_nil():
                    unsafesubtree.append(x.right)
                return
        else:
            # x.interval >= z
            if x.value == z.value:
                if not x.right.is_nil():
                    safesubtree.append(x.right)
                if not x.left.is_nil():
                    unsafesubtree.append(x.left)
                modify.append(x)
                unsafenode.append(x)
                return
            else:
                x.interval = x.interval - z.interval
                safenode.append(x)
                if not x.left.is_nil():
                    unsafesubtree.append(x.left)
                return

    def check_left_enclosure(self, x, unsafesubtree):
        if x.left_enclosure < x.interval:
            return True
        elif x.left_enclosure in x.interval:
            unsafesubtree.append(x.left)
            return True
        else:
            return False

    def check_right_enclosure(self, x, unsafesubtree):
        if x.right_enclosure > x.interval:
            return True
        elif x.right_enclosure in x.interval:
            unsafesubtree.append(x.right)
            return True
        else:
            return False

    def overlap3_helper(self, x, z):

        # go in subtree x and locate all type of nodes

        safesubtree = []
        safenode = [x]
        modify = []
        unsafesubtree = []
        unsafenode = []

        # TODO check left enclosure
        self.check_overlap(x.left, z, safesubtree, safenode, modify, unsafesubtree, unsafenode)
        # TODO check right enclosure
        self.check_overlap(x.right, z, safesubtree, safenode, modify, unsafesubtree, unsafenode)
        for node in modify:
            x.interval = x.interval | node.interval
        safe = len(safenode)
        for node in safesubtree:
            safe = safe + node.size
        unsafe = len(unsafenode)
        for node in unsafesubtree:
            unsafe = unsafe + node.size
        if unsafe >= self.root.size / 2:
            # too many nodes to delete

            # fuse safe nodes and safe subtree
            for node in safesubtree:
                current = self.minimum(node)
                while current != self.successor(self.maximum(node)):
                    safenode.append(current)
                    current = self.successor(current)

            # find other safe nodes in the tree
            current = x
            while current.p != self.nil:
                if current.p.left == current:
                    current = current.p
                    safenode.append(current)
                    # add all nodes in the right subtree of current node
                    left_sub = current.right
                    current2 = self.minimum(left_sub)
                    while current2 != self.successor(self.maximum(left_sub)):
                        safenode.append(current2)
                        current2 = self.successor(current2)
                else:
                    current = current.p
                    safenode.append(current)
                    # add all nodes in the left subtree of current node
                    left_sub = current.left
                    current2 = self.minimum(left_sub)
                    while current2 != self.successor(self.maximum(left_sub)):
                        safenode.append(current2)
                        current2 = self.successor(current2)

            # create new tree and add all safe nodes
            self.__init__()
            for node in safenode:
                self.insert(Node(node.interval, node.value))
        else:
            # fuse unsafe nodes and unsafe subtrees
            for node in unsafesubtree:
                current = self.minimum(node)
                while current != self.successor(self.maximum(node)):
                    unsafenode.append(current)
                    current = self.successor(current)
            # delete all unsafe nodes
            for node in unsafenode:
                self.delete(node)

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
                if z.value == x.value:
                    x.value = z.value
                else:
                    x.interval = z.interval
                    x.value = z.value
                    new_intervals = x.interval - z.interval
                    for interval in new_intervals:
                        self.insert(Node(interval, x.value))
                return
            elif x.interval in z.interval:
                x.interval = z.interval
                x.value = z.value
                self.overlap_helper(x, z)
                return
            elif z.interval <= x.interval:
                if x.value == z.value:
                    # extend x value
                    x.interval = x.interval | z.interval
                    self.overlap_helper(x, z)
                    return
                else:
                    # cut left x value
                    x.interval = x.interval - z.interval
                    x = x.left
            else:
                # z.interval >= x.interval
                if x.value == z.value:
                    x.interval = x.interval | z.interval
                    self.overlap_helper(x, z)
                    return
                else:
                    # cut right x value
                    x.interval = x.interval - z.interval
                    x = x.right

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
        # update size
        z.size = 1
        while not z.p.is_nil():
            z = z.p
            z.size = z.size + 1
