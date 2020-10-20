# Relative Dating
Copyright © 2020, Adrián A. Davín. Released under the MIT license.

This GitHub repository contains a gentle introduction to relative dating with Lateral Gene Transfer and some scripts that might be useful to those interested in performing their own analyses. It assumes a very basic understanding of phylogenetics (i.e. what is a gene tree).
## A very brief introduction
***

Dating is difficult. Dating prokaryotes is really difficult. The faint trace that prokaryotes have left in the fossils record does not allow us to properly place them in the context of a phylogeny (i.e. identifying the extant relatives of the fossil) nor using the most standard dating methods (such as radiometric dating).

Luckily for us, we can access now the information contained in the genomes of extant living prokaryotes and infer from there the occurrence of LGT that took place a long time ago (potentially billions of years). These transfers also can be used to date those lineages, in a **relative manner**: a transfer can tell us the order of diversification, e.g. A diverged before than B.

If you want a more detailed description of the process you can read our paper on relative dating [here](https://www.nature.com/articles/s41559-018-0525-3)


## How do we know that a gene has been transferred in the past?
There are several ways to infer LGT, but the most powerful one is called phylogenetic reconciliation. The (only) way to understand phylogenetic reconciliations is by having first a clear image of how cells evolve and genes evolve inside them
It is good to begin by having a clear picture on how the process we are studying affect 
For instance, in the picture we have a gene evolving a species tree with 4 species. The species tree is represented by the wider tree (in black). The gene tree is inside the species tree. n1,n2,n3,n4 are the name of the leaves (i.e the extant species), and the inner nodes (Root, a, b) correspond to speciation events. In phylogenetics we refer to the different branches of the tree by the name of the final node, e.g n1 is both the extant organism and the branch leading to n1. It should be obvious by the context when I am referring to the speciation node or to the branch, but I will be as explicit as possible to avoid confusion.
There is a transfer event (indicated by the horizontal line), going from the branch n1 to the ancestor lineage of n3 and n4. The ancestor of n3 and n4 has two homologous copies of the gene after the transfer event (the second copy is represented in blue).
 
<p align="center">
  <img src="/Images/Figure1.png">
</p>
 

If we had a magic crystal ball or a time machine we could see evolution happening with this level of detail, but we are not there yet. The best we have is the sequences in the genomes of the extant species (in the example: n1,n2,n3 and n4), that we can read and then infer the trees by using different phylogenetic techniques.
The data that we can recover from the previous example would look like:
 
<p align="center">
  <img src="/Images/Figure2.png">
</p>

The challenge is going from those two trees to something that tells us:
There has been a transfer between the branch leading to n1 to the immediate ancestor of n3 and n4
The way we do that is using a technique called "phylogenetic reconciliation"
## Phylogenetic reconciliations
***
This is a relatively old technique ([the first one published in 1979](https://www.jstor.org/stable/2412519?seq=1#metadata_info_tab_contents)) that consist of mapping two trees. You can imagine this as the process of explaining the topology of one tree (the gene tree) based on the topology of a second tree (the species tree) and a series of events, such as duplications, transfers and losses. 
In a reconciliation, transfer events will be mapped on the species tree, such as:
<p align="center">
  <img src="/Images/Figure3.png">
</p>

 
The exact moment of the transfer cannot be inferred with the currently existing techniques. The best we can do is obtaining something like:
<p align="center">
  <img src="/Images/Figure4.png">
</p>
Or
n1 --> b
We don't know when the gene left n1, but it did at some point along the branch. We don't know when the gene arrived to b, but it occurs sometime across the length of the branch

## Transfers can be transformed into constraints
***

Assuming that we are correctly inferring the transfer in the correct species tree, we could say that those two lineages (the donor and the recipient of the transfer) had to coexist in the past.
Right?
Not so fast. This assumes that the transfers occur between those two lineages that are in the tree without any intermediates that might be not in the tree. Some of them could be unsampled species, some of them could even be extinct lineages. In fact, the gene could leave the donor much before the gene is acquired by the recipient lineage.
 
We can see that very clearly in the next example, that represents the full evolutionary history of a group of organisms of which one of them goes extinct (n9)
 
<p align="center">
  <img src="/Images/Figure5.png">
</p>

 
We do not retrieve the genome of n9 in the past, and the species tree + the transfer we can infer looks like:
<p align="center">
  <img src="/Images/Figure6.png">
</p>

The branches b and c from the figure where we can see n9 going extinct are collapse into one. In the reconciliation analysis, we effectively see the transfer leaving the branch b+c. But, **b+c are not contemporary to a**:
<p align="center">
  <img src="/Images/Figure7.png">
</p>

What we can say just by looking at the reconciliation is that the donor lineage appeared before the recipient lineage "disappeared". In our example, the branch **b+c** appears with speciation **d** and the branch **a** disappears with speciation **a**.
The simplest way to put that is:
> A transfer implies a constraint between two nodes. The parent node of the donor must be older than the descendant node of the recipient.
 
Or even simpler:
 
> node d is older than node a
 
## There are many ways to order the speciations in a tree
***

Now we understand why a transfer can give the relative order of two nodes. In relative dating we just try to order the speciation nodes of the tree. The total number of possible orders (or speciation rankings) depends on the number of leaves and the topology of the tree. For instance, a caterpillar tree has one possible order:
<p align="center">
  <img src="/Images/Figure8.png">
</p>

We give the order beginning with the root and moving towards the leaves. 
The order is obviously Root,a,b
However, a tree with 4 species completely balanced (the other possible topology for 4 species), has two possible orders:
<p align="center">
  <img src="/Images/Figure9.png">
</p>

The number of possible orders grows very quickly. You can count the possible total orders of a tree using the script count_orders.py
## There are many transfers

***
A single transfer constraints two nodes. This affects obviously at all the ancestor nodes of the donor, that will be older than all the descendants nodes of the recipients.
In prokaryotes, there are normally many transfer events, some more recent, some older. If we are able to infer many transfers, we might not be able to obtain the true speciation ranking of all nodes in a tree, but we can constrain their position to a potentially narrow interval.
## Some transfers do not carry dating information
***
Transfers arriving to the leaves do not carry time information, because leaves have no descendant nodes.
<p align="center">
  <img src="/Images/Figure10.png">
</p>

Transfers from ancestors to descendants carry not information, because the constraint that they imply is always forced by the topology of the tree (it is possible in theory to have a gene being transferred from an ancestor to a descendant, think of a gene that leaves the tree in time 1, evolves outside a different lineage and then comes back to a descendant of the 
original donor). Transfer from a linage to its sister lineage also imply constraints that are not informative, since this constraints are always respected, imposed by the topology of the ree
<p align="center">
  <img src="/Images/Figure11.png">
</p>
 

## Some transfers can be falsely inferred
***
If the inference was perfect this would not be a concern, but, as any phylogenetic practitioner knows, many things can go wrong at different steps in the pipeline. Sometimes we detect transfers that are not correct: maybe the direction of the transfer is wrong, maybe the donor or the recipient are not the correct ones. This means that some transfers might imply constraints in the tree that are false, and some of them might be even contradictory (for instance, a transfer implies a older than b, and a second transfer implies than b is older than a)
Two transfers are time-incompatible if they imply constraints that can not be respected in the same tree:
<p align="center">
  <img src="/Images/Figure12.png">
</p>

 
## Filtering false transfers
***
We found that the best way to deal with having false transfers is selecting the maximum set of time-compatible transfers. This problem is NP-complete, so we cannot guarantee, for most datasets (even for relatively small ones), that we find the best possible solution. Luckily for us, there are some algorithms that can deal with this problem obtaining trees that are "good enough" and probably very close to the absolute maximum. The algorithm we used is based on dynamic programming and is called [MaxTiC](https://hal.archives-ouvertes.fr/hal-01532738v3/document).
<p align="center">
  <img src="/Images/Figure13.png">
</p>

 
In the above figure, there are multiple transfers supporting the constraint
f > a
And a single constraint (the purple transfer), supporting
a > f
The MaxTiC algorithm in this case will simply:
 
 
Remove that constraint (we think it has been falsely inferred)
<p align="center">
  <img src="/Images/Figure14.png">
</p>


## Sampling speciation rankings
***

A limitation of the MaxTIC algorithm is that it produces a single set of constraints. Some of those constraints might not even be very well supported by many families. To obtain a more robust measure we developed a slightly more complex pipeline.
Instead of doing the MaxTiC analysis once, you can bootstrap the gene families N times, and then run the MaxTiC in the constraints coming from each replicate.

Then, you measure the support of every constraint by counting on how many replicates the constraint appears. We select only those constraints that appear on 95 or more of the replicates.

Then, we can use those constraints and the script order_sampler.py to produce a distribution of trees compatible with those highly supported constraints

The way that order_sampler work is by taking a node at a time, and then moving it to a random position, respecting the topology of the tree and the current speciation ranking. For example:

<p align="center">
  <img src="/Images/Figure15.png">
</p>



In the figure, we see how the order_sampler took the node c (the last speciation on the left) and made it a few steps older. 

Running this algorithm for many steps effectively mixes the speciation ranking and produces a distribution of ranked trees. The algorithm has a temperature component, that can be used to explore order that might be potentially conflicting with the given constraints imposed by MaxTiC. Setting a very low temperature will prevent this from happening.

## Pipeline
***
You will need to install the ete3 library to use some of the scripts
#### Obtaining transfers
1. Infer a Species Tree
2. Infer Gene Trees 
3. Reconcile them both with an undated reconciliation algorithm. I use ALE undated. This produces several files. The files that you need are the ones ending with uTs. They contain three columns with the donor of the transfer, the recipient and the support of the transfer.
#### Obtaining a single MaxTiC Tree
***
 
1. Compute reconciliations using ALEml_undated. Store all the uTs files in the same folder
2. Parse all the transfers and put them on the same file:
python parse_transfers.py folder_with_uTs > AllTransfers.tsv
3. Filter those transfers with a weight less to 0.05:
         awk -F ‘\t’ ‘$3 >= 0.05’ AllTransfers.tsv > AllTransfersFiltered.tsv
4. You need the species tree in a file. The species tree must have its inner nodes named  using the same way that ALE does. The easiest way is just take a random reconciliation (the uml_rec file), and get the tree from there. A short command to that is:
head -3 your_reconciliation.ale.uml_rec | tail -1 | cut -f 2 > RefTree.nwk
5. Transform the transfers into constraints:
python get_constraints.py RefTree.nwk AllTransfersFiltered.tsv > AllConstraints.tsv	
6. Launch MaxTiC:
python MaxTiC.py RefTree.nwk AllConstraints.tsv Analysis1
MaxTiC will generate different files:
           MaxTiCTree.nwk - A tree compatible with the MaxTiC set of constraints
 
#### Obtaining a distribution of relative-dated trees
***

1. Compute reconciliations using ALEml_undated. Store all the uTs files in the same folder
2. Parse all the transfers and put them on the same file:
    python parse_transfers.py folder_with_uTs > AllTransfers.tsv
3. You need the species tree in a file. The species tree must have its inner nodes named  using the same way that ALE does. The easiest way is just take a random reconciliation (the uml_rec file), and get the tree from there. A short command to that is: head -3 your_reconciliation.ale.uml_rec | tail -1 | cut -f 2 > RefTree.nwk
4. Bootstrap the transfers: This script automatically filters transfers smaller than 0.05 and converts the transfers to constraints
python bootstrap_transfers.py AllTransfers.tsv RefTree.nwk 100
5. Get the commands to run maxtic
python prepare_maxtic_commands.py folder_with_the_replicates RefTree.nwk > coms
6. Run MaxTiC, once for each Replicate
parallel -j n_of_threads < coms 
7. Parse the bootstrapped result
python read_bootstrap.py ./ > ResultsBootstrap.tsv
8. Get those that appear in at least 95 of the replicates:
awk -F "\t" '$3 >= 95 {print $1,$2,$3}' OFS="\t"  ResultsBootstrap.tsv > HighSupportConstraints.tsv
9. Run MaxTiC on those constraints
python MaxTiC.py RefTree.nwk HighSupportConstraints.tsv Global
10. Run the order explorer with a very low temperature (use the MaxTiC tree as the departure point!):
python order_explorer.py -tree Global_MaxTiCTree.nwk -constraints HighSupportConstraints.tsv -T 0.00000000000000000000000000001 -f 1000 -o Orders
By default order_explorer runs 10^6 cycles. You can sample every 1000th cycle (-f option) to get 1000 node orders compatible with the constraints.
## Scripts
***
#### count_orders.py
**Usage**: python count_orders.py tree.nwk
 
**Output**: Prints to stdoutput the number of possible node arrangements
#### bootstrap_transfers.py

**Usage**: python bootstrap_transfers.py AllTransfers.tsv RefTree.nwk 100
 
**Output**: Creates a given number of replicates (100 in the example), to perform a bootstrap analysis on the transfers
#### get_node_order.py
**Usage**: python get_node_order.py tree.nwk
 
**Output**: Prints to stdoutput the node order of the given tree. For instance, using this tree:
Would produce:
Root,a,b

#### generate_orders.py
**Usage**: python generate_orders.py tree.nwk
 
**Output**: Prints to stdoutput the different trees with the different orders
#### MaxTiC.py
**Usage**: python MaxTiC.py RefTree.nwk AllConstraints.tsv Name


**Output**: It producs a MaxTiC tree, and return a MaxTiC set of constraints
#### order_explorer.py
**Usage**: python order_explorer.py -tree MaxTiCTree.nwk -constraints ConstraintsFile.tsv -o Analysis

**Output**: It two different files: A log file with all the orders sampled, the conflict (weight of constraints conflicting with a give node order) and a tree with the best score.
#### read_bootstrap.py
**Usage**: python read_bootstrap.py ./ > ResultsBootstrap.tsv


**Output**: It outputs to the stdoutput 4 columns: Donor, Recipient, Number of times that the constraint has been found,  Total weight of constraints
#### parse_transfers.py

**Usage**: python parse_transfers.py folder_with_uTs > AllTransfers.tsv
The folder contains the uTs files output by ALE_undated
 
**Output** It will store in a single file all the outputs in the format:
Family  Donor  Recipient  Weight
The weight is the posterior probability of the transfer inferred by ALE undated
#### prepare_maxtic_commands.py

**Usage**: python prepare_maxtic_commands.py folder_with_the_replicates RefTree.nwk
 
**Output**: It prints the commands that you can use then to run MaxTiC. 
#### ultrametrice.py
**Usage**: python ultrametrice.py tree.nwk order.txt
The file order.txt must contain the name of the inner nodes of the tree.nwk in the format Root,node1,node2,node3
 
**Output**: Prints to the stdouput an ultrametric tree where the inner nodes are ordered according to the file order.txt
 


