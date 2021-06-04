#!/bin/bash

## Input is proteinortho output tsv file with added first column of GeneID

if [ $# -ne 2 ]
then
	echo -e "\nUsage: $0 <proteinortho filtered file (removed)> <cdbfasta-indexed all proteins/genes file>\n"
	exit 0
fi


grep -v "#" $1 | cat -n | sed -e 's/^[ \t]*//' | awk '{ print "OrthoGroup"$0"" }' | sed 's/\t/,/g' | sed 's/,/\t/1' | sed 's/,/\t/1' | sed 's/,/\t/1' | sed 's/,/\t/1' > list
/srv/sw/cdb/fasta/cdbfasta $2

cut -f1,5 list > list2

while read line1 line2
do
	echo $line2 | sed 's/,/\n/g' > tmp
	cat tmp | /srv/sw/cdb/fasta/cdbyank $2.cidx > "$line1".fasta
	rm tmp 
done < list2
