import operator as op
import functools
from ete3 import PhyloTree
import sys

def ncr(n, r):
    r = min(r, n-r)
    if r == 0: return 1
    numer = functools.reduce(op.mul, range(n, n-r, -1))
    denom = functools.reduce(op.mul, range(1, r+1))
    return numer//denom


def count_inner(node):

    n = len([x for x in node.iter_descendants() if x.kind != 0])

    return n

def count_total_orders(mytree_file):

    with open(mytree_file) as f:
        mytree = f.readline().strip()
        mytree = PhyloTree(mytree, format=1)


    # We assign kinds to the nodes
    # 0 To leaves
    # 1 To nodes with two descendant to leaves
    # 2 To nodes with one descendant to leaf
    # 3 To nodes with two descendants to inner nodes

    # Value stores the combinatorial value of the node. -1 if it is not computed yet for the node

    i = 0



    for node in mytree.traverse("postorder"):

        if node.is_leaf():
            node.add_features(kind=0, descendants=-1, value=1)

        else:
            i += 1

            node.name = str(i)

            node.add_features(kind=0, descendants=0, value=0)

            children = node.get_children()
            leaves = len([x for x in children if x.is_leaf()])

            if leaves == 2:

                node.kind = 1
                node.value = 1

            elif leaves == 1:

                node.kind = 2
                node.value = -1

            elif leaves == 0:

                node.kind = 3
                node.value = -1

            node.descendants = count_inner(node)


    myroot = node.get_tree_root()
    myroot.value = -1

    while myroot.value == -1:

        for node in mytree.traverse("postorder"):

            if node.kind != 0 and node.kind != 1:

                c1, c2 = node.get_children()
                if c1.value == -1 or c2.value == -1:
                    continue
                x, y = c1.descendants + 1, c2.descendants + 1

                node.value = ncr(x+y,x) * (c1.value * c2.value)

    print(myroot.value)



if __name__ == "__main__":

    if len(sys.argv) != 2:
        print ("usage: python count_total_orders.py mytree")
        exit(0)

    scr, mytree_file = sys.argv
    count_total_orders(mytree_file)
