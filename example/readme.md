# Example scaffold details

As an example for demonstrating evaluation with MotifBench and to stand as a baseline for evaluation of novel motif-scaffolding methods we have designed scaffolds each benchmark problem with [RosettaFold Diffusion](https://github.com/RosettaCommons/RFdiffusion) and uploaded these scaffolds to [Zenodo](https://zenodo.org/) at [zenodo.org/records/14731790](https://zenodo.org/records/14731790).

The below provides details and scripts about how this scaffold set was generated.

### 1. Choosing "contigs" in [contig_specifications.csv](./contig_specifications.csv)
RFdiffusion requires the specification of a "contig" that describes the placement of the sequence-contiguous motif segments in the scaffold to be generated.
This choice of contig can have significant implications on the scaffolds that it generates.
For motifs problems that were part of the earlier RFdiffusion benchmark set, we adopt the contig used there.

For the problems with one segment we chose the contig to place no limits on the size of the flanking regions. 

For the remaining problems we chose contigs that specified order of segments in the reference structure and included gaps between segments of at least 10 residues that spanned the gap in the reference structure between the associated segments.

### 2. Running RFdiffusion motif-scaffolding via apptainer and docker image
* We installed RFdiffusion using the docker image (see [readme](https://github.com/RosettaCommons/RFdiffusion?tab=readme-ov-file#docker), accessed November 2024).
* We used generated SLURM scripts for each benchmark problem using [write_scripts_by_case.sh](./write_scripts_by_case.sh).  The script includes details of the exact RFdiffusion run commands.
* We ran these on a university compute cluster, [Sherlock](www.sherlock.stanford.edu).  Each script ran on a single GPU, of which the model varied.  The mean runtime across test cases to generate 100 scaffolds was 62 minutes.  Per-problem runtimes are reported in [runtime_by_problem.txt](./runtime_by_problem.txt).

### 3. Assembly of `scaffold_info.csv` for each benchmark problem.
Finally we generated the `scaffold_info.csv` metadata files for each problem with [write_all_scaffold_info_csvs.sh](./write_all_scaffold_info_csvs.sh).


# Reference PDB evaluation results
We additional provide intermediate computations and results of the evaluation of reference scaffolds from which motifs are defined in [reference_pdb_baseline/](./reference_pdb_baseline/).
