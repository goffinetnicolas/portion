import portion as P
import random as r


import timeit as t


def check_nil_color(tree):
    """
    Check if the tree is well-structured with respect to the nil node (must always be black)
    """

    current = tree.minimum(tree.root)
    while not current.is_nil:
        if current.left.is_nil:
            if current.left.color == True:
                print("check_nil_color : ", current, " left is nil but color is red")
                return False
        if current.right.is_nil:
            if current.right.color == True:
                print("check_nil_color : ", current, " right is nil but color is red")
                return False
        current = tree.successor(current)
    return True


def check_red_colors(tree):
    """
    Check if the tree is well-structured with respect to the red nodes
    If a node is red, then both its children are black
    """

    current = tree.minimum(tree.root)
    while not current.is_nil:
        if current.color == True:
            if current.left.color == True or current.right.color == True:
                print("check_red_colors : ", current, " is red but one of its children is red")
                return False
        current = tree.successor(current)
    return True


def check_each_nodes_black_colors(tree):
    """
    Check if the tree is well-structured with respect to the black nodes
    For each node, all simple paths from the node to descendant leaves contain the same number of black nodes
    """

    current = tree.minimum(tree.root)
    while not current.is_nil:
        if not check_black_colors(current, tree):
            print("check_each_nodes_black_colors : ", current, " is not well-structured")
            return False
        current = tree.successor(current)
    return True


def create_path(x, p, tree):
    """
    Used to verify if all the paths have the same number of black nodes
    """
    path = [tree.nil]
    while x != p.p:
        path.append(x)
        x = x.p
    return path


def check_black_colors(x, tree):
    """
    Check for a single node if all simple paths from the node
    to descendant leaves contain the same number of black nodes
    """

    current = tree.minimum(x)
    paths = []
    while current != tree.successor(tree.maximum(x)):
        if current.left.is_nil:
            path = create_path(current, x, tree)
            paths.append(path)
        if current.right.is_nil:
            path = create_path(current, x, tree)
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
            print("check_black_colors : ", x, " is not well-structured")
            return False
    return True


def check_rb_tree(tree):
    """
    Check if the tree respect the red black tree properties
    """

    if tree.root.is_nil:
        return True

    # The root is black.
    a = tree.root.color == False

    # Every leaf (NIL) is black.
    b = check_nil_color(tree)

    # If a node is red, then both its children are black.
    c = check_red_colors(tree)

    # For each node, all simple paths from the node to descendant leaves contain the same number of black nodes.
    d = check_each_nodes_black_colors(tree)

    return a and b and c and d


def check_interval_tree(tree):
    """
    Check if the tree respect the interval tree properties (no overlapping intervals)
    """

    if tree.root.is_nil:
        return True

    visited = []
    current = tree.minimum(tree.root)
    while not current.is_nil:
        for v in visited:
            if v.interval.overlaps(current.interval):
                print("check_interval_tree : ", current, " overlaps with ", v)
                return False
        visited.append(current)
        current = tree.successor(current)
    return check_rb_tree(tree)


def generate_interval(lower_bound, upper_bound, length):
    num = r.randint(0, 4)
    a = r.randint(lower_bound, upper_bound)
    b = r.randint(0, length)
    c = a + b
    if num == 0:
        return P.open(a, c)
    if num == 1:
        return P.closed(a, c)
    if num == 2:
        return P.openclosed(a, c)
    if num == 3:
        return P.closedopen(a, c)
    if num == 4:
        return P.singleton(a)

def test_interval_correct():
    tree = P.IntervalTree()
    values = ["a", "b", "c"]
    for i in range(10000):
        print()
        print(tree)
        s = generate_interval(0, 30, 3)
        node = P.Node(s, r.choice(values))
        print(i, " inserting : ", node)
        tree.insert_interval(node)
        print()
        print(tree)
        if not tree.root.is_nil:
            if check_size(tree) == False:
                return False
            if check_min_max(tree) == False:
                return False
            if check_interval_tree(tree) == False:
                return False
        a = r.randint(0, 20)
        if not tree.root.is_nil:
            if a == 0:
                u = r.randint(0, tree.root.size - 1)
                n = tree.minimum(tree.root)
                while u != 0:
                    u -= 1
                    n = tree.successor(n)
                print("deleting : ", n)
                tree.delete(n)
                if not tree.root.is_nil:
                    if check_size(tree) == False:
                        return False
                    if check_min_max(tree) == False:
                        return False
                    if check_interval_tree(tree) == False:
                        return False
def hard_test():
    #while (True):
    test_interval_correct()


def test_delete_interval_correct():
    tree = P.IntervalTree()
    values = ["a", "b", "c"]
    nodes = []
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


def check_size(tree):
    current = tree.minimum(tree.root)
    while not current.is_nil:
        if current.size != current.left.size + current.right.size + 1:
            return False
        current = tree.successor(current)
    return True

def check_min_max(tree):
    current = tree.minimum(tree.root)
    while not current.is_nil:
        if current.maximum != maximum(current):
            print(current)
            return False
        if current.minimum != minimum(current):
            print(current)
            return False
        current = tree.successor(current)
    return True

def minimum(x):
    if x.is_nil:
        raise TypeError("cannot compute minimum of empty tree")
    while not x.left.is_nil:
        x = x.left
    return x

def maximum(x):
    if x.is_nil:
        raise TypeError("cannot compute minimum of empty tree")
    while not x.right.is_nil:
        x = x.right
    return x

def generate_dic_set(n):
    set = []
    values = ["a", "b", "c"]
    for i in range(n):
        s = generate_interval(-10000, 10000, 10000)
        set.append([s, r.choice(values)])
    return set

def timer_interval_tree(set):
    tree = P.IntervalTree()
    for s in set:
        tree.insert_interval(P.Node(s[0], s[1]))
    return tree

def timer_dict(set):
    dic = P.IntervalDict()
    for s in set:
        dic[s[0]] = s[1]
    return dic

set = generate_dic_set(1000000)
def timer():

    print(t.timeit("timer_interval_tree(set)", setup="from __main__ import timer_interval_tree, set", number=1))
    print(t.timeit("timer_dict(set)", setup="from __main__ import timer_dict, set", number=1))


if __name__ == "__main__":
    #timer()
    hard_test()
