# MotifBench V1.0
MotifBench is a standardized protein design benchmark for motif-scaffolding problems.
The motif-scaffolding problem is a central task in computational protein design:
Given the coordinates of atoms in a geometry chosen to confer a desired biochemical function (a motif), the goal is to identify diverse protein structures (scaffolds) that include the motif and stabilize its geometry.

MotifBench is introduced in a [whitepaper](PAPER_LINK_WHEN_READY).
In this companion repository we provide:
* [A collection of motif test cases](#test-cases)
* [Instructions and resources for evaluating evaluation solutions](#evaluation)
* [Instructions for preparing and evaluating a set of solutions](#instructions-for-preparing-and-evaluating-a-set-of-solutions)
* [An example set of scaffolds and demonstration of the summarized results](#demonstration-of-example-set-of-scaffolds-and-evaluation)
* [A leaderboard of results of motif-scaffolding methods on the benchmark](#leaderboard)
* 

# Test-Cases

The benchmark test problems are specified in `./motif_specs.csv`, in the table below, and through the pdb files in `./motif_pdbs/`.
In table below, each row corresponds to a problem in the benchmark.
The following columns characterize the problems:
* `PDB ID` The Protein Data Bank identifier of the experimentally characterized structure from which the motif extracted.
* `Group` The problem group into which the motif is assigned (TODO: describe once grouping is decided).
* `Length` The number of residues that must required in each scaffold
* `Motif Residues` The chain ID and indices of residues that comprise the motif.  Discontiguous residue ranges are separated by semicolons.
* `Positions where residue may be designed` Self explanatory.

| #  | PDB ID | Group | Length | Motif Residues                 | Positions where residue may be designed                      | Description                        |
|----|--------|-------|--------|--------------------------------|-------------------------------------------------------------|------------------------------------|
| 1  | 1BCF   | 1     | 125    | A18-25;A47-54;A92-99;A123-130  | A19-25;A47-50;A52-53;A92-93;A95-99;A123-126;A128-129         | Di-iron binding motif              |
| 2  | 1YOV   | 1     | 75     | B213-223                       |                                                             | Ubiquitin-activating enzyme E1C binding |
| 3  | 2KL8   | 1     | 100    | A1-7;A28-79                    |                                                             | De novo designed protein           |
| 4  | 6E6R   | 1     | 75     | A23-35                         | A23-35                                                     | Ferridoxin Protein                 |
| 5  | 6E6R   | 1     | 200    | A23-35                         | A23-35                                                     | Ferridoxin Protein                 |
| 6  | 6EXZ   | 1     | 100    | A556-570                       | A556-570                                                   | RNA export factor                  |
| 7  | 6EXZ   | 1     | 200    | A556-570                       | A556-570                                                   | RNA export factor                  |
| 8  | 1ITU   | 2     | 150    | A124-147                       |                                                             | Renal dipeptidase                  |
| 9  | 1LDB   | 2     | 125    | A186-206                       |                                                             | Lactate dehydrogenase              |
| 10 | 5IUS   | 2     | 100    | A63-82;A119-140                | A63;A65;A67;A69;A71-72;A76;A79-80;A82;A119-123;A125;A127;A129-130;A133;A135;A137-138;A140 | PD-L1 binding interface on PD-1    |
| 11 | 5WN9   | 2     | 75     | A170-189                       | A170-175;A188-189                                          | RSV G-protein 2D10 site            |
| 12 | 5YUI   | 2     | 75     | A93-97;A118-120;A198-200       | A93;A95;A97;A118;A120                                      | Carbonic anhydrase active site     |
| 13 | 7A8S   | 2     | 100    | A41-55;A72-86                  |                                                             | Orphan protein                     |
| 14 | 7AHO   | 2     | 125    | A199-213                       |                                                             | Orphan protein                     |
| 15 | 7BNY   | 2     | 125    | A83-97;A111-125                |                                                             | Orphan protein                     |
| 16 | 7DGW   | 2     | 125    | A22-36;A70-84                  |                                                             | Orphan protein                     |
| 17 | 7MQQ   | 2     | 125    | A80-94;A115-129                |                                                             | Orphan protein                     |
| 18 | 1B73   | 3     | 125    | A7-8;A70;A178-180              | A179                                                       | Glutamate racemase active site     |
| 19 | 1LCC   | 3     | 150    | A1-52                          |                                                             | DNA-binding helix-turn-helix       |
| 20 | 1MPY   | 3     | 125    | A153;A199;A214;A246;A255;A265  |                                                             | Catechol deoxygenase active site   |
| 21 | 1QY3   | 3     | 225    | A58-71;A96;A222                | A62;A65-67;A96;A222                                        | GFP pre-cyclized state             |
| 22 | 2RKX   | 3     | 225    | A9-11;A48-50;A101;A128;A169;A176;A201;A222-224 | A10;A49;A223                                               | De novo designed Kemp eliminase    |
| 23 | 3B5V   | 3     | 200    | A51-53;A81;A110;A131;A159;A180-184;A210-211;A231-233 | A52;A181;A183;A232                                         | De novo designed retro-aldol enzyme |
| 24 | 4JHW   | 3     | 125    | F63-69;F196-212                | F63;F69;F196;F198;F203;F211-212                            | RSV F-protein Site 0               |
| 25 | 4XOJ   | 3     | 150    | A55;A99;A190-192               | A191                                                       | Trypsin catalytic triad and oxyanion hole |
| 26 | 6CPA   | 3     | 200    | A69-72;A127;A196;A248;A270     | A70-71                                                     | Carboxypeptidase active site       |
| 27 | 7AD5   | 3     | 125    | A99-113                        |                                                             | Orphan protein                     |
| 28 | 7WRK   | 3     | 125    | A80-94                         |                                                             | Orphan protein                     |
| 29 | 7UWL   | 3     | 175    | E63-73;E101-111                | E63-73;E101-103;E105-111                                   | IL17-RA interface to IL17-RB       |
| 30 | 7UWL   | 3     | 175    | E63-73;E101-111;E132-142;E165-174 | E63-73;E101-103;E105-111;E132-142;E165-174                 | IL17-RA interface to IL17-RB       |

# Evaluation

Evaluating a collection of scaffolds according to the specification of the benchmark requires several steps

### Prepare backbone directory structure and metadata

For each benchmark problem create a directory containing a metadata file and the 100 designed scaffolds.
* Each scaffold should follow the naming format {test_case}_{sample_number}.pdb, where `test_case` is the concatenation of the problem number and the PDB ID (e.g. `01_1LDB`) and  `sample_number` is 1-indexed (e.g. `01_1LDB_0.pdb, 01_1LDB_1.pdb,...,01_1LDB_99.pdb`).

```bash
backbone_outputs
|-- test_case_1/
|    scaffold_info.csv
|    {test_case_1}_0.pdb
|    {test_case_1}_1.pdb
|    ...
|    {test_case_1}_99.pdb
|
|-- test_case_2/
|    scaffold_info.csv
|    {test_case_2}_0.pdb
|    {test_case_2}_1.pdb
|    ...
|    {test_case_2}_99.pdb
|
| ....
|
|-- test_case_30/
|  ...
```

The metadata file should be named `scaffold_info.csv` and contain two columns:
* `sample_num`: The sample number for each backbone. This should be range from $1$ to $100$. 
* `motif_placements`: The order of multiple motif segments in backbones. For example, for a motif with 3 segments the string `12/A/6/C/29/B/17` would indicate that pdb file with the following:
  * First 12 residues of scaffold
  * followed by motif segment A
  * followed by 6 residues of scaffiold
  * followed by motif semgent C
  * followed by 29 residues of scaffold
  * followed by motif segment B
  * terminating with 17 residues of scaffold.

### Evaluate each scaffold set independently

```
# Clone the benchmark repo
git clone git@github.com:blt2114/motif_scaffolding_benchmark.git
cd motif_scaffolding_benchmark
```

```
# Create and activate environment
conda env create -f motif_bench.yml
conda activate motif_bench
```

The workhorse benchmarking evaluation steps are implemented in [Scaffold-Lab](https://github.com/Immortals-33/Scaffold-Lab).
```
# Install Scaffold-lab into your conda environment
pip install -e Scaffold-Lab
```

For novelty evaluation, the Foldseek PDB database is required.
```
foldseek_pdb_database_path=./pdb
mkdir $foldseek_pdb_database_path
cd $foldseek_pdb_database_path
foldseek databases PDB pdb tmp
```

Next, several paths must be specified in a configuration file [config.txt](config.txt) which is given as an input to the evaluation script.
```
# Paths configuration
scaffold_base_dir=<path/to/backbone_outputs/> # Directory with your scaffolds to benchmark, organized as above
benchmark_dir=<path/to/motif_scaffolding_benchmark/> # Location of this code repository
foldseek_db_path=</path/to/foldseek/pdb_database/pdb> # Same as $foldseek_pdb_database_path above
base_output_dir=</path/to/eval_results_dir/> # Location to write evaluation results
```

Then from the repository directory run the evaluation script:
```
# Run the evaluation for each problem in sequence on one machine / GPU
ls motif_pdbs/ | while read motif; do
    ./scripts/evaluate_bbs.sh $motif config.txt
done

# Or run on the whole set of scaffolds in parallel on a Slurm cluster
./scripts/launch_all.sh config.txt
```

Running the benchmark requires about one GPU-day.  (TODO: say something about GPU type and memory requirements!)
Finally compile results as 
```
./scripts/summarize_results.sh config.txt
```

Summary results are written to the <base_output_dir> specified in your config file both by problem (`summary_by_problem.csv`) and by group (`summary_by_group.csv`).
For example for the RFdiffusion example, we can view results by group as:
```
> cat rfdiffusion_eval/summary_by_group.csv | column -s, -t 
Group  Number_Solved  Mean_Num_Solutions  Mean_Novelty  Mean_Success_rate
1      6              11.40               0.19          27.30
2      6              0.80                0.20          19.90
3      1              0.40                0.07          2.00
```


## Demonstration of example set of scaffolds and evaluation
We have included an example collection of scaffolds for all benchmark problems produced by [RosettaFold Diffusion](https://github.com/RosettaCommons/RFdiffusion) in [./example/rfdiffusion_test_run/](./example/rfdiffusion_test_run/).
Further information is provided in [here](./example/readme.md).

To run the evaluation you must first download the files. 
These are stored with `git-lfs`
which must be installed (see instructions [here](https://docs.github.com/en/repositories/working-with-files/managing-large-files/installing-git-large-file-storage).
```
git lfs fetch --all
git lfs checkout
```

Then set the relevant fields in [config.txt](./config.txt).

Using slurm, all jobs may be launched as:
```
./scripts/launch_all.sh config.txt
```


## Motif Specification Format
`./parsing/motif_load_and_parse.ipynb` parses the motif problem specifications 
writes out target motifs as `.pdb` files to be used as input for motif scaffolding methods.
In these files:
* Each segment of the motif is labeled as its own chain (i.e. A, B, C, etc).
* For residues for which the amino acid type may be redesigned, all atoms other than N, CA, C, and O are removed and the residue type is set to unknown (`UNK`).  Side-chain heavy atoms are included for other residues.
* The header of the motif includes a contig specifying how the motif is placed in the native scaffold. This header can provide guidance for methods that require the length of a scaffold and the order and placement of the motif to be specified. However this aspect of a solution may also be chosen (even dynamically) in a problem-specific manner.
  * Example: for motif specification `4xoj,A55;A99;A190-192,A191` the header contig is `38;A;43;B;90;C;46`. This obtains because 4xoj has 223 resolved residues (indexed as 16 through 238), the 38 corresponds to the 38 residues (16-54) before residue 55 (segment A), the 43 corresponds to the residues between residue 55 and 99 and so on. The final 46 indicates that the native structure terminates with 46 additional residues that are not part of the motif.

# Leaderboard
## TODO: create leaderboard and add in RFDiffusion results.

### Instructions for having your results added to the leaderboard
Results of motif-scaffolding methods will be shared on the github repository upon request.
To have the results of your method posted, write to [btrippe@stanford.edu](mailto:btrippe@stanford.edu) or post an issue to the github and include:
 1. Your success rate summary produced by `./scripts/collect_summaries.sh`
 1. A __permanent__ download link from which (1) your submitted scaffold set and (2) all intermediate evaluation results as produced by `./scripts/compile_results.sh` (TODO: write this script!).  We recommend using [Zenodo](https://zenodo.org/) or [Open Science Framework](https://osf.io/). 
 1. A description of the how the scaffolds were genereated.  This could be a link to an arXiv paper or github repository, or an explanation of how an existing approach was used with non-standard settings.}
 1. A description of the compute resources used to generating backbones (e.g.\ ``about 50 GPU hours across a variety of node types on the university cluster'') }
 1. A contact name and email address to be posted with your results.
We will do our best to update with your results within a week.


# Acknowledgement
This repository wraps [Scaffold-Lab](https://github.com/Immortals-33/Scaffold-Lab) for the benchmark implementation.
If you use the scripts herein in published research, please attributed credit there as well.
