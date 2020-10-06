# Relative Dating

We know very little about the history of life. Unfortunately, just a tiny fraction of all living beings that have ever lived on this planet have left a trace in the fossil record. The problem is especially acute in the case of prokaryotes, the most diverse and abundant life beings, for which just a handful of recognizable fossils have survived and carry very little information about their lifestyles.
Luckily for us, we do have access to the genomes of living organisms and by analysing and comparing them we can say many things about how life has evolved. 

In prokaryotes, the process of Lateral Gene Transfers (also known as Horizontal Gene Transfers, LGT or HGT for short) consist on cells incoroporting in their own genomes fragments of genomic material from different cells. These events can be inferred by studying the genomes of their descendants and carry a very valuable information: a LGT beween two organisms tells us that those cells coexisted in the past. 

In Gene transfers can date the tree of life, we showed (https://www.nature.com/articles/s41559-018-0525-3) how we can detect transfers and how they carry time information. In this GitHub repository you can find some scripts and tools useful to perform a relative dating analysis

## Scripts

You will need to install the ete3 library to use most of the scripts

### get_node_order.py

**Usage**: python get_node_order.py tree.nwk

**Output**: Prints to stdoutput the node order of the given tree. For instance, using this tree:

![Tree 1](/Images/Tree1.png)

Would produce:

Root,a,b

### count_orders.py

**Usage**: python count_orders.py tree.nwk

**Output**: Prints to stdoutput the number of possible node arrangements

![Tree orders](/Images/TreeCountOrders.png)

The number of total arrangements depends on the topology of the tree. In the figure, we see that a tree with 4 leaves and that particular topology has a total of 2 possible node arrangements (Root,a,b and Root,b,a). 











