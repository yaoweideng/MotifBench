# Bos taurus carboxypeptidase A 6cpa

Example obtained from:
"New algorithms and an in silico benchmark for computational enzyme design"
https://pubmed.ncbi.nlm.nih.gov/17132862/


> fetch 6cpa
// select Zn and ZAF (ligand complex)
// rename selection as "ligand"
# show polar contacts with other atoms in the selection
// sidebar --> "ligand" --> "A" --> "Find" --> "Polar contacts" --> "to other atoms in object"

# find and show residues near ligand
> select within_cutoff, br. ligand around 3
> show sticks,  within_cutoff

# Seems that active site residues with polar contacts are:
H69 E72 R127 H196 Y248 E270, allow redesign for 70-71

There are 307 residues total.

