# MotifBench V1.0
MotifBench is a standardized protein design benchmark for motif-scaffolding problems.
The motif-scaffolding problem is a central task in computational protein design:
Given the coordinates of atoms in a geometry chosen to confer a desired biochemical function (a motif), the goal is to identify diverse protein structures (scaffolds) that include the motif and stabilize its geometry.

MotifBench is introduced in a [whitepaper](PAPER_LINK_WHEN_READY).
In this companion repository we provide:
* [A collection of motif test cases](#test-cases)
* [Evaluation instructions with an example](#evaluation)
* [A performance leaderboard (with submission instructions)](#leaderboard)
* [Acknowledgements](#acknowledgement)

# Test-Cases

The benchmark test problems are specified in `./motif_specs.csv`, in the table below, and through the pdb files in `./motif_pdbs/`.
In table below, each row corresponds to a problem in the benchmark.


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

The following columns characterize the problems:
* `PDB ID` The Protein Data Bank identifier of the experimentally characterized structure from which the motif extracted.
* `Group` The problem group into which the motif is assigned (TODO: describe once grouping is decided).
* `Length` The number of residues that must required in each scaffold
* `Motif Residues` The chain ID and indices of residues that comprise the motif.  Discontiguous residue ranges are separated by semicolons.
* `Positions where residue may be designed` The indices of residues within motif segments for which the amino acid type is not constrained to match its identity in the reference protein.  This column is included because in cases where side-chain atoms are not involved in protein function, the motif-scaffolding problem may be made easier by allowing alternative amino acid types to be chosen for these positions during fixed-backbone sequence design.

### Motif pdb files in `./motif_pdbs/`
We provide a pdb for each benchmark problems in [./motif_pdbs/](./motif_pdbs/) for use as input to motif scaffolding methods.
These files have been constructed programmatically using `./scripts/download_and_format_motifs.py`, which reads the motif problem specifications in [./motif_specs.csv](./motif_specs.csv), downloads associated experimental structures from [rcsb.org](https://www.rcsb.org/), and parses out data for each motif.
In these files:
* Each segment of the motif is labeled as its own chain (i.e. A, B, C, etc).
* For residues for which the amino acid type may be redesigned, all atoms other than N, CA, C, and O are removed and the residue type is set to unknown (`UNK`).  For residues for which the amino acid type may not be redesigned, side-chain heavy atoms.
* For convenience, metadata about each problem is also specified in the header of each motif pdb fie.  It includes:
  *  `Reference PDB ID.` This is the idenitifier associated with the experimental structure from which the motif extracted.
  *  `Motif Segment Placement in Reference PDB.` This field may provide guidance for methods that require motif placement within designed scaffolds to be specified. However this aspect of a solution may also be chosen (even dynamically) in a problem-specific manner.  For example, for problem 27 (4XOJ) this field is `38;A;43;B;90;C;46`. This obtains because 4XOJ has 223 resolved residues (indexed as 16 through 238), the 38 corresponds to the 38 residues (16-54) before residue 55 (segment A), the 43 corresponds to the residues between residue 55 and 99 and so on. The final 46 indicates that the native structure terminates with 46 additional residues that are not part of the motif.
  * `Length for Designed Scaffolds.` This again is copied from the `motif_specs.csv` specification that dictates the required length of scaffolds.


# Evaluation

Evaluating the benchmark requires several steps, described below.
We provide examples of compatible inputs, example evaluation outputs, and result summaries for download from [Zenodo](https://zenodo.org/) at [zenodo.org/records/14396944](https://zenodo.org/records/14396944).
This demonstration uses scaffolds generated with [RosettaFold Diffusion](https://github.com/RosettaCommons/RFdiffusion);
we provide details and scripts used to create this example [here](./example/readme.md) for replicablility.

### Prepare backbone directory structure and metadata

For each benchmark problem, create a directory with 100 designed scaffolds as PDB files and a metadata csv file.
* Each scaffold should follow the naming format `{test_case}_{sample_number}.pdb`, where `{test_case}` is the concatenation of the problem number and the PDB ID (e.g. `01_1LDB`) and  `sample_number` is zero-indexed (e.g. `01_1LDB_0.pdb, 01_1LDB_1.pdb,...,01_1LDB_99.pdb`).
* The metadata file must be named `scaffold_info.csv` and contain two columns:
  * `sample_num`: The sample number for each backbone. This should be range from $0$ to $99$. 
  * `motif_placements`: The order of multiple motif segments in backbones. For example, for a motif with 3 segments (chains `A` and `B` in the motif_pdb file) the string `12/B/15/A/29` indicates that the full backbone chain comprises 12 residues of scaffold, then the residues of motif segment B, then another 15 residues of scaffold, then the residues of motif segment A, and finally another 29 residues of scaffold.  If placement is such that the backbone begins (respectively _ends_) with a motif segment the motif_placements string starts with the motif chain for example as `B/15/A/29` (respectively `12/B/15/A`).

The organize the scaffold and metadata files as below:
```bash
scaffolds/
|-- {test_case_1}/
|    scaffold_info.csv
|    {test_case_1}_0.pdb
|    {test_case_1}_1.pdb
|    ...
|    {test_case_1}_99.pdb
|
|-- {test_case_2}/
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
Find an example obeying these conventions in `scaffolds.zip` at [zenodo.org/records/14396944](https://zenodo.org/records/14396944).

### Install required packages and Foldseek database
To evaluation benchmark peformance on scaffolds assembled as described above, first download the repo and install necessary requirements.
```
# Clone the benchmark repo and install 
git clone git@github.com:blt2114/motif_scaffolding_benchmark.git
cd motif_scaffolding_benchmark

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
foldseek_pdb_database_path=<desired_path_for_foldseek_database>
mkdir $foldseek_pdb_database_path
cd $foldseek_pdb_database_path
foldseek databases PDB pdb tmp
```

### Run the benchmark and compile result summaries
Next, several paths must be specified in a configuration file [config.txt](config.txt), which will given as an input to the evaluation script.
```
# Paths configuration
scaffold_base_dir=<path/to/scaffolds/> # Directory with your scaffolds to benchmark, organized as above
benchmark_dir=<path/to/motif_scaffolding_benchmark/> # Location of this code repository
foldseek_db_path=</path/to/foldseek/pdb_database/pdb> # Same as $foldseek_pdb_database_path above
base_output_dir=</path/to/eval_results_dir/> # Location to write evaluation results
```

As a demonstration you can download and run the benchmark evaluation of RFdiffusion scaffolds by downloading our example case:
```
# In the benchmark repository directory, download example scaffolds from zenodo
wget https://zenodo.org/records/14396944/files/scaffolds.zip
unzip scaffolds.zip

# Write paths to config.txt
echo scaffold_base_dir=`pwd`/scaffolds/ > config.txt
echo benchmark_dir=`pwd`/ >> config.txt
echo foldseek_db_path=$foldseek_pdb_database_path >> config.txt
echo base_output_dir=`pwd`/evaluation/ >> config.txt
```

Run the evaluation script from the benchmark repository directory.
This step requires about one GPU-day.
```
# Run the evaluation for each problem in sequence on one machine / GPU
ls motif_pdbs/ | while read motif; do
    ./scripts/evaluate_bbs.sh $motif config.txt
done

# Or run on the whole set of scaffolds in parallel on a Slurm cluster
./scripts/launch_all.sh config.txt
```

Finally, compile results as:
```
./scripts/summarize_results.sh config.txt
```
Summary results are written to the <base_output_dir> specified in your config file both by problem (`summary_by_problem.csv`) and by group (`summary_by_group.csv`).
Example summary files are provided on Zenodo.

For example, for the RFdiffusion example, we can view results by group as:
```
> wget https://zenodo.org/records/14396944/files/evaluation_summaries.zip
> unzip evaluation_summaries.zip
> cat evaluation_summaries/summary_by_group.csv | column -s, -t 
Group  Number_Solved  Mean_Num_Solutions  Mean_Novelty  Mean_Success_rate
1      6              11.40               0.19          27.30
2      6              0.80                0.20          19.90
3      1              0.40                0.07          2.00
```


# Leaderboard
## TODO: create leaderboard and add in RFDiffusion results.

### Instructions for having your results added to the leaderboard
Results of motif-scaffolding methods will be shared on the github repository upon request.
To have the results of your method posted, write to [btrippe@stanford.edu](mailto:btrippe@stanford.edu) or post an issue to the github and include:
 1. Your success rate summary produced by `./scripts/collect_summaries.sh`
 1. A __permanent__ download link including (1) your submitted scaffold set, (2) the full evaluation results, and (3) summary results as produced by `./scripts/summarize_results.sh`.  We recommend using [Zenodo](https://zenodo.org/) or [Open Science Framework](https://osf.io/) for saving these results.
 1. A description of the how the scaffolds were generated.  This could be a link to an arXiv paper or github repository, or an explanation of how an existing approach (e.g. with what default or non-default settings).}
 1. A description of the compute resources used to generating backbones (e.g. "about 50 GPU hours across a variety of node types on a university cluster") }
 1. A contact name and email address to be posted with your results.
We will do our best to update this page with your results within a week.


# Acknowledgement
This repository builds heavily on several existing codebases:
* [Scaffold-Lab](https://github.com/Immortals-33/Scaffold-Lab) houses the evaluation pipeline.
* [ProteinMPNN](https://github.com/dauparas/ProteinMPNN) is used for fixed backbone sequence design.
* [ESMFold](https://github.com/facebookresearch/esm) is used for protein structure prediction.
* [Foldseek](https://github.com/steineggerlab/foldseek) is used for structural clustering and novelty evaluation.
If you use the scripts herein in published research, please consider crediting these resources.
