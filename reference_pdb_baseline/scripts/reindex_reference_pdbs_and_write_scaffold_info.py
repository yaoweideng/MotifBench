"""Initial ChatGPT prompt.
Write a python script with a function that takes as input:
1. a path to a pdb file (e.g. example.pdb) and,
2. a string specifying ranges of residues on one of the chains (e.g. "F63-69;F196-212").
3. a path to write a cleaned pdb file (e.g. output.pdb)

The function should:
1. find the index of the first residue in the specified chain (in this example, chain F), say this is residue index "N".  And the overall length of the chain say "L" residues.
2. Save a new pdb file to the specified output that includes only the specified chain (F).  But first (1) relabel this chain so that it is chain A, (2) reindex the residues to start at index 1 and end at residue L (so "FN" becomes "A1"), and (3) remove all atoms that are not part of amino acids.
3. Create and return a new string that indicates where the residue ranges are in the new pdb file.  The format should give the lengths of the regions that pad and fill gaps between the specified residue ranges, and label the residue ranges as "A", "B", "C" etc.  For example, if in example.pdb the first residue is N=11 and the total length is 210, the string should be ("52/A/126/B/8" because 63-10-1 =52, 196-69+1=126, and 210+10-212=8).
"""
import re
import sys
import os

def process_pdb(input_pdb_path, residue_ranges, output_pdb_path):
    """
    Process a PDB file to relabel and extract specified chains and residues.

    Args:
        input_pdb_path (str): Path to the input PDB file.
        residue_ranges (str): String specifying residue ranges (e.g., "F63-69;F196-212").
        output_pdb_path (str): Path to write the cleaned PDB file.

    Returns:
        str: New string indicating the reindexed residue ranges.
    """
    # Parse the residue ranges string
    chain = residue_ranges[0]# Extract chain ID from the first range
    residue_ranges_list = []
    for res_range in residue_ranges.split(";"):
        if "-" in res_range:
            start, end = res_range[1:].split("-")
        else:
            start = end = res_range[1:]
        residue_ranges_list.append((int(start), int(end)))
    residue_ranges = residue_ranges_list

    # Read the PDB file and extract relevant data
    with open(input_pdb_path, 'r') as file:
        pdb_lines = file.readlines()

    # Filter lines to keep only the specified chain and amino acids
    relevant_lines = []
    first_residue_index = None
    last_residue_index = None
    residue_indices = set()
    for line in pdb_lines:
        if line.startswith("ATOM"):
            if line[21] == chain:  # Check if the chain matches
                residue_index = int(line[22:26].strip())
                if first_residue_index is None or residue_index < first_residue_index:
                    first_residue_index = residue_index
                if last_residue_index is None or residue_index > last_residue_index:
                    last_residue_index = residue_index
                residue_indices.add(residue_index)
                relevant_lines.append(line)

    if first_residue_index is None or last_residue_index is None:
        raise ValueError(f"Chain {chain} not found in {input_pdb_path}.")

    # Check for gaps in the input PDB file
    sorted_residues = sorted(residue_indices)
    for i in range(1, len(sorted_residues)):
        if sorted_residues[i] > sorted_residues[i - 1] + 1:
            print(
                f"Warning: Gap detected in chain {chain} between residues "
                f"{sorted_residues[i - 1]} and {sorted_residues[i]}."
            )


    # Reindex and relabel the chain to chain A
    reindexed_lines = []
    residue_mapping = {}
    new_residue_index = 1
    for line in relevant_lines:
        residue_index = int(line[22:26].strip())
        if residue_index not in residue_mapping:
            residue_mapping[residue_index] = new_residue_index
            new_residue_index += 1
        new_line = (
            line[:21] + "A" +  # Relabel chain to A
            f"{residue_mapping[residue_index]:>4}" + line[26:]  # Reindex residue
        )
        reindexed_lines.append(new_line)

    # Save the cleaned PDB file
    with open(output_pdb_path, 'w') as file:
        file.writelines(reindexed_lines)

    # Calculate the reindexed residue ranges
    padded_regions = []
    last_end = 0
    range_labels = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    range_strings = []
    for idx, (start, end) in enumerate(residue_ranges):
        new_start = residue_mapping[start]
        new_end = residue_mapping[end]
        padding_before = new_start - last_end - 1
        #if padding_before > 0:
        #    padded_regions.append(str(padding_before))
        range_strings.append(f"{padding_before}/{range_labels[idx]}")
        last_end = new_end
    padding_after = len(residue_mapping) - last_end
    if padding_after > 0:
        #padded_regions.append(str(padding_after))
        range_strings.append(str(padding_after))

    #return "/".join(padded_regions + range_strings)
    return "/".join(range_strings)

def main(base_dir, motif, residue_ranges):

    motif_name = motif[3:]
    input_pdb = f"{base_dir}/reference_pdbs/{motif_name}.pdb"
    output_dir = f"{base_dir}/reference_pdb_baseline/{motif}"
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
    output_pdb = f"{output_dir}/{motif}_0.pdb"
    result = process_pdb(input_pdb, residue_ranges, output_pdb)
    scaffold_info_fn = f"{output_dir}/scaffold_info.csv"
    with open(scaffold_info_fn, 'w') as f:
        f.write("sample_num,motif_placements\n")
        f.write(f"0,{result}")

    print("Resulting range string:", result)

if __name__ == "__main__":
    if not len(sys.argv) == 4:
        print("python reindex_reference_pdbs_and_write_scaffold_info.py " 
                "<benchmark_path> <motif> <contig>")
        sys.exit(1)

    benchmark_path = sys.argv[1]
    motif = sys.argv[2]
    residue_ranges = sys.argv[3]
    main(benchmark_path, motif, residue_ranges)
