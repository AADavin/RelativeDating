from ete3 import Tree
import sys

def ultrametricer(node_order, tree_file):
    with open(tree_file) as f:
        mytree = Tree(f.readline().strip(),format=1)

    # First I get every single leaf

    leaves = mytree.get_leaves()

    # The total distance must be:

    v = len(leaves)

    # Now we get the expected distances
    distances = dict()
    for i,node in enumerate(node_order):

        distances[node] = i+1

    for node in leaves:
        distances[node.name] = v

    # We add the root (that has no name)
    distances[""] = 0

    # We get the root

    root = mytree.get_tree_root()

    for node in leaves:
        #Now I start traversing to the root

        while(node.up):

            # The expected distance of this branch is:
            expected = distances[node.name] - distances[node.up.name]

            node.dist = expected

            node = node.up

    return mytree.write(format=1)


def ultrametrice(species_tree, order_file):

    with open(order_file) as f:
        for line in f:
            order = line.strip().split(",")
            chronogram = ultrametricer(order,species_tree)
            print(chronogram)


if __name__ == "__main__":

    if len(sys.argv) != 3:
        print ("usage: python ultrametrice.py tree_file order_file")
        exit(0)

    scr, species_tree, order_file = sys.argv
    ultrametrice(species_tree, order_file)
