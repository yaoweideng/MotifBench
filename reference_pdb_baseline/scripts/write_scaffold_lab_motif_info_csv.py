import sys
import os
import re
import csv
from Bio.PDB import PDBParser, PDBIO, Structure, Model, Chain, Residue


def reindex_pdb(input_pdb, output_pdb):
    # Parse the input PDB file
    parser = PDBParser(QUIET=True)
    structure = parser.get_structure("structure", input_pdb)
    
    # Assume there is only one model and one chain in the structure
    original_chain = structure[0].child_list[0]  # Get the first (and only) chain

    # Create a new structure with a single model and chain
    new_structure = Structure.Structure("reindexed_structure")
    new_model = Model.Model(0)
    new_chain = Chain.Chain("A")  # Use "A" as the chain ID for the new structure
    new_model.add(new_chain)
    new_structure.add(new_model)

    # Set new residue index starting from 1
    new_index = 1
    for residue in original_chain:
        # Skip heteroatoms (HETATM) to avoid reindexing them
        if residue.id[0] != " ":
            continue

        # Copy the residue and assign a new unique index
        new_residue = residue.copy()
        new_residue.id = (" ", new_index, " ")
        new_chain.add(new_residue)
        new_index += 1  # Increment index for the next residue

    # Save the modified structure to the output file
    io = PDBIO()
    io.set_structure(new_structure)
    io.save(output_pdb)


def parse_pdb_name(filename):
    match = re.match(r"(.+)\.pdb", filename)
    if match:
        return match.group(1)
    return None

def extract_contig_and_redesign_positions(pdb_file):
    parser = PDBParser(QUIET=True)
    structure = parser.get_structure("structure", pdb_file)
    
    contig = []
    redesign_positions = []
    non_zero_segments = []
    chain_residues = {}
    
    for chain in structure.get_chains():
        current_segment = []
        scaffold_segment_length = 0
        in_motif = False
        
        for res in chain.get_residues():
            bfactor = res["CA"].get_bfactor() if "CA" in res else 0
            res_id = res.get_id()[1]
            res_name = res.get_resname()
            
            # Determine if the current residue is part of the motif or scaffold
            if bfactor != 1.:  # Residue `res` is part of the scaffold
                if in_motif: # A motif segment has just finished
                    in_motif = False

                    # Create contig component for motif segment.
                    chain_id = current_segment[0][0]
                    start = current_segment[0][1]
                    end = current_segment[-1][1]
                    non_zero_segments.append(current_segment)
                    contig.append(f"{chain_id}{start}-{end}")
                    current_segment = []
                scaffold_segment_length += 1
            else: # Residue `res` is part of the motif
                if not in_motif:  # A motif segment has just started
                    in_motif = True
                    if scaffold_segment_length: # A scaffold segment has ended
                        # Create contig component for scaffold segment.
                        contig.append(str(scaffold_segment_length))
                    scaffold_segment_length = 0
                current_segment.append((chain.id, res_id))
            
            # Check for "UNK" residues for redesign positions
            if res_name == "UNK":
                chain_residues.setdefault(chain.id, []).append(res_id)
        
        # Append any remaining non-zero or zero segment after last residue
        if current_segment:
            chain_id = current_segment[0][0]
            start = current_segment[0][1]
            end = current_segment[-1][1]
            non_zero_segments.append(current_segment)
            contig.append(f"{chain_id}{start}-{end}")
        if scaffold_segment_length:
            contig.append(str(scaffold_segment_length))
    
    contig_str = "/".join(contig)
    
    # Format the redesign positions string
    redesign_positions_str = []
    for chain, residues in chain_residues.items():
        residues.sort()
        ranges = []
        start = residues[0]
        for i in range(1, len(residues)):
            if residues[i] != residues[i - 1] + 1:
                if start == residues[i - 1]:
                    ranges.append(f"{chain}{start}")
                else:
                    ranges.append(f"{chain}{start}-{residues[i - 1]}")
                start = residues[i]
        # Append the last range
        if start == residues[-1]:
            ranges.append(f"{chain}{start}")
        else:
            ranges.append(f"{chain}{start}-{residues[-1]}")
        redesign_positions_str.extend(ranges)
    
    return contig_str, ";".join(redesign_positions_str)

def get_segment_order(rfdiffusion_contig_info, pdb_name):
    with open(rfdiffusion_contig_info, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] == pdb_name:
                # The segment order is in the last column of the line
                segments = sorted(row[-1].split(";"))
                # Extract chain identifiers and join them as "C;D;B;A"
                segment_order = ";".join(segment[0] for segment in segments if not segment[0].isnumeric() )
                return segment_order
    return ""

def main(input_dir, output_csv, rfdiffusion_contig_info):
    with open(output_csv, 'w', newline='') as csvfile:
        fieldnames = ["pdb_name", "sample_num", "contig", "redesign_positions", "segment_order"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=',')
        writer.writeheader()
        
        for filename in os.listdir(input_dir):
            print(filename)
            if filename.endswith(".pdb"):
                reindex_pdb(input_dir + "/" + filename,input_dir + "/" +  filename)
                pdb_name = filename.split("/")[-1].split(".")[0]
                pdb_name = pdb_name[:7]
                if pdb_name is not None:
                    pdb_file = os.path.join(input_dir, filename)
                    contig, redesign_positions = extract_contig_and_redesign_positions(pdb_file)
                    
                    # Get segment order from rfdiffusion_contig_info
                    segment_order = get_segment_order(rfdiffusion_contig_info, pdb_name)
                    
                    writer.writerow({
                        "pdb_name": pdb_name,
                        "sample_num": 0,
                        "contig": contig,
                        "redesign_positions": redesign_positions,
                        "segment_order": segment_order,
                    })

if __name__ == "__main__":
    if not len(sys.argv) == 4:
        print("python write_scaffold_lab_motif_info_csv.py <path_to_reference_pdb_dir> <path_to_motif_csv_file> <path_to_rfdiffusion_contig_info>")
        sys.exit(1)

    input_directory = sys.argv[1]
    output_file = sys.argv[2]
    rfdiffusion_contig_info = sys.argv[3]
    main(input_directory, output_file, rfdiffusion_contig_info)

