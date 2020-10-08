# Relative Dating
Copyright © 2020, Adrián A. Davín. Released under the MIT license.

## A very brief introduction

We know very little about the history of life. Unfortunately, just a tiny fraction of all living beings that have ever lived on this planet have left a trace in the fossil record. The problem is especially acute in the case of prokaryotes, the most diverse and abundant life beings, for which just a handful of recognizable fossils have survived and carry very little information about their lifestyles.
Luckily for us, we do have access to the genomes of living organisms and by analysing and comparing them we can say many things about how life has evolved. 

In prokaryotes, the process of Lateral Gene Transfers (also known as Horizontal Gene Transfers, LGT or HGT for short) consist on cells incoroporting in their own genomes fragments of genomic material from different cells. These events can be inferred by studying the genomes of their descendants and carry a very valuable information: a LGT beween two organisms tells us that those cells coexisted in the past. 

In Gene transfers can date the tree of life, we showed (https://www.nature.com/articles/s41559-018-0525-3) how we can detect transfers and how they carry time information. In this GitHub repository you can find some scripts and tools useful to perform a relative dating analysis

## Evolution and trees

Evolution is most commonly represented using trees. These trees can be used to illustrate how different entities (cells, species, populations, genes, etc) diverge over time from a common ancestor. There has been a ton of discussion (sometimes quite heated) over the validity of using trees and not networks to represent evolution. My take on this is that when we are dealing with entities that do "mix" or "recombine" over time (to a significant extent), a network (with a vertical component) is the *correct* representation. However, that does not mean that using tree-based techniques we cannot obtain meaningful results

In the case of prokaryotic evolution there are two different layers of evolution we have to study. The first one is the tree of species, that represents how different lineages of prokaryotic diverge over time. The second one is the tree of genes, that represent, for a given gene family (all sequences that share a common ancestor), how the gene has been evolving and *moving* inside the gene tree.

## How do we know that a gene has been transferred in the past?

There are several ways to infer LGT, but the most powerful one is called phylogenetic reconciliation.
The (only) way to understand phylogenetic reconciliations is by having first a clear image of how cells evolve and genes evolve inside them

For instance, in the picture we have a gene evolving a species tree with 4 species. The species tree is represented by the wider tree (in black). The gene tree is inside the species tree. There is a transfer event (indicated by the horizontal line), going from linage n1 to the ancestor lineage of n3 and n4. The ancestor of n3 and n4 has two homologous copies of the gene after the transfer event (the second copy is represented in blue). 

<p align="center">
  <img src="/Images/Figure1.png">
</p>

If we had a magical crystal ball or a time machine we could see evolution happening with this level of detail, but sadly, we are not there yet. The best we have is the sequences in the genomes of the extant species (in the example: n1,n2,n3 and n4), that we can read and then infer the trees by using different phylogenetic techniques.

The data that we can recover from the previous example would look like:

<p align="center">
  <img src="/Images/Figure2.png">
</p>        

LGT can be inferred using a set of techniques called *phylogenetic reconciliations*. 

##

##




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

### generate_orders.py

**Usage**: python generate_orders.py tree.nwk

**Output**: Prints to stdoutput the trees, in newick format, of all possible node arrangements

### ultrametrice.py 

**Usage**: python ultrametrice.py tree.nwk order.txt

The file order.txt must contain the name of the inner nodes of the tree.nwk in the format Root,node1,node2,node3

**Output**: Prints to the stdouput an ultrametric tree where the inner nodes are ordered according to the file order.txt

