import pandas as pd
import argparse

def main(motif_specs_file, summary_by_case_file, summary_by_group_file):
    # Load the input files
    motif_specs = pd.read_csv(motif_specs_file)
    motif_specs['idx'] = [i+1 for i in range(len(motif_specs))]     
    group_by_idx = {row[1]["idx"]:row[1]['group'] for row in
            motif_specs.iterrows()}
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

    # Save the output to a new CSV file
    summary_by_group.to_csv(summary_by_group_file, float_format='%.2f', index=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process motif_specs and summary_by_case files to generate group-level statistics.")
    parser.add_argument("motif_specs_file", help="Path to the motif_specs.csv file")
    parser.add_argument("summary_by_case_file", help="Path to the summary_by_case.csv file")
    parser.add_argument("summary_by_group_file", help="Path to the summary_by_group.csv file")

    args = parser.parse_args()

    main(args.motif_specs_file, args.summary_by_case_file,
            args.summary_by_group_file)
