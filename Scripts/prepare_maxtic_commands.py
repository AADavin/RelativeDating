import os
import sys


def prepare_maxtic_commands(path, tree):
    
    maxticpath = os.path.dirname(os.path.abspath(__file__)) 
    reps = [x for x in os.listdir(path) if "Replicate" in x]
    mpath = "python MaxTiC.py TREE REP rep_numb"
    for rep in reps:
        rep_numb = rep.split("_")[-1].split(".")[0]
        print("python %s/MaxTiC.py %s %s %s" % (maxticpath,tree,rep,rep_numb))

if __name__ == "__main__":

    if len(sys.argv) != 3:
        print("usage: python prepare_maxtic_commands.py path tree")
        exit(0)

    _, path, tree = sys.argv
    prepare_maxtic_commands(path, tree)
