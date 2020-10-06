from ete3 import Tree
import sys

def get_order(tree):

    mytree = Tree(tree, format=1)
    distances = dict()

    for mynode in mytree.traverse():
       if mynode.is_leaf():
           continue
       one_leaf = mynode.get_leaves()[0]
       dist = mynode.get_distance(one_leaf)
       distances[mynode.name] = dist

    node_order = sorted(distances.items(), key=lambda x: x[1])
    node_order = [x[0] for x in node_order][::-1]
    return ",".join(node_order)


def get_node_order(tree_file):

    with open(tree_file) as f:
        for line in f:
            print(get_order(line.strip()))


if __name__ == "__main__":

    if len(sys.argv) != 2:
        print ("usage: python get_node_order.py tree_file")
        exit(0)

    scr, tree_file = sys.argv
    get_node_order(tree_file)
