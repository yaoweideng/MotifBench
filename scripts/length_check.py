import os
import numpy as np
import logging
import argparse
from pathlib import Path
from typing import Union, Optional, Dict, List

import biotite.structure
import biotite.structure.io as strucio

"""
Check if the uploaded structures require the length specified by the standardized benchmark
Args: "-i", "--input", The input folder to be checked.

Input could be a single folder containing many PDB files for one case,
or a root folder containing many folders for the whole benchmark set. 
"""

logging.basicConfig(level=logging.INFO)


def create_parser():
    parser = argparse.ArgumentParser(description='Input protein folder to process length checking')
    parser.add_argument(
        '-i',
        '--input',
        type=str,
        help='Input protein folder'
    )
    return parser


def get_protein_length(
    pdb_file: Union[str, Path, biotite.structure.AtomArray],
    is_multichain: Optional[bool] = False,
    return_full_information: Optional[bool] = False
) -> Union[int, Dict]:
    """Return the length or plus extended information of a protein, supporting both monomers and multimers.
    Args:
        pdb_file (Union[str, Path, biotite.structure.AtomArray]): The path or biotite.AtomArray object of protein file.
        is_multichain (Optional[bool], optional): Whether want to treat the input protein as a multimer object.
        return_full_information (Optional[bool], optional): Whether return the length of a protein or full {chain ID-residue number-residue name} information.

    Returns:
        `Int`: overall length of input protein if return_full_information is False,
        or `Dict` containing information for length of each corresponding chain otherwise.
    """
    pdb_array = strucio.load_structure(pdb_file) if isinstance(pdb_file, (str, Path)) else pdb_array
    ca_array = pdb_array[(pdb_array.atom_name=="CA")]
    
    chain_dict = {}
    
    if is_multichain:
        for res_num, chain_id, res_name in zip(ca_array.res_id, ca_array.chain_id, ca_array.res_name):
            #print(res_num, chain_id, res_name)
            if chain_id not in chain_dict.keys():
                chain_dict[chain_id] = {}
            chain_dict[chain_id][res_num] = res_name
        for chain_id in chain_dict.keys():
            chain_dict[chain_id]['length'] = int(len(chain_dict[chain_id])) 
    else: # Monomer
        for res_num, res_name in zip(ca_array.res_id, ca_array.res_name):
            chain_dict[res_num] = res_name
            chain_dict['length'] = int(len(ca_array.res_id))
            
    chain_length = {chain: chain_dict[chain]['length'] for chain in chain_dict} if is_multichain else chain_dict['length']
    return chain_length if not return_full_information else chain_dict


PDB_TO_OVERALL_LENGTH = {
 '5TPN': [75],
 '5IUS': [100],
 '3IXT': [75],
 '5YUI': [75],
 '1YCR': [75],
 '2KL8': [100],
 '7MRX': [75],
 '4JHW': [125],
 '4ZYP': [75],
 '5WN9': [75],
 '5TRV': [75],
 '6E6R': [200, 75],
 '6EXZ': [200, 100],
 '7A8S': [100],
 '7AD5': [125],
 '7AHO': [125],
 '7BNY': [125],
 '7DGW': [125],
 '7KUW': [125],
 '7KWW': [125],
 '7MQQ': [125],
 '7S5L': [125],
 '7WRK': [125],
 '6CPA': [200],
 '1MPY': [125],
 '1B73': [125],
 '2RKX': [225],
 '3B5V': [200],
 '4XOJ': [150],
 '1QY3': [225],
 '1LDB': [125],
 '1ITU': [150],
 '1YOV': [75],
 '1A41': [100],
 '1LCC': [150],
 '5ZE9': [100],
 '7UWL': [175],
 '1BCF': [125]
}


def length_check(
    input_folder: Union[str, Path]
):

    for pdb_file in os.listdir(input_folder):
        if ".pdb" not in pdb_file:
            continue

        all_name = os.path.splitext(pdb_file)[0]
        try:
            case_num, backbone_name, sample_num = all_name.split("_") # "01_1BCF_1.pdb"
        except ValueError:
            logging.warning(f"The naming format {all_name} is not as default. \
            Try to use another format.")
            try:
                assert len(all_name.split("_")) == 2, f"{all_name} not following default!"
                backbone_name, sample_num = all_name.split("_") # "1BCF_1.pdb"
                logging.info(f"tested case :{backbone_name}, sample_num: {sample_num}")
            except (ValueError, AssertionError):
                logging.warning(f"The naming format {all_name} is not as default. \
                Try to rename the PDB file to format.")
                for reference_pdb in PDB_TO_OVERALL_LENGTH.keys():
                    if reference_pdb in all_name.upper():
                        backbone_name = reference_pdb

        backbone_name = backbone_name.upper()
        protein_length = get_protein_length(
            pdb_file=os.path.join(input_folder, pdb_file),
            is_multichain=False,
            return_full_information=False
        )

        if int(protein_length) not in PDB_TO_OVERALL_LENGTH[backbone_name]:
            logging.warning(f"The name is not valid. The overall length of designed {backbone_name} should be {PDB_TO_OVERALL_LENGTH[backbone_name]}.")
        else:
            logging.info(f"Passed Length check for {pdb_file}.")
    

if __name__ == "__main__":
    parser = create_parser()
    args = parser.parse_args()

    pdb_files = [f for f in os.listdir(args.input) if f.endswith(".pdb")]
    if not pdb_files:
        logging.info(f"Checking whole benchmark set...")
        case_folders = [case for case in os.listdir(args.input) if os.path.isdir(os.path.join(args.input, case))]
        for folder in case_folders:
            length_check(os.path.join(args.input, folder))
        logging.info(f"Finished processing all directories in {args.input}.")
    else:
        logging.info(f"Checking case {args.input}...")
        length_check(os.path.abspath(args.input))
        logging.info(f"Finished checking all PDB files in {args.input}.")

