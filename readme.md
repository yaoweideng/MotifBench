# Motif-Scaffolding Benchmark Test Cases

This repository describes a updated set of benchmark problems and provides code that
parses a motif specification into a standardized format for motif-scaffolding methods.

## Motif specification format for motifs

A motif present in an existing structure may be specified by a comma-separated string with:
1. The PDB id of the protein from which the motif is obtained.
2. The chain and residue indices of the amino acids comprising the motif.  Contiguous segments of residues are concatenated into a list separated by semi-colons.
3. The chain and indices of residues whose amino acid identity may be redesigned.



### Examples
* `7F7P,B32-46;A7-21,B32-46;A7-21` --> two segments of motif. Residues 32 through 46 on chain B and residues 7 through 21 on chain A.  All positions may be redesigned.

* `4xoj,A55;A99;A190-192,A191` --> three segments of motif.  All segments are on chain A.  Residues 55, 99, 190, 191, and 192.  Only residue 191 may be redesigned.

### Motif-file specification
`./parsing/motif_load_and_parse.ipynb` parses the motif problem specifications 
writes out target motifs as `.pdb` files to be used as input for motif scaffolding methods.
In these files:
* Each segment of the motif is labeled as its own chain (i.e. A, B, C, etc).
* For residues for which the amino acide type may be redesigned, all atoms other than N, CA, C, and O are removed and the residue type is set to unknown (`UNK`).  Side-chain heavy atoms are included for other residues.
* The header of the motif includes a contig specifying how the motif is placed in the native scaffold. This header can provide guidance for methods that require the length of a scaffold and the order and placement of the motif to be specified. However this aspect of a solution may also be chosen (even dynamically) in a problem-specific manner.
  * Example: for motif specification `4xoj,A55;A99;A190-192,A191` the header contig is `38;A;43;B;90;C;46`. This obtains because 4xoj has 223 resolved residues (indexed as 16 through 238), the 38 corresponds to the 38 residues (16-54) before residue 55 (segment A), the 43 corresponds to the residues between residue 55 and 99 and so on. The final 46 indicates that the native structure terminates with 46 additional residues that are not part of the motif.


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
| 19  | 7CG5 | A95-109 |  | Orphan protein [6] |
| 20  | 7DGW | A22-36;A70-84 |  | Orphan protein [6] |
| 21  | 7KUW | A2-16;A30-44 |  | Orphan protein [6] |
| 22  | 7KWW | B14-28 |  | Orphan protein [6] |
| 23  | 7MQQ | A80-94;A115-129 |  | Orphan protein [6] |
| 24  | 7S5L | A27-41;A77-91 |  | Orphan protein [6] |
| 25  | 7WRK | A80-94 |  | Orphan protein [6] |
| 26  | 6CPA | A69-72;A127;A196;A248;A270 | A70-71 | Carboxypeptidase active site  [7] |
| 27  | 1MPY | A153;A199;A214;A246;A255;A265 |  | catechol deoxygenase active site [7] |
| 28  | 1B73 | A7-8;A70;A178-180 | A179 | Glutamate racemase active site [7] |
| 29  | 2RKX | A9-11;A48-50;A101;A128;A169;A176;A201;A222-224 | A10;A49;A223 | De novo designed Kemp eliminase [8] |
| 30  | 3B5V | A51-53;A81;A110;A131;A159;A180-184;A210-211;A231-233 | A52;A181;A183;A232 | De novo designed retro-aldol enzyme [9]  |
| 31  | 4XOJ | A55;A99;A190-192 | A191 | Trypsin catalytic triad and oxyanion hole [10] |
| 32  | 1QY3 | A58-71;A96;A222  | A62;A65-67;A96;A222 | GFP pre-cyclized state (** must restore residue 96 to Arg rather than keep inactive R96A mutation ** ) [11] |
| 33  | 1LDB | A186-206 |  | Lactate dehydrogenase  [11] | 
| 34  | 1ITU | A124-147 | | Renal dipeptidase  [11] |
| 35  | 1YOV | B213-223 | |  Ubiquitin-activating enzyme E1C binding  [11] |
| 36  | 1A41 | A248-280 | | DNA topoisomerase  [11] |
| 37  | 1LCC | A1-52 | | DNA-binding helix-turn-helix  [11] |
| 38  | 5ze9 | A229-243,| P-loop  [11] |

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
