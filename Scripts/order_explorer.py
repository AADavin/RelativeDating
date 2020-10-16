import ete3
import copy
import argparse
import math
import random

def ultrametricer(node_order, tree_file):

    with open(tree_file) as f:
        mytree = ete3.Tree(f.readline().strip(), format=1)

    # First I get every single leaf

    leaves = mytree.get_leaves()

    # The total distance must be

    v = len(leaves)

    # Now we get the expected distances
    distances = dict()
    for i, node in enumerate(node_order):
        distances[node] = i + 1

    for node in leaves:
        distances[node.name] = v

    # We add the root (that has no name)
    distances[""] = 0

    # We get the root

    root = mytree.get_tree_root()

    for node in leaves:
        # Now I start traversing to the root

        while (node.up):
            # The expected distance of this branch is:
            expected = distances[node.name] - distances[node.up.name]
            node.dist = expected
            node = node.up

    return mytree.write(format=1, format_root_node = True)


def get_order(tree):

    mytree = ete3.Tree(tree, format=1)
    distances = dict()

    for mynode in mytree.traverse():
       if mynode.is_leaf():
           continue
       one_leaf = mynode.get_leaves()[0]
       dist = mynode.get_distance(one_leaf)
       distances[mynode.name] = dist

    node_order = sorted(distances.items(), key=lambda x: x[1])
    node_order = [x[0] for x in node_order][::-1]
    return node_order

def get_parents(tree_file):
    with open(tree_file) as f:
        mytree = ete3.Tree(f.readline().strip(), format=1)

    parents = {node.name: node.up.name for node in mytree.iter_descendants() if node.is_leaf() == False}
    parents[mytree.get_tree_root().name] = None

    return parents


def get_children(tree_file):
    with open(tree_file) as f:
        mytree = ete3.Tree(f.readline().strip(), format=1)

    children = {node.name: [x.name for x in node.get_children() if x.is_leaf() == False] for node in mytree.traverse()
                if node.is_leaf() == False}

    return children


def propose_order(parents, children, order):

    proposed_order = copy.deepcopy(order)
    direction = ""
    distance = 1

    while distance <= 1:
        if random.random() <= 0.5:
            # We push towards the root

            mynode = random.choice(proposed_order[1:])  # We take one node at random (not the root)
            myindex = proposed_order.index(mynode)  # We retrieve his index
            myparent = parents[mynode]
            myparentindex = proposed_order.index(myparent)
            direction = "R"
            distance = myindex - myparentindex

        else:

            # We push towards the leaves

            mynode = random.choice(proposed_order[1:])  # We take one node at random (not the root)
            myindex = proposed_order.index(mynode)  # We retrieve his index
            mychildren = children[mynode]

            if len(mychildren) == 0:
                # Then I am just limited by the end of the list
                child1index = len(proposed_order) - 1
                direction = "L"
                distance = child1index - myindex

            elif len(mychildren) == 1:

                child1index = proposed_order.index(mychildren[0])
                direction = "L"
                distance = child1index - myindex

            elif len(mychildren) == 2:

                child1index, child2index = proposed_order.index(mychildren[0]), proposed_order.index(mychildren[1])
                direction = "L"
                distance = min((child1index - myindex, child2index - myindex))

    if direction == "R":
        mynewindex = myindex - random.randint(1, distance - 1)
        proposed_order.insert(mynewindex, mynode)
        proposed_order.pop(myindex + 1)

    if direction == "L":
        mynewindex = myindex + random.randint(1, distance - 1)
        proposed_order.insert(mynewindex, mynode)
        proposed_order.pop(myindex)

    return proposed_order


def myround(n):
    return float(str(n)[0:5])

# This is a function that takes a tree, a node and a scale parameter and return the scaled tree


def compute_conflict(node_order, constraints):
    conflict = float()
    ranking = {node: rank for rank, node in enumerate(node_order)}
    for dn, rcs in constraints.items():
        for rc, wt in rcs.items():
            if ranking[dn] > ranking[rc]:
                conflict += wt
    return conflict


