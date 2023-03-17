class Node:
    """
    represent a node in the interval tree
    """

    def __init__(self, interval, value):
        """
        :param interval: an atomic interval.
        :param value: a value mapped to the interval.

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
        self.size = 1

        # False = black
        # True = red
        self.color = True

    def is_nil(self):
        """
        check if the node is a nil node
        """

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
    """
    Represent an interval tree i.e. a red black tree storing atomic intervals mapped to values in the nodes
    The intervals of the nodes cannot overlap each other
    This data structure is used create an interval dictionary
    """

    def __init__(self):
        """
        Create an empty interval tree
        - Create the nil node
        - Set nil node as root
        """

        # define NIL node
        self.nil = Node("NIL", "NIL")
        self.nil.color = False
        self.nil.size = 0

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

    def left_rotate(self, x):
        """
        Left rotation of the tree
        Must maintain nodes attributes such as size
        @see Cormen, Leiserson, Rivest, Stein. Introduction to Algorithms, 3rd edition. 2009. p 313
        """

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
        """
        Right rotation of the tree
        Must maintain nodes attributes such as size
        symmetric to left_rotate
        """

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
        """
        Fix the red black tree properties after an insertion
        @see Cormen, Leiserson, Rivest, Stein. Introduction to Algorithms, 3rd edition. 2009. p 316
        """

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
        """
        Red Black Tree insertion
        Must maintain nodes attributes such as size
        @see Cormen, Leiserson, Rivest, Stein. Introduction to Algorithms, 3rd edition. 2009. p 315
        """

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

    def rb_transplant(self, u, v):
        """
        Replace the subtree rooted at node u with the subtree rooted at node v
        @see Cormen, Leiserson, Rivest, Stein. Introduction to Algorithms, 3rd edition. 2009. p 323
        """

        if u.p.is_nil():
            self.root = v
        elif u == u.p.left:
            u.p.left = v
        else:
            u.p.right = v
        v.p = u.p

    def rb_delete_fixup(self, x):
        """
        Fix the red black tree properties after a deletion
        @see Cormen, Leiserson, Rivest, Stein. Introduction to Algorithms, 3rd edition. 2009. p 326
        """

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
        """
        Red Black Tree deletion
        Must maintain nodes attributes such as size
        @see Cormen, Leiserson, Rivest, Stein. Introduction to Algorithms, 3rd edition. 2009. p 324
        """

        y = z
        y_original_color = y.color
        if z.left.is_nil():
            x = z.right
            self.rb_transplant(z, z.right)

            # update size from x to root
            f = x.p
            while not f.is_nil():
                f.size = f.size - 1
                f = f.p
        elif z.right.is_nil():
            x = z.left
            self.rb_transplant(z, z.left)

            # update size from x to root
            f = x.p
            while not f.is_nil():
                f.size = f.size - 1
                f = f.p
        else:
            y = self.minimum(z.right)

            # update size from y to root
            u = y
            u.size = z.size
            while not u.is_nil():
                u.size = u.size - 1
                u = u.p

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

    def delete_using_interval(self, x, interval):
        """
        Delete first node found in the tree corresponding to the interval
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
        Delete all nodes found in the tree corresponding to the value
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

    def overlap_helper(self, x, z):

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

    def insert_interval(self, z):
        """
        Insert a node such that his interval does not overlap with any other node in the tree
        Some other nodes may be deleted or fused
        """

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
                # case 1 : x interval is equal to z interval
                x.value = z.value
                return
            elif z.interval in x.interval:
                if z.value == x.value:
                    # case 2 : z interval is included in x interval and have the same value
                    x.interval = z.interval
                else:
                    # case 3 : z interval is included in x interval and have different value
                    new_intervals = x.interval - z.interval
                    x.interval = z.interval
                    for interval in new_intervals:
                        self.insert(Node(interval, x.value))
                    x.value = z.value
                return
            elif x.interval in z.interval:
                # case 4 : x interval is included in z interval
                x.interval = z.interval
                x.value = z.value
                self.overlap_helper(x, z)
                return
            elif z.interval <= x.interval:
                if x.value == z.value:
                    # case 5 : z interval <= x interval and have the same value
                    # extend x value
                    x.interval = x.interval | z.interval
                    self.overlap_helper(x, z)
                    return
                else:
                    # cut left x value
                    # case 6 : x interval <= z interval and have different value
                    x.interval = x.interval - z.interval
                    x = x.left
            else:
                # symmetric case of case 5 and 6
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

        # update size
        while not z.p.is_nil():
            z = z.p
            z.size = z.size + 1

        self.rb_insert_fixup(z)
