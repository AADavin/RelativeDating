import ete3
import sys
import itertools
import copy

# This scripts generates all the possible orders for a given tree
# We name the inner nodes if required

def name_nodes(mytree):
    i=0
    for node in mytree.traverse():
        if node.is_leaf() == False:
            i+=1
            node.name = str(i)

def partitions(n, k):
    for c in itertools.combinations(range(n+k-1), k-1):
        yield [b-a-1 for a, b in zip((-1,)+c, c+(n+k-1,))]

def is_inner_node(node):
    children = node.get_children()
    if not children[0].is_leaf() and not children[1].is_leaf():
        return True
    else:
        return False

def return_type_node(node):

    # 3 Real inner node with no leaf descedents
    # 2 Inner node with one leaf descendant
    # 1 With two leafes descendents


    children = node.get_children()
    if not children[0].is_leaf() and not children[1].is_leaf():
        return 3
    else:
        if (children[0].is_leaf() and not children[1].is_leaf()) or (not children[0].is_leaf() and children[1].is_leaf()):
            return 2
        else:
            return 1

# First thing we count the number of inner nodes under each node.
# We write for every inner node the number of partitions

def write_partitions(mytree):
    all_partitions = list()

    for node in mytree.traverse(strategy="postorder"):

        if node.is_leaf():
            continue


        node.add_feature("order",list())

        if is_inner_node(node):
            children = node.get_children()
            left_branch =  len(children[0].get_leaves())
            right_branch =  len(children[1].get_leaves()) - 1

            # This line stores the node and the corresponding partitions:

            all_partitions.append([node.name + ";" + ",".join([str(x) for x in p]) for p in partitions(right_branch,left_branch)])

    return all_partitions


def get_node_order(node, boxes):
    children = node.get_children()
    if children[0].is_leaf():
        node.order = list(children[1].order)
        node.order.insert(0, node.name)

    elif children[1].is_leaf():
        node.order = list(children[0].order)
        node.order.insert(0, node.name)

    else:
        # This is the general case where we are dealing with an inner node. Here we need information
        # relative to the partitions
        myorder = list(children[0].order) # We use the left node as a mold
        # And now we insert the other nodes onto that list
        # For that we iterate on the partitions
        counter = 0 # We count how many nodes of the right branch we have inserted
        balls_number = len(children[1].order)

        if node.is_root():
            pass
        while counter < balls_number:
            true_index = 0

            for index, box in enumerate(boxes):

                if box == "0":
                    pass
                else:
                    for x in range(int(box)):
                        if true_index < len(myorder):
                            myorder.insert(true_index, children[1].order[counter])
                        else:
                            myorder.append(children[1].order[counter])
                        true_index+=1
                        counter += 1
                true_index +=1
        myorder.insert(0,node.name)
        node.order = myorder

def generate_node_orders(all_partitions):

    for element in itertools.product(*all_partitions):

        # Now we translate the code into orders:

        tree = copy.deepcopy(mytree)
        root = tree.get_tree_root()

        mypartitions = dict()

        for partition in element:
            node, boxes = partition.split(";")
            mypartitions[node] = boxes.split(",")

        # Now we iterate the tree filling the node orders


        for node in tree.traverse(strategy="postorder"):

            if node.is_leaf():
                continue

            node_type = return_type_node(node)

            if node_type == 1:
                node.order.append(node.name)

            elif node_type == 2:
                get_node_order(node, None)

            elif node_type == 3:

                get_node_order(node, mypartitions[node.name])

        # Now we get the node orders of the tree

        print (",".join(root.order))


def test_tree():
    all_partitions = write_partitions(mytree)
    generate_node_orders(all_partitions)


if __name__ == "__main__":

    if len(sys.argv) != 2:
        print ("usage: python generate_orders.py mytree")
        exit(0)

    scr,mytree_file = sys.argv

    with open(mytree_file) as f:
        mytree = ete3.PhyloTree(f.next().strip(), format=1)

    all_partitions = write_partitions(mytree)
    generate_node_orders(all_partitions)
