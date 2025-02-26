import os
import numpy as np
import logging
import argparse
import pandas as pd
from pathlib import Path
from typing import Union
from collections import defaultdict

"""
Check if the number of motif segments exactly match the specification of corresponding test cases.
"-i": The CSV file storing specification of test cases, which is `$ROOT_DIR/test_cases.csv` by default.
"-t": The `motif_info.csv` file to be checked.
If there's an inconsistency, throws an error and exits.
"""

logging.basicConfig(level=logging.INFO)

def create_parser():
    parser = argparse.ArgumentParser(description='Input protein folder to process length checking')
    parser.add_argument(
        '-i',
        '--input',
        type=str,
        help='CSV file storing specifications for test cases'
    )
    parser.add_argument(
        '-t',
        '--test',
        type=str,
        help='`motif_info.csv` to be checked'
    )
    return parser


def check_segment_info(
    cases_info: Union[str, Path, pd.DataFrame],
    motif_info_path: Union[str, Path, pd.DataFrame]
) -> None:

    test_cases = cases_info if isinstance(cases_info, pd.DataFrame) else pd.read_csv(cases_info)
    motif_info = motif_info_path if isinstance(motif_info_path, pd.DataFrame) else pd.read_csv(motif_info_path)

    segment_info = []
    for num, case in test_cases.iterrows():
        formatted_num = '{:02d}'.format(num + 1)
        segment_info.append((f"{formatted_num}_{case['pdb_id']}", len(case['motif_residues'].split(';'))))
    
    segment_dict = defaultdict(int)
    for case_id, segment_num in segment_info:
        segment_dict[case_id] = segment_num

    for _, scaffold in motif_info.iterrows():
        specified_segment = segment_dict[scaffold['pdb_name']]
        actual_segment = len(scaffold['segment_order'].split(';'))
        if specified_segment != actual_segment:
            raise ValueError(f"Inconsistent segment number detected! Sample num: {scaffold['sample_num']}\
                Detected {actual_segment} segment(s), where {scaffold['pdb_name']} should have {specified_segment} segment(s).")
        else:
            pass

    case_name = motif_info_path.split("/")[-2]
    logging.info(f"Number of segments passed checking in {case_name}!")


if __name__ == "__main__":
    parser = create_parser()
    args = parser.parse_args()
    check_segment_info(args.input, args.test)