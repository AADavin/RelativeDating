import sys
import os
import random
import ete3

def bootstrap_transfers(transfers_file, tree_file, replicates):

    with open(tree_file) as f:
        mtree = ete3.Tree(f.readline().strip(),format=1)

    node2parent = dict()
    leaves = set()
    constraints = dict()

    for n in mtree.traverse():
        if n.is_root():
            node2parent[n.name] = "None"
        else:
            node2parent[n.name] = n.up.name
        if n.is_leaf():
            leaves.add(n.name)

    with open(transfers_file) as f:
        for line in f:
            fam, dn, rc, wt = line.strip().split("\t")
             
            if float(wt) < 0.05:
                continue            

            if "(" in dn:
                dn = dn.split("(")[0]
            if "(" in rc:
                rc = rc.split("(")[0]

            if fam not in constraints:
                constraints[fam] = dict()
            if node2parent[dn] == "None":
                continue
            if rc in leaves:
                continue
            dn_c = node2parent[dn]
            if dn_c not in constraints[fam]:
                constraints[fam][dn_c] = dict()
            if rc not in constraints[fam][dn_c]:
                constraints[fam][dn_c][rc] = 0.0
            constraints[fam][dn_c][rc] += float(wt)

    fam_number = len(constraints)
    print(fam_number) 
    for i in range(replicates):
        print("Constraints_Replicate_NUM.tsv".replace("NUM",str(i))) 
        with open("Constraints_Replicate_NUM.tsv".replace("NUM",str(i)), "w") as f:
            fams_sampled = random.choices(list(constraints.keys()), k = fam_number )
            for fam in fams_sampled:
                for dn_c in constraints[fam]:
                    for rc in constraints[fam][dn_c]:
                        mline = "\t".join([dn_c, rc, str(constraints[fam][dn_c][rc])])+"\n"
                        f.write(mline)


if __name__ == "__main__":

    if len(sys.argv) != 4:
        print("usage: python bootstrap_transfers.py transfers_file tree_file numer_of_replicates")
        exit(0)

    scr, transfers_file, tree_file, replicates = sys.argv
    bootstrap_transfers(transfers_file, tree_file, int(replicates))
