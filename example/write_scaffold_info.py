import sys
import os
import re
import csv
from Bio.PDB import PDBParser

def parse_pdb_name(filename):
    """Parse the PDB filename to extract the sample number."""
    match = re.match(r".+_(\d+)\.pdb", filename)
    return int(match.group(1)) if match else None

def extract_motif_placements(pdb_file):
    """Extract motif placements from the PDB file."""
    parser = PDBParser(QUIET=True)
    structure = parser.get_structure("structure", pdb_file)
    
    placements = []
    scaffold_segment_length = 0
    in_motif = False

    for chain in structure.get_chains():
        for res in chain.get_residues():
            bfactor = res["CA"].get_bfactor() if "CA" in res else 0

            if bfactor == 0:  # Residue is part of the scaffold
                if in_motif:  # Motif segment ends
                    in_motif = False
                    placements.append(f"{chain.id}")
                scaffold_segment_length += 1
            else:  # Residue is part of the motif
                if not in_motif:  # Motif segment starts
                    in_motif = True
                    if scaffold_segment_length > 0:  # Append scaffold segment
                        placements.append(str(scaffold_segment_length))
                    scaffold_segment_length = 0

        # Append scaffold segment if still tracking
        if scaffold_segment_length > 0:
            placements.append(str(scaffold_segment_length))
            scaffold_segment_length = 0

    return "/".join(placements)

def main(input_dir, output_csv):
    """Generate the scaffold_info.csv file, sorted by sample_num."""
    rows = []

    for filename in os.listdir(input_dir):
        if filename.endswith(".pdb"):
            sample_num = parse_pdb_name(filename)
            if sample_num is not None:
                pdb_file = os.path.join(input_dir, filename)
                motif_placements = extract_motif_placements(pdb_file)
                rows.append([sample_num, motif_placements])

    # Sort rows by sample_num
    rows.sort(key=lambda x: x[0])

    # Write sorted rows to the CSV
    with open(output_csv, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["sample_num", "motif_placements"])
        writer.writerows(rows)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python write_scaffold_info.py <input_directory> <output_csv>")
        sys.exit(1)

    input_directory = sys.argv[1]
    output_file = sys.argv[2]
    main(input_directory, output_file)