def get_constraints(constraints_file):
    constraints = dict()
    total_w = float()

    with open(constraints_file) as f:

        for line in f:



            try: _, dn, rc, wt = line.strip().split("\t")
            except:
                try: dn, rc, wt, _ = line.strip().split(" ")
                except:
                    dn, rc, wt = line.strip().split("\t")


            if dn not in constraints:
                constraints[dn] = dict()

            if rc not in constraints[dn]:
                constraints[dn][rc] = 0.0

            constraints[dn][rc] += float(wt)
            total_w += float(wt)

    return (constraints, total_w)


def write_log(outfile, cycle, order, conflict, total_w):
    with open(outfile, "a") as f:
        myorder = ",".join(order)
        line = "\t".join([str(cycle), str(conflict), str(conflict / total_w), myorder]) + "\n"
        f.write(line)


def get_node_order(tree_file):
    with open(tree_file) as f:
        mytree = ete3.Tree(f.readline().strip(), format=1)

    distances = dict()

    for mynode in mytree.traverse():

        if mynode.is_leaf():
            continue

        one_leaf = mynode.get_leaves()[0]
        dist = mynode.get_distance(one_leaf)
        distances[mynode.name] = dist

    node_order = sorted(distances.items(), key=lambda x: x[1])
    node_order = [x[0] for x in node_order][::-1]

    return node_order


def order_explorer(tree_file, constraints_file, n_cycles, T, freq, stopping, annealing, output):

    best_tree = output + "_" + "BestTree"

    #orders_file = output + ".orders"

    #with open(orders_file, "w") as f:
    #    pass

    log_file = output + "_" + "Log.tsv"

    with open(log_file, "w") as f:

        header = "\t".join(["Cycle", "Conflict", "Normalized_conflict", "Order"]) + "\n"
        f.write(header)

    best_solution = 1

    constraints, total_w = get_constraints(constraints_file)

    parents = get_parents(tree_file)
    children = get_children(tree_file)

    with open(tree_file) as f:
        mycurrenttree = ete3.Tree(f.readline().strip(),format=1)
        inner_nodes = [node.name for node in mycurrenttree.iter_descendants() if node.is_leaf() == False]
        mycurrenttree = mycurrenttree.write(format=1, format_root_node=True)

    mynode_order = get_node_order(tree_file)
    myconflict = compute_conflict(mynode_order, constraints)

    last_acceptance_ratio = 0
    cycle = 0

    print("### Node ranking explorer ### ")
    print("Total weight of constraints is %s" % str(total_w))
    print("Orders will be saved in %s" % orders_file)
    print("Log will be saved in %s" % log_file)
    print("Best Tree will be saved in %s" % best_tree)
    print("Running %s cycles. Sampling 1 out of %s trees" % (n_cycles,freq))
    print("Temperature set at %s. " % T)
    print("Annealing set as %s" % str(annealing))

    stack_size = len(mynode_order) * 10
    accepted_changes = [0 for x in range(stack_size)]
    # This is a stack with a size proportional to the tree

    #if annealing == 1:#

    #    print("Setting temperature to 0.1 percent total weight of Transfers: %s" % str(total_w/1000))
    #    print("To avoid this, do not use annealing")
    #    T = total_w / 1000


    while cycle < n_cycles:

        cool_down = False

        if myconflict <= stopping:
            print("Conflict went below the treshold limit")
            break

        if annealing and cycle >= 1000: # To have some burning

            acceptance_ratio = sum(accepted_changes) / float(len(accepted_changes))

            if cycle % int(freq / 10) == 0:
                print("Acceptance ratio of last %s cycles is %s" % (str(len(accepted_changes)), str(acceptance_ratio)))

                # PD

                derivative = acceptance_ratio - last_acceptance_ratio

                if acceptance_ratio >= 0.30 and derivative >= 0:
                    T = T * (1 - (acceptance_ratio - 0.3)) * (1 - derivative)
                    print("New temperature is %s" % str(T))
                    cool_down = True

                elif cool_down == True and acceptance_ratio <= 0.20 and derivative <= 0:
                    T = T * (1 + abs((acceptance_ratio - 0.2))) * (1 + abs(derivative))
                    print("New temperature is %s" % str(T))


                #elif acceptance_ratio <= 20 and cooled_down == True:
                #  T = T * (1 - derivative)

            last_acceptance_ratio = acceptance_ratio


        proposed_order = propose_order(parents, children, mynode_order)

        newconflict = compute_conflict(proposed_order, constraints)

        if newconflict < best_solution:
            best_solution = newconflict

            with open(best_tree, "w") as f:
                line = str(newconflict) + "\t" + ",".join(proposed_order) + "\n"
                f.write(line)
                f.write(ultrametricer(proposed_order, tree_file))

        if newconflict < myconflict:

            mynode_order = proposed_order
            myconflict = newconflict

            accepted_changes.insert(0, 1)
            accepted_changes.pop()

            cycle += 1

        elif newconflict == myconflict:

            mynode_order = proposed_order
            myconflict = newconflict

            cycle += 1

        else:

            cutoff = math.exp((myconflict - newconflict) / T)

            if random.random() <= cutoff:

                accepted_changes.insert(0, 1)
                accepted_changes.pop()

                mynode_order = proposed_order
                myconflict = newconflict
                cycle += 1


            else:

                accepted_changes.insert(0, 0)
                accepted_changes.pop()

                cycle += 1

        if cycle % freq == 0:
            write_log(log_file, cycle, mynode_order, myconflict, total_w)
            print(cycle)

            #with open(orders_file, "a") as f:
            #    f.write(",".join(mynode_order) + "\n")


