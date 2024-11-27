# Example scaffold set and results

We here provide scripts used for running RFDiffusion on the benchmark problems.

To generate the RFdiffusion scaffolds we followed the following steps.

### 1. Specified "contigs" in [contig_specifications.csv](./contig_specifications.csv)
RFdiffusion requires the specification of a "contig" that describes the placement of the sequence-contiguous motif segments in the scaffold to be generated.
This choice of contig can have significant implications on the scaffolds that it generates.
For motifs problems that were part of the earlier RFdiffusion benchmark set, we adopt the contig used there.
These 13 problems are 1BCF, 2KL8, 4JHW, 5IUS, 5YUI, 5WN9, 6E6R, 7AD5, 7AHO, 7BNY, 7DGW, 7MQQ, 7WRK.

For the problems with one segment we chose the contig to place no limits on the size of the flanking regions. 
These problems are 1LDB and 1ITU.

For the remaining problems we chose contigs that specified order of segments in the reference structure and included gaps between segments of at least 10 residues that spanned the gap in the reference structure between the associated segments.

### 2. Run RFdiffusion motif-scaffolding via apptainer and docker image
* We installed RFdiffusion using the docker image (see [readme](https://github.com/RosettaCommons/RFdiffusion?tab=readme-ov-file#docker)).
* We used generated SLURM scripts for each benchmark problem using [write_scripts_by_case.sh](./scripts/write_scripts_by_case.sh).  The script includes details of the exact RFdiffusion run commands.
* We ran these on a university compute cluster, [Sherlock](www.sherlock.stanford.edu).  Each script ran on a single GPU, of which the model varied.  The mean runtime across test cases to generate 100 scaffolds was 49 minutes.  Per-problem runtimes are reported in [runtime_by_problem.txt](./runtime_by_problem.txt).

### 3. Assemble `scaffold_info.csv` for each benchmark problem.
Finally we generated the `scaffold_info.csv` metadata files for each problem with [write_all_scaffold_lab_motif_info_csvs.sh](./write_all_scaffold_lab_motif_info_csvs.sh).
