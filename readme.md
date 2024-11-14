# Motif-Scaffolding Benchmark Test Cases

This repository describes a updated set of benchmark problems and provides code that
parses a motif specification into a standardized format for motif-scaffolding methods.



## Motif Specification Format

### Motif-file specification
`./parsing/motif_load_and_parse.ipynb` parses the motif problem specifications 
writes out target motifs as `.pdb` files to be used as input for motif scaffolding methods.
In these files:
* Each segment of the motif is labeled as its own chain (i.e. A, B, C, etc).
* For residues for which the amino acide type may be redesigned, all atoms other than N, CA, C, and O are removed and the residue type is set to unknown (`UNK`).  Side-chain heavy atoms are included for other residues.
* The header of the motif includes a contig specifying how the motif is placed in the native scaffold. This header can provide guidance for methods that require the length of a scaffold and the order and placement of the motif to be specified. However this aspect of a solution may also be chosen (even dynamically) in a problem-specific manner.
  * Example: for motif specification `4xoj,A55;A99;A190-192,A191` the header contig is `38;A;43;B;90;C;46`. This obtains because 4xoj has 223 resolved residues (indexed as 16 through 238), the 38 corresponds to the 38 residues (16-54) before residue 55 (segment A), the 43 corresponds to the residues between residue 55 and 99 and so on. The final 46 indicates that the native structure terminates with 46 additional residues that are not part of the motif.

## Provide Necessary Inputs for Evaluation

Typically, once designed scaffolds are generated, they'll entering a preprocessing stage including:

*  Backbones are subtracted and renamed by sample numbers. The naming format is {case_number}+{case_name}_{sample_number}.pdb, where `sample_number` follows the **1-based** system. (e.g. 01_1BCF_1.pdb. 01_1BCF_2.pdb,...,01_1BCF_100.pdb).
* The outputs should be organized like:

```bash
backbone_outputs
|-- pdb_case_1
|    01_{pdb_case_1}_1.pdb
|    01_{pdb_case_1}_2.pdb
|    ...
|    01_{pdb_case_1}_100.pdb
|
|-- pdb_case_2
|    02_{pdb_case_2}_1.pdb
|    02_{pdb_case_2}_2.pdb
|    ...
|    02_{pdb_case_2}_100.pdb
|  
|  ......
|
|-- pdb_case_41
|--  41_{pdb_case_41}_1.pdb
|--  41_{pdb_case_41}_2.pdb
|--  41_{pdb_case_41}_100.pdb
```

