import pandas as pd
import numpy as np
import argparse

def main(test_cases_file, summary_by_case_file, summary_by_group_file):
    # Load the input files
    test_cases = pd.read_csv(test_cases_file)
    test_cases['idx'] = [i+1 for i in range(len(test_cases))]     
    group_by_idx = {row[1]["idx"]:row[1]['group'] for row in
            test_cases.iterrows()}
    summary_by_case = pd.read_csv(summary_by_case_file)
    summary_by_case['group'] = [group_by_idx[int(row[1]['Problem'].split("_")[0])]
            for row in summary_by_case.iterrows()]

    # Group by the "group" column and calculate the required statistics
    summary_by_group = summary_by_case.groupby('group').agg(
        Number_Solved=('Num_Solutions', lambda x: (x > 0).sum()),
        Mean_Num_Solutions=('Num_Solutions', 'mean'),
        Mean_Novelty=('Novelty', 'mean'),
        Mean_Success_rate=('Success_rate', 'mean')
    ).reset_index()

    # Rename columns to match the specified format
    summary_by_group.rename(columns={'group': 'Group'}, inplace=True)

    # Add summary column with that incorporates information across groups
    summary_by_group.loc[len(summary_by_group)] = {
        "Group": "overall",
        "Number_Solved": np.sum(summary_by_group["Number_Solved"]),
        "Mean_Num_Solutions": np.mean(summary_by_group["Mean_Num_Solutions"]),
        "Mean_Novelty": np.mean(summary_by_group["Mean_Novelty"]),
        "Mean_Success_rate": np.mean(summary_by_group["Mean_Success_rate"]),
    }

    # Save the output to a new CSV file
    summary_by_group.to_csv(summary_by_group_file, float_format='%.2f', index=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process test_cases and summary_by_case files to generate group-level statistics.")
    parser.add_argument("test_cases_file", help="Path to the test_cases.csv file")
    parser.add_argument("summary_by_case_file", help="Path to the summary_by_case.csv file")
    parser.add_argument("summary_by_group_file", help="Path to the summary_by_group.csv file")

    args = parser.parse_args()

    main(args.test_cases_file, args.summary_by_case_file,
            args.summary_by_group_file)
