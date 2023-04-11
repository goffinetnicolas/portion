import portion as P
import random as r
import timeit as t

def generate_interval(lower_bound, upper_bound, length):
    num = r.randint(0, 4)
    a = r.randint(lower_bound, upper_bound)
    b = r.randint(1, length)
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

def generate_dic_set2(n, min, max, maxlength):

    set = generate_random_dic_set(n, min, max, maxlength)
    visited = []
    m=0
    for s in set:
        for v in visited:
            if s[0].overlaps(v[0]):
                m+=1
                break
        visited.append(s)
    o=n-m
    print(m/n * 100, "% overlap")
    return set

def generate_random_dic_set(n, min, max, maxlength):
    set = []
    values = ["a", "b", "c"]
    for i in range(n):
        s = generate_interval(min, max, maxlength)
        set.append([s, r.choice(values)])
    return set

def timer():
    print(t.timeit("timer_interval_tree(a)", setup="from __main__ import timer_interval_tree, a", number=1))
    print(t.timeit("timer_dict(a)", setup="from __main__ import timer_dict, a", number=1))
    print()
    print(t.timeit("timer_interval_tree(b)", setup="from __main__ import timer_interval_tree, b", number=1))
    print(t.timeit("timer_dict(b)", setup="from __main__ import timer_dict, b", number=1))
    print()
    print(t.timeit("timer_interval_tree(c)", setup="from __main__ import timer_interval_tree, c", number=1))
    print(t.timeit("timer_dict(c)", setup="from __main__ import timer_dict, c", number=1))
    print()
    print(t.timeit("timer_interval_tree(d)", setup="from __main__ import timer_interval_tree, d", number=1))
    print(t.timeit("timer_dict(d)", setup="from __main__ import timer_dict, d", number=1))
    print()
    print(t.timeit("timer_interval_tree(e)", setup="from __main__ import timer_interval_tree, e", number=1))
    print(t.timeit("timer_dict(e)", setup="from __main__ import timer_dict, e", number=1))
    print()
    print(t.timeit("timer_interval_tree(f)", setup="from __main__ import timer_interval_tree, f", number=1))
    print(t.timeit("timer_dict(f)", setup="from __main__ import timer_dict, f", number=1))
    print()
    print(t.timeit("timer_interval_tree(g)", setup="from __main__ import timer_interval_tree, g", number=1))
    print(t.timeit("timer_dict(g)", setup="from __main__ import timer_dict, g", number=1))
    print()
    print(t.timeit("timer_interval_tree(h)", setup="from __main__ import timer_interval_tree, h", number=1))
    print(t.timeit("timer_dict(h)", setup="from __main__ import timer_dict,h ", number=1))
    print()
    print(t.timeit("timer_interval_tree(i)", setup="from __main__ import timer_interval_tree, i", number=1))
    print(t.timeit("timer_dict(i)", setup="from __main__ import timer_dict, i", number=1))
    print()
    print(t.timeit("timer_interval_tree(j)", setup="from __main__ import timer_interval_tree, j", number=1))
    print(t.timeit("timer_dict(j)", setup="from __main__ import timer_dict, j", number=1))
    print()
    print(t.timeit("timer_interval_tree(k)", setup="from __main__ import timer_interval_tree, k", number=1))
    print(t.timeit("timer_dict(k)", setup="from __main__ import timer_dict, k", number=1))
    print()
    print(t.timeit("timer_interval_tree(l)", setup="from __main__ import timer_interval_tree, l", number=1))
    print(t.timeit("timer_dict(l)", setup="from __main__ import timer_dict, l", number=1))
    print()

a=generate_dic_set2(10000, -1000000, 1000000, 100000)
b=generate_dic_set2(10000, -1000000, 1000000, 5000)
c=generate_dic_set2(10000, -1000000, 1000000, 2500)
d=generate_dic_set2(10000, -1000000, 1000000, 1250)
e=generate_dic_set2(10000, -1000000, 1000000, 500)
f=generate_dic_set2(10000, -1000000, 1000000, 250)
g=generate_dic_set2(10000, -1000000, 1000000, 100)
h=generate_dic_set2(10000, -1000000, 1000000, 50)
i=generate_dic_set2(10000, -1000000, 1000000, 25)
j=generate_dic_set2(10000, -1000000, 1000000, 10)
k=generate_dic_set2(10000, -1000000, 1000000, 5)
l=generate_dic_set2(10000, -1000000, 1000000, 1)


if __name__ == "__main__":
    timer()