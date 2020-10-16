import sys
import os

def parse_transfers(mypath):

    myfiles = [x for x in os.listdir(mypath) if x.endswith("uTs")]
    for myfile in myfiles:
        with open(os.path.join(mypath, myfile)) as f:
            f.readline()
            for line in f:
                print(myfile + "\t" + line.strip())

if __name__ == "__main__":

    if len(sys.argv) != 2:
        print ("usage: python parse_transfers.py folder_with_uTs_files")
        exit(0)

    scr, mypath = sys.argv
    parse_transfers(mypath)