def test_propose_order():
    mytree = "/Users/aadavin/Desktop/ClocksAndTransfers/SpeciesTree/RefTrees/CyanoTree"
    parents = get_parents(mytree)
    myorder = [str(x) for x in
               [78, 77, 76, 64, 72, 75, 69, 74, 73, 67, 60, 71, 65, 44, 68, 56, 61, 45, 47, 59, 70, 41, 57, 62, 66, 58,
                46, 63, 43, 52, 55, 53, 50, 48, 40, 51, 49, 42, 54]]
    print(myorder)
    print(propose_order(parents, myorder))


def test_get_conflict():
    tree_file = "/Users/aadavin/Desktop/ClocksAndTransfers/SpeciesTree/RefTrees/CyanoTree"
    constraints_file = "/Users/aadavin/Desktop/ClocksAndTransfers/FamiliesInformation/Transfers/Cyano_Constraints_0.4_8_0.25.tsv"
    # node_order = get_node_order(tree_file)
    node_order = ['78', '77', '72', '60', '69', '44', '76', '67', '65', '56', '61', '59', '62', '41', '42', '45', '43',
                  '46', '54', '75', '74', '64', '40', '55', '70', '73', '57', '66', '71', '58', '47', '68', '51', '49',
                  '63', '52', '53', '50', '48']
    constraints, total_w = get_constraints(constraints_file)
    print(node_order)
    print(total_w)
    print(compute_conflict(node_order, constraints) / total_w)

    t = float()
    with open(constraints_file) as f:
        for line in f:
            t += float(line.strip().split("\t")[-1])
    print(t)


if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument("-output", "--o", help="output of the MC")
    parser.add_argument("-tree", "--t", help="starting tree")
    parser.add_argument("-constraints", "--c", help="constraints file")
    parser.add_argument("-n", "--n", help="number of cycles, default to 10^6", default=1000000)
    parser.add_argument("-T", "--T", help="Temperature of the chain, default = 1.0", default=1.0)
    parser.add_argument("-f", "--f", help="frequency of sampling, default = 10", default=10)
    parser.add_argument("-s", "--s", help="Stop chain when conflict goes below this, default = -1", default=-1)
    parser.add_argument("-a", "--a", help="Annealing. Default False", default=False)

    args = parser.parse_args()

    if args.t == None:
        print("use python order_explorer.py -h to see options")
        print("you can run this script just with python order_explorer -tree yourtreefile -constraints yourconstraints -o name of the output chain")
        exit(0)

    order_explorer(args.t, args.c, int(args.n), float(args.T), int(args.f), float(args.s), float(args.a), "./" + args.o)

