import sys
import os
import re
import csv
from Bio.PDB import PDBParser


def parse_pdb_name(filename):
    """Parse the PDB filename to extract the sample number."""
    match = re.match(r".+_(\d+)\.pdb", filename)
    return int(match.group(1)) if match else None

def parse_contig_specifications(contig_file):
    """Parse the contig_specifications.csv to get a list of chain IDs for each structure."""
    chain_order = {}
    with open(contig_file, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            problem = row['problem']
            contig = row['contig']
            # Extract entries starting with a letter (chain IDs)
            chains = [segment[0] for segment in contig.split(';') if segment and segment[0].isalpha()]
            chain_order[problem] = chains
    return chain_order


def extract_motif_placements(pdb_file, chain_order, problem_id):
    """Extract motif placements from the PDB file using chain order from contig_specifications."""
    parser = PDBParser(QUIET=True)
    structure = parser.get_structure("structure", pdb_file)
    
    placements = []
    scaffold_segment_length = 0
    in_motif = False
    chains = chain_order.get(problem_id, [])
    motif_index = 0  # Tracks which motif segment's chain to use

    for chain in structure.get_chains():
        for res in chain.get_residues():
            bfactor = res["CA"].get_bfactor() if "CA" in res else 0

            if bfactor == 0:  # Residue is part of the scaffold
                if in_motif:  # Motif segment ends
                    in_motif = False
                    if motif_index < len(chains):  # Add corresponding chain ID
                        placements.append(chains[motif_index])
                        motif_index += 1
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

        # Append motif segment if still tracking
        if in_motif:
            if motif_index < len(chains):  # Add corresponding chain ID
                placements.append(chains[motif_index])


    return "/".join(placements)


def main(input_dir, output_csv, contig_file):
    """Generate the scaffold_info.csv file, sorted by sample_num."""
    chain_order = parse_contig_specifications(contig_file)
    rows = []

    for filename in os.listdir(input_dir):
        if filename.endswith(".pdb"):
            sample_num = parse_pdb_name(filename)
            if sample_num is not None:
                pdb_file = os.path.join(input_dir, filename)
                problem_id = os.path.basename(input_dir.strip("/"))  # Assuming problem_id is the folder name
                motif_placements = extract_motif_placements(pdb_file, chain_order, problem_id)
                rows.append([sample_num, motif_placements])

    # Sort rows by sample_num
    rows.sort(key=lambda x: x[0])

    # Write sorted rows to the CSV
    with open(output_csv, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["sample_num", "motif_placements"])
        writer.writerows(rows)


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python write_scaffold_info.py <input_directory> <output_csv> <contig_specifications.csv>")
        sys.exit(1)

    input_directory = sys.argv[1]
    output_file = sys.argv[2]
    contig_specifications_file = sys.argv[3]
    main(input_directory, output_file, contig_specifications_file)
