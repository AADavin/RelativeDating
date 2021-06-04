import sys
import os
_, mcl_output,protein_file, output_folder, max_size = sys.argv

def fasta_parser(myfile):
    with open(myfile) as f:

        header = ""
        seq = ""
        for line in f:
            if line[0] == ">":
                if seq != "":
                    yield (header[1:], seq)
                    header = line.strip()
                    seq = ""
                else:
                    header = line.strip()
            else:
                seq += line.strip()
        yield (header[1:], seq)

h2seq = dict()
for h, seq in fasta_parser(protein_file):
    h2seq[h] = seq
index = 0

with open(mcl_output) as f:
    for l in f:
        index += 1
        hs = l.strip().split("\t")
        if len(hs) < 4:
            continue           
        if len(hs) >= max_size:
            continue
        myseqs = list()
        for h in hs:  
            myseqs.append((h,len(h2seq[h])))
            # Compute the median of the fmamily!!!
         


        with open(os.path.join(output_folder,"Gf%s" % str(index) + ".faa"), "w") as f1:
            for h in hs:
                f1.write(">"+h+"\n")
                f1.write(h2seq[h]+"\n")
              
