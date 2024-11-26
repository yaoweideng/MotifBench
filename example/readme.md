# Example scaffold set and results

We here provide scripts used for running RFDiffusion on the benchmark problems.

RFdiffusion requires the specification of a "contig" that describes the placement of the sequence-contiguous motif segments in the scaffold to be generated.
This choice of contig can have significant implications on the scaffolds that it generates.
For motifs problems that were part of the earlier RFdiffusion benchmark set, we adopt the contig used there.
These 13 problems are 1BCF, 2KL8, 4JHW, 5IUS, 5YUI, 5WN9, 6E6R, 7AD5, 7AHO, 7BNY, 7DGW, 7MQQ, 7WRK.

For the problems with one segment we chose the contig to place no limits on the size of the flanking regions. 
These problems are 1LDB and 1ITU.

For the remaining problems we chose contigs that specified order of segments in the reference structure and included gaps between segments of at least 10 residues that spanned the gap in the reference structure between the associated segments.