After that, you need to provide information for motifs and scaffolds. Similar to [the usage within RFdiffusion](https://github.com/RosettaCommons/RFdiffusion?tab=readme-ov-file#motif-scaffolding), we specify them by contigs. 

### Contig Grammar

 A **_contig_** is a placeholder to indicate the information for motifs and scaffolds in designed protein structures. For each protein backbone, you need to provide a contig to show the motif placements and positions to be redesigned. 

Within our grammar system, a complete contig includes **two** to **four** parts separated by a `,` (**comma**). In the following parts, we would use `01_1BCF,12/A92-99/22/A123-130/22/A47-54/24/A18-25/13,A19-25;A47-50;A52-53;A92-93;A95-99;A123-126;A128-129,C;D;B;A` of the benchmark case **_1BCF_** as an example. Separated by the commas are four parts:

* **The native PDB name:** This is for extracting native motifs for calculation and identification. e.g. `01_1BCF` in this case.
* **Motif Placement:** This part shows the information of where the motifs and scaffolds are placed. e.g. `12/A92-99/22/A123-130/22/A47-54/24/A18-25/13` in this case.
  - The **motif** parts start with an uppercase letter and contain information about the corresponding **native motifs.** If the numbers are continuous, then separated by **hyphens**. The boundaries of motifs and scaffolds are separated by **slashes**.
  - The **scaffold** parts are single numbers, which is **deterministic** as the scaffold part of the uploaded PDB files are already placed during the design process. **The motif parts indicate residues in native PDBs but not scaffold PDBs. We choose this way because this would be convenient for users to locate which part the motifs are mimicking corresponding to the reference PDBs.**
  - Together, the motif placement part provides information about which parts are motifs (indicated by chain letter) and how they correspond to native ones, and the overall length of the designed scaffold. For example, `12/A92-99/22/A123-130/22/A47-54/24/A18-25/13` means the scaffold parts contains:
    - First a 12-residue scaffold in the N-terminal;
    - Then a motif part mimicking residue 92~99 in chain A in **_1BCF_**;
    - Followed by a 22-residue scaffold;
    - Then a motif part mimicking residue 123~130 in chain A in **_1BCF_**;
    - Followed by a 22-residue scaffold;
    - Then a motif part mimicking residue 47~54 in chain A in **_1BCF_**;
    - Followed by a 24-residue scaffold;
    - Then a motif part mimicking residue 18~25 in chain A in **_1BCF_**;
    - Finally a 13-residue scaffold in the C-terminal of the designed structure.
* **Redesigned positions:** This part indicates which positions to be redesigned in the **reference proteins**, e.g.`A19-25;A47-50;A52-53;A92-93;A95-99;A123-126;A128-129` in this case indicates residue 19~25, 47~50, 52~53, 92~93, 95~99, 123~126, 128~129 of chain A in **_1BCF_**. Different redesigned positions are separated by **semi-colons**; if the positions are continuous, then connected by **hyphens**; always starts with an uppercase chain letter.
* **Segment order**: The order of multiple motif segments in backbones. For example, for `01_1BCF`, the default motif segment order could be read from [here](https://github.com/blt2114/motif_scaffolding_benchmark?tab=readme-ov-file#benchmark-test-cases): `{"A": A18-25, "B": A47-54, "C": A92-99, "D": A123-130}`. So again, let's take `12/A92-99/22/A123-130/22/A47-54/24/A18-25/13` for **_1BCF_** as an example: In this contig, the ordering of motifs appeared in the designed structure is `A92-99`->`A123-130`->`A47-54`->`A18-25`. Therefore, the resulting segment order should be `C;D;B;A` separated by a `;`(**semicolon**).

> [!NOTE]
>
> * It is important to note that **no space** should appear inside even a complete contig! 
> * For PDB code of `case_name`, we use **uppercase** by default.
> * If redesigned positions is null, simply left the part with nothing. (to be adjusted)

The users must specify the contig with the following rules:

- The **overall lengths** of the designed scaffolds are **fixed** within each PDB case and shouldn’t be changed throughout the benchmarking procedure. But we encourage method developers to develop algorithms that allow length-variable designs.
- The **redesigned positions** of the designed scaffolds should strictly follow the ones presented in the table of the standardized benchmark. 
- However, the placement of motifs and scaffolds within the overall lengths could be specified by the users themselves, as long as they provide the correct contig for benchmarking.

We provide flexible ways for users to specify the contig information. You can go either way you want within the following choices.

### Specify contig information through a CSV file (Recommended)

For each case, the users should provide the following information:

* `pdb_name`: The case name, which should be identical for each backbone within one specific benchmark case. e.g. `01_1BCF` for **_1BCF_**.
* `sample_num`: The sample number for each backbone. Should be range from $1$ to $100$ in the standardized benchmark. 
* `contig`: The **motif placement** string aforementioned indicating the motif and scaffold information for each backbone.
* `redesign_positions`: The **redesigned positions** aforementioned for which positions to be redesigned for each backbone.
* `segment_order`: The order of multiple motif segments in backbones. 

After that, the evaluation pipeline could use this single csv file for mapping between **each designed structure** and their **corresponding motif placements**, which would allow us to evaluate them correctly. 

###   Specify through PDB Header

The users can specify the contig string in the **“classification”** part of the PDB header. Here we have two ways for contig parsing:

* **A complete contig string:** Should be followed the format mentioned above with two or three parts separated by commas. The native PDB ID and motif placement are always necessary, and the part of redesigned positions is additionally provided if there’s a need. 
* For specification of redesigned positions, another straightforward way is to **index them by the “UNK” residues**. The logic here is, if the code found the contig string just have two parts, it will automatically look for “UNK” residues inside the PDB file and specify them as positions to be redesigned.


## Benchmark test cases
The benchmark test problems are specified in `./motif_specs.csv`,
and repeated below with a brief description and references for their provenances.


| #  | PDB  | Motif Residues | Redesigned Positions | Description |
| -- | ---- | -------------- | -------------------- | ----------- |
| 1  | 1BCF | A18-25;A47-54;A92-99;A123-130 | A19-25;A47-50;A52-53;A92-93;A95-99;A123-126;A128-129 | Di-iron binding motif [1] |
| 2  | 5TPN | A163-181 | A163-168;A170-171;A179 | RSV F-protein Site V [1] |
| 3  | 5IUS | A119-140;A63-82 | A63;A65;A67;A69;A71-72;A76;A79-80;A82;A119-123;A125;A127;A129-130;A133;A135;A137-138;A140 | PD-L1 binding interface on PD-1 [1] |
| 4  | 3IXT | P254-277 | P255;P258-259;P262-263;P268;P271-272;P275-276 | RSV F-protein Site II [2] |
| 5  | 5YUI | A93-97;A118-120;A198-200 | A93;A95;A97;A118;A120 | Carbonic anhydrase active site [1] |
| 6  | 1YCR | B19-27 | B20-22;B24-25 | P53 helix that binds to Mdm2 [1] |
| 7  | 2KL8 | A1-7;A28-79 | | De novo designed protein [1] |
| 8  | 7MRX | B25-46 | B25-46 | Barnase ribonuclease inhibitor [3] |
| 9  | 4JHW | F63-69;F196-212 | F63;F69;F196;F198;F203;F211-212 | RSV F-protein Site 0 [4] |
| 10  | 4ZYP | A422-436 | A422-427;A430-431;A433-43 | RSV F-protein Site 4 [4] |
| 11  | 5WN9 | A170-189 | A170-175;A188-189 | RSV G-protein 2D10 site [2] |
| 12  | 5TRV | A45-65 | A45-65 | De novo designed protein [5] |
| 13  | 6E6R | A23-35 | A23-35 | Ferridoxin Protein [5] |
| 14  | 6EXZ | A556-570 | A556-570 | RNA export factor [5] |
| 15  | 7A8S | A41-55;A72-86 |  | Orphan protein [6] |
| 16  | 7AD5 | A99-113 |  | Orphan protein [6] |
| 17  | 7AHO | A199-213 |  | Orphan protein [6] |
| 18  | 7BNY | A83-97;A111-125 |  | Orphan protein [6] |
| 19  | 7DGW | A22-36;A70-84 |  | Orphan protein [6] |
| 20  | 7KUW | A2-16;A30-44 |  | Orphan protein [6] |
| 21  | 7KWW | B14-28 |  | Orphan protein [6] |
| 22  | 7MQQ | A80-94;A115-129 |  | Orphan protein [6] |
| 23  | 7S5L | A27-41;A77-91 |  | Orphan protein [6] |
| 24  | 7WRK | A80-94 |  | Orphan protein [6] |
| 25  | 6CPA | A69-72;A127;A196;A248;A270 | A70-71 | Carboxypeptidase active site  [7] |
| 26  | 1MPY | A153;A199;A214;A246;A255;A265 |  | catechol deoxygenase active site [7] |
| 27  | 1B73 | A7-8;A70;A178-180 | A179 | Glutamate racemase active site [7] |
| 28  | 2RKX | A9-11;A48-50;A101;A128;A169;A176;A201;A222-224 | A10;A49;A223 | De novo designed Kemp eliminase [8] |
| 29  | 3B5V | A51-53;A81;A110;A131;A159;A180-184;A210-211;A231-233 | A52;A181;A183;A232 | De novo designed retro-aldol enzyme [9]  |
| 30  | 4XOJ | A55;A99;A190-192 | A191 | Trypsin catalytic triad and oxyanion hole [10] |
| 31  | 1QY3 | A58-71;A96;A222  | A62;A65-67;A96;A222 | GFP pre-cyclized state (** must restore residue 96 to Arg rather than keep inactive R96A mutation ** ) [11] |
| 32  | 1LDB | A186-206 |  | Lactate dehydrogenase  [11] |
| 33  | 1ITU | A124-147 | | Renal dipeptidase  [11] |
| 34  | 1YOV | B213-223 | |  Ubiquitin-activating enzyme E1C binding  [11] |
| 35  | 1A41 | A248-280 | | DNA topoisomerase  [11] |
| 36  | 1LCC | A1-52 | | DNA-binding helix-turn-helix  [11] |
| 37  | 5ZE9 | A229-243| | P-loop  [11] |
| 38  | 7UWL | E63-73;E101-111 | E63-73;E101-103;E105-111 | IL17-RA interface that interacts with IL17-RB [12] |
| 39  | 7UWL | E63-73;E101-111;E132-142;E165-174 | E63-73;E101-103;E105-111;E132-142;E165-174 | IL17-RA interface that interacts with IL17-RB [12] |

The last six problems (6CPA, 1MPY,  1B73,  2RKX,  3B5V, and 4XOJ) are enzyme active sites extracted from various sources detailed in `test_case_sources/other_enzymes/`.

### References:
* [1] https://www.science.org/doi/10.1126/science.abn2100
* [2] https://www.nature.com/articles/s41589-020-00699-x
* [3] https://www.nature.com/articles/s43588-023-00440-3
* [4] https://www.science.org/doi/10.1126/science.aay5051
* [5] https://arxiv.org/abs/2206.04119
* [6] https://www.biorxiv.org/content/10.1101/2022.07.21.500999v1
* [7] https://academic.oup.com/nar/article/46/D1/D618/4584620
* [8] https://www.nature.com/articles/nature06879 
* [9] https://pubmed.ncbi.nlm.nih.gov/18323453/
* [10] https://www.biorxiv.org/content/10.1101/2024.02.28.582624v2
* [11] https://www.evolutionaryscale.ai/papers/esm3-simulating-500-million-years-of-evolution-with-a-language-model
* [12] https://www.nature.com/articles/s41586-022-05116-y
