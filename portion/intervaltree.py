from .func import empty
from .interval import Interval

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

        self.minimum = self
        self.maximum = self

        # nil nodes have self.size = 0
        # leaf nodes have self.size = 1
        # other nodes have size = self.left.size + self.right.size + 1
        self.size = 1

        # False = black
        # True = red
        self.color = True

    @property
    def is_nil(self):
        """
        check if the node is a nil node
        """

        return self.interval == empty()

    @property
    def subtree_enclosure(self):
        """
        compute the enclosure of the subtree
        """

        return Interval.from_atomic(self.minimum.interval.left, self.minimum.interval.lower, self.maximum.interval.upper, self.maximum.interval.right)

    def __eq__(self, other):
        if isinstance(other, Node):
            return self.interval == other.interval and self.value == other.value
        return NotImplemented

    def __repr__(self):
        if self.color is True:
            return f'interval: {self.interval}, value: {self.value}, color: red, size : {self.size}, minimum: {self.minimum.interval}, maximum: {self.maximum.interval}, enclosure: {self.subtree_enclosure}'
        if self.color is False:
            return f'interval: {self.interval}, value: {self.value}, color: black, size : {self.size}, minimum: {self.minimum.interval}, maximum: {self.maximum.interval}, enclosure: {self.subtree_enclosure}'


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
        self.nil = Node(empty(), "NIL")
        self.nil.color = False
        self.nil.size = 0

        # define empty root
        self.root = self.nil

    def __repr__(self):
        return self.display(self.root)

    def display(self, x, level=0):
        """
        display recursively the tree
        :param x: node used to visit the tree
        :param level: current level of height in the tree
        :return: a string representing the tree
        """

        tree = "\t" * level + repr(x) + "\n"
        if not x.is_nil:
            tree += self.display(x.left, level + 1)
            tree += self.display(x.right, level + 1)
        return tree

    def successor(self, x):
        """
        Find the successor of a node
        :param x: the input node
        :return: the successor of x
        """

        if not x.right.is_nil:
            return x.right.minimum
        y = x.p
        while not y.is_nil and x == y.right:
            x = y
            y = y.p
        return y

    def predecessor(self, x):
        """
        Find the predecessor of a node
        :param x: the input node
        :return: the predecessor of x
        """

        if not x.left.is_nil:
            return x.left.maximum
        y = x.p
        while not y.is_nil and x == y.left:
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
        if not y.left.is_nil:
            y.left.p = x
        y.p = x.p
        if x.p.is_nil:
            self.root = y
        elif x == x.p.left:
            x.p.left = y
        else:
            x.p.right = y
        y.left = x
        x.p = y

        # update size
        y.size = x.size
        x.size = x.left.size + x.right.size + 1

        # update minimum and maximum
        y.minimum = x.minimum
        if x.right.is_nil:
            x.maximum = x
        else:
            x.maximum = x.right.maximum

    def right_rotate(self, x):
        """
        Right rotation of the tree
        Must maintain nodes attributes such as size
        symmetric to left_rotate
        """

        y = x.left
        x.left = y.right
        if not y.right.is_nil:
            y.right.p = x
        y.p = x.p
        if x.p.is_nil:
            self.root = y
        elif x == x.p.right:
            x.p.right = y
        else:
            x.p.left = y
        y.right = x
        x.p = y

        # update size
        y.size = x.size
        x.size = x.left.size + x.right.size + 1

        # update minimum and maximum
        y.maximum = x.maximum

        if x.left.is_nil:
            x.minimum = x
        else:
            x.minimum = x.left.minimum

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
        while not x.is_nil:
            # update size
            x.size = x.size + 1

            # update minimum and maximum
            if x.minimum.interval > z.interval:
                x.minimum = z
            if x.maximum.interval < z.interval:
                x.maximum = z

            y = x
            if z.interval < x.interval:
                x = x.left
            else:
                x = x.right
        z.p = y
        if y.is_nil:
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

        if u.p.is_nil:
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
        if z.left.is_nil:
            x = z.right
            self.rb_transplant(z, z.right)

            # update node attributes from x to root
            f = x.p
            while not f.is_nil:

                # update size
                f.size = f.size - 1

                # update minimum and maximum
                if z == f.minimum:
                    if f.left.is_nil:
                        f.minimum = f
                    else:
                        f.minimum = f.left.minimum

                if z == f.maximum:
                    if f.right.is_nil:
                        f.maximum = f
                    else:
                        f.maximum = f.right.maximum

                f = f.p

        elif z.right.is_nil:
            x = z.left
            self.rb_transplant(z, z.left)

            # update node attributes from x to root
            f = x.p
            while not f.is_nil:

                # update size
                f.size = f.size - 1

                # update minimum and maximum
                if z == f.minimum:
                    if f.left.is_nil:
                        f.minimum = f
                    else:
                        f.minimum = f.left.minimum

                if z == f.maximum:
                    if f.right.is_nil:
                        f.maximum = f
                    else:
                        f.maximum = f.right.maximum

                f = f.p
        else:
            y = z.right.minimum

            # update node attributes from y to root
            u = y
            u.size = z.size
            while not u.is_nil:

                # update size
                u.size = u.size - 1

                # update minimum and maximum
                if y == u.left:
                    if y.maximum != y:
                        u.minimum = y.maximum
                    else:
                        u.minimum = u
                else:
                    if u.minimum == y:
                        u.minimum = u.left.minimum

                u = u.p

            # update minimum and maximum
            y.maximum = z.maximum
            y.minimum = z.minimum

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

    def locate_nodes_deletion(self, x, interval, safe_node, safe_subtree, unsafe_node, unsafe_subtree):
        """
        Recursive function to modify the subtree
        Nodes that overlap with z must be deleted or cut

        @param x: node used to visit the subtree
        @param interval: range to be deleted
        @param safe_node: list of nodes that will not be deleted
        @param safe_subtree: list of subtrees that will not be deleted
        @param unsafe_node: list of nodes that will be deleted
        @param unsafe_subtree: list of subtrees that will be deleted
        """

        if x.is_nil:
            return
        if x.interval < interval:
            safe_node.append(x)
            if not x.left.is_nil:
                safe_subtree.append(x.left)
            if not self.check_right_enclosure(x, interval, safe_subtree, unsafe_subtree):
                self.locate_nodes_deletion(x.right, interval, safe_node, safe_subtree, unsafe_node, unsafe_subtree)
            return
        elif x.interval > interval:
            safe_node.append(x)
            if not x.right.is_nil:
                safe_subtree.append(x.right)
            if not self.check_left_enclosure(x, interval, safe_subtree, unsafe_subtree):
                self.locate_nodes_deletion(x.left, interval, safe_node, safe_subtree, unsafe_node, unsafe_subtree)
            return
        elif x.interval in interval:
            unsafe_node.append(x)
            if not self.check_right_enclosure(x, interval, safe_subtree, unsafe_subtree):
                self.locate_nodes_deletion(x.right, interval, safe_node, safe_subtree, unsafe_node, unsafe_subtree)
            if not self.check_left_enclosure(x, interval, safe_subtree, unsafe_subtree):
                self.locate_nodes_deletion(x.left, interval, safe_node, safe_subtree, unsafe_node, unsafe_subtree)
            return
        elif x.interval <= interval:
            x.interval = x.interval - interval
            safe_node.append(x)
            if not self.check_right_enclosure(x, interval, safe_subtree, unsafe_subtree):
                self.locate_nodes_deletion(x.right, interval, safe_node, safe_subtree, unsafe_node, unsafe_subtree)
            if not x.left.is_nil:
                safe_subtree.append(x.left)
            return
        else:
            # x.interval >= interval
            x.interval = x.interval - interval
            safe_node.append(x)
            if not self.check_left_enclosure(x, interval, safe_subtree, unsafe_subtree):
                self.locate_nodes_deletion(x.left, interval, safe_node, safe_subtree, unsafe_node, unsafe_subtree)
            if not x.right.is_nil:
                safe_subtree.append(x.right)
            return

    def delete_interval(self, interval):
        """
        Delete the range of interval in the tree
        """

        x = self.root
        safe_node = []
        safe_subtree = []
        unsafe_node = []
        unsafe_subtree = []

        # visit the tree until we meet an overlapping node
        while not x.interval.overlaps(interval):
            safe_node.append(x)
            if x.interval < interval:
                if not x.left.is_nil:
                    safe_subtree.append(x.left)
                x = x.right
            else:
                if not x.right.is_nil:
                    safe_subtree.append(x.right)
                x = x.left

        # special case, we may insert a new node instead of deleting one
        if interval in x.interval and x.interval != interval:
            new_interval = x.interval - interval
            x.interval = new_interval[0]
            if len(new_interval) == 2:
                self.insert(Node(new_interval[1], x.value))
            return

        self.locate_nodes_deletion(x, interval, safe_node, safe_subtree, unsafe_node, unsafe_subtree)

        # computing the number of nodes to delete
        unsafe_count = len(unsafe_node)
        for node in unsafe_subtree:
            unsafe_count = unsafe_count + node.size

        if unsafe_count >= self.root.size / 2:
            # too many nodes to delete

            # fuse safe nodes and safe subtree
            for node in safe_subtree:
                if not node.is_nil:
                    current = node.minimum
                    while current != self.successor(node.maximum):
                        safe_node.append(current)
                        current = self.successor(current)

            # create new tree and add all safe nodes
            self.__init__()
            for node in safe_node:
                self.insert(Node(node.interval, node.value))
        else:
            # fuse unsafe nodes and unsafe subtrees
            for node in unsafe_subtree:
                current = node.minimum
                while current != self.successor(node.maximum):
                    unsafe_node.append(current)
                    current = self.successor(current)
            # delete all unsafe nodes
            for node in unsafe_node:
                self.delete(node)

    def locate_nodes_insertion(self, y, z, safe_subtree, safe_node, extend, unsafe_subtree, unsafe_node):
        """
        Recursive function to modify the subtree
        Nodes that overlap with z must be deleted or cut

        @param y: node used to visit the subtree
        @param z: inserted node
        @param safe_subtree: list of subtrees that will not be deleted
        @param safe_node: list of nodes that will not be deleted
        @param extend: list of nodes that have to extend x interval
        @param unsafe_subtree: list of subtrees that will be deleted
        @param unsafe_node: list of nodes that will be deleted
        """

        if y.is_nil:
            return
        if y.interval < z.interval:
            safe_node.append(y)
            if not y.left.is_nil:
                safe_subtree.append(y.left)
            if not self.check_right_enclosure(y, z.interval, safe_subtree, unsafe_subtree):
                self.locate_nodes_insertion(y.right, z, safe_subtree, safe_node, extend, unsafe_subtree, unsafe_node)
            return
        elif y.interval > z.interval:
            safe_node.append(y)
            if not y.right.is_nil:
                safe_subtree.append(y.right)
            if not self.check_left_enclosure(y, z.interval, safe_subtree, unsafe_subtree):
                self.locate_nodes_insertion(y.left, z, safe_subtree, safe_node, extend, unsafe_subtree, unsafe_node)
            return
        elif y.interval in z.interval:
            unsafe_node.append(y)
            if not self.check_right_enclosure(y, z.interval, safe_subtree, unsafe_subtree):
                self.locate_nodes_insertion(y.right, z, safe_subtree, safe_node, extend, unsafe_subtree, unsafe_node)
            if not self.check_left_enclosure(y, z.interval, safe_subtree, unsafe_subtree):
                self.locate_nodes_insertion(y.left, z, safe_subtree, safe_node, extend, unsafe_subtree, unsafe_node)
            return
        elif y.interval <= z.interval:
            if y.value == z.value:
                if not y.left.is_nil:
                    safe_subtree.append(y.left)
                if not y.right.is_nil:
                    unsafe_subtree.append(y.right)
                extend.append(y)
                unsafe_node.append(y)
                return
            else:
                y.interval = y.interval - z.interval
                safe_node.append(y)
                if not y.right.is_nil:
                    unsafe_subtree.append(y.right)
                if not y.left.is_nil:
                    safe_subtree.append(y.left)
                return
        else:
            # x.interval >= z
            if y.value == z.value:
                if not y.right.is_nil:
                    safe_subtree.append(y.right)
                if not y.left.is_nil:
                    unsafe_subtree.append(y.left)
                extend.append(y)
                unsafe_node.append(y)
                return
            else:
                y.interval = y.interval - z.interval
                safe_node.append(y)
                if not y.left.is_nil:
                    unsafe_subtree.append(y.left)
                if not y.right.is_nil:
                    safe_subtree.append(y.right)
                return

    def check_left_enclosure(self, y, interval, safe_subtree, unsafe_subtree):
        """
        Check the left enclosure x and decide which action to take

        :param y: the input node
        :param interval: the target interval
        :param safe_subtree: used to store x.left if it is safe
        :param unsafe_subtree: used to store x.left if it is unsafe
        :return: True if x.left subtree is safe or unsafe, False otherwise (we must continue to visit x.left)

        """

        if y.left.is_nil:
            return True
        if y.left.subtree_enclosure < interval:
            if not y.left.is_nil:
                safe_subtree.append(y.left)
            return True
        elif y.left.subtree_enclosure in interval:
            if not y.left.is_nil:
                unsafe_subtree.append(y.left)
            return True
        else:
            return False

    def check_right_enclosure(self, y, interval, safe_subtree, unsafe_subtree):
        """
        Check the right enclosure x and decide which action to take

        :param y: the input node
        :param interval: the target interval
        :param safe_subtree: used to store x.right if it is safe
        :param unsafe_subtree: used to store x.right if it is unsafe
        :return: True if x.right subtree is safe or unsafe, False otherwise (we must continue to visit x.right)
        """

        if y.right.is_nil:
            return True
        if y.right.subtree_enclosure > interval:
            if not y.right.is_nil:
                safe_subtree.append(y.right)
            return True
        elif y.right.subtree_enclosure in interval:
            if not y.right.is_nil:
                unsafe_subtree.append(y.right)
            return True
        else:
            return False

    def modify(self, x, z):
        """
        extend the subtree x depending on the inserted node z

        :param x: node used to visit the subtree
        :param z: the inserted node
        """

        # go in subtree x and locate all type of nodes

        safe_subtree = []
        safe_node = [x]
        extend = []
        unsafe_subtree = []
        unsafe_node = []

        if not self.check_left_enclosure(x, z.interval, safe_subtree, unsafe_subtree):
            self.locate_nodes_insertion(x.left, z, safe_subtree, safe_node, extend, unsafe_subtree, unsafe_node)
        if not self.check_right_enclosure(x, z.interval, safe_subtree, unsafe_subtree):
            self.locate_nodes_insertion(x.right, z, safe_subtree, safe_node, extend, unsafe_subtree, unsafe_node)

        # extend x interval
        for node in extend:
            x.interval = x.interval | node.interval

        # compute the number of nodes to be deleted
        unsafe_count = len(unsafe_node)
        for node in unsafe_subtree:
            unsafe_count = unsafe_count + node.size

        if unsafe_count >= self.root.size / 2:
            # too many nodes to delete

            # fuse safe nodes and safe subtree
            for node in safe_subtree:
                if not node.is_nil:
                    current = node.minimum
                    while current != self.successor(node.maximum):
                        safe_node.append(current)
                        current = self.successor(current)

            # find other safe nodes in the tree
            current = x
            while current.p != self.nil:
                if current.p.left == current:
                    current = current.p
                    safe_node.append(current)
                    # add all nodes in the right subtree of current node
                    other_sub = current.right
                    current2 = other_sub.minimum
                    while current2 != self.successor(other_sub.maximum):
                        safe_node.append(current2)
                        current2 = self.successor(current2)
                else:
                    # current.p.right == current
                    current = current.p
                    safe_node.append(current)
                    # add all nodes in the left subtree of current node
                    other_sub = current.left
                    current2 = other_sub.minimum
                    while current2 != self.successor(other_sub.maximum):
                        safe_node.append(current2)
                        current2 = self.successor(current2)

            # create new tree and add all safe nodes
            self.__init__()
            for node in safe_node:
                self.insert(Node(node.interval, node.value))
        else:
            # fuse unsafe nodes and unsafe subtrees
            for node in unsafe_subtree:
                current = node.minimum
                while current != self.successor(node.maximum):
                    unsafe_node.append(current)
                    current = self.successor(current)
            # delete all unsafe nodes
            for node in unsafe_node:
                self.delete(node)

    def insert_interval(self, z):
        """
        Insert a node such that his interval does not overlap with any other node in the tree
        Some other nodes may be inserted, deleted or fused
        """

        y = self.nil
        x = self.root
        while not x.is_nil:
            y = x
            if z.interval < x.interval:
                x = x.left
            elif z.interval > x.interval:
                x = x.right
            elif x.interval == z.interval:
                # case 1 : x interval is equal to z interval
                x.value = z.value
                return
            elif z.interval in x.interval and z.value != x.value:
                # case 2 : z interval is included in x interval and have different value
                new_intervals = x.interval - z.interval
                x.interval = z.interval
                for interval in new_intervals:
                    self.insert(Node(interval, x.value))
                x.value = z.value
                return
            elif x.interval in z.interval:
                # case 3 : x interval is included in z interval
                x.interval = z.interval
                x.value = z.value
                self.modify(x, z)
                return
            elif z.interval <= x.interval:
                if x.value == z.value:
                    # case 4 : z interval <= x interval and have the same value
                    # extend x value
                    x.interval = x.interval | z.interval
                    self.modify(x, z)
                    return
                else:
                    # cut left x value
                    # case 5 : x interval <= z interval and have different value
                    x.interval = x.interval - z.interval
                    x = x.left
            else:
                # symmetric case of case 4 and 5
                if x.value == z.value:
                    x.interval = x.interval | z.interval
                    self.modify(x, z)
                    return
                else:
                    # cut right x value
                    x.interval = x.interval - z.interval
                    x = x.right

        # nil node is reached
        # normal insertion (red-black tree insertion)
        z.p = y
        if y.is_nil:
            self.root = z
        elif z.interval < y.interval:
            y.left = z
        else:
            y.right = z
        z.left = self.nil
        z.right = self.nil
        z.color = True

        # update nodes attributes
        f = z.p
        while not f.is_nil:

            # update size
            f.size = f.size + 1

            if f.minimum.interval > z.interval:
                f.minimum = z
            if f.maximum.interval < z.interval:
                f.maximum = z

            f = f.p

        self.rb_insert_fixup(z)

    def insert_interval_value(self, interval, value):
        """
        fast insertion of an interval with a value
        :param interval: the input interval
        :param value: the value associated to the interval
        """

        self.insert_interval(Node(interval, value))

    def search(self, key):
        """
        visit the tree to get the items associated to the interval
        :param key: the target interval
        :return: a list of tuples (interval, value) where the interval is the intersection between the target interval
        """

        items = []
        x = self.root
        while not x.interval.overlaps(key):
            if x.interval < key:
                x = x.right
            else:
                x = x.left
        while self.predecessor(x).interval.overlaps(key):
            x = self.predecessor(x)
        while x.interval.overlaps(key):
            intersection = key & x.interval
            if not intersection.empty:
                items.append((intersection, x.value))
            x = self.successor(x)
        return items

    def items(self):
        """
        visit the tree to get all items
        :return: a list of tuples (interval, value)
        """

        items = []
        current = self.root.minimum
        while not current.is_nil:
            found = False
            for item in items:
                if item[1] == current.value:
                    item[0] |= current.interval
                    found = True
                    break
            if not found:
                items.append([current.interval, current.value])
            current = self.successor(current)
        for i in range(len(items)):
            items[i] = tuple(items[i])
        return items

    def keys(self):
        """
        visit the tree to get all keys
        :return: a list of intervals
        """

        return [item[0] for item in self.items()]

    def values(self):
        """
        visit the tree to get all values
        :return: a list of values
        """

        values = []
        current = self.root.minimum
        while not current.is_nil:
            if current.value not in values:
                values.append(current.value)
            current = self.successor(current)
        return values

    def find(self, value):
        """
        get the key associated to the value
        :param value: the input value
        :return: the interval associated to the value
        """

        key = empty()
        x = self.root.minimum
        while not x.is_nil:
            if x.value == value:
                key |= x.interval
            x = self.successor(x)
        return key
