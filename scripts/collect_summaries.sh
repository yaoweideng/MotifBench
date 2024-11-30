#!/bin/bash

# Check if a file path is provided as an argument
if [ "$#" -ne 2 ]; then
  echo "Usage: $0 <evaluation_output_dir> <output_csv>"
  exit 1
fi

# Input file containing the list of summary file paths
eval_dir=$1
all_summaries_fn=$eval_dir/all_summary_paths.txt
ls $eval_dir/*/esm_summary.txt > $all_summaries_fn

# Output CSV file
output_file=$2

# Initialize the output CSV file with headers
echo "Protein,Num_Solutions,Novelty,Success_rate" > "$output_file"

# Loop through each summary file path in the input file
while IFS= read -r summary_file; do
  if [ -f "$summary_file" ]; then
    # Extract relevant fields from the summary file
    protein=$(awk -F': ' '/Evaluated Protein/ {print $2}' "$summary_file")
    num_solutions=$(awk -F': ' '/Number of distinct solutions/ {print $2}' "$summary_file")
    novelty=$(awk -F': ' '/Novelty/ {printf "%.3f", $2}' "$summary_file")
    success_rate=$(awk -F': ' '/Success rate/ {gsub("%", "", $2); printf "%.2f", $2}' "$summary_file")

    # Append the extracted information to the output CSV
    echo "$protein,$num_solutions,$novelty,$success_rate" >> "$output_file"
  else
    echo "Warning: File $summary_file not found. Skipping..."
  fi
done < "$all_summaries_fn"

echo "Data extraction complete. Results saved to $output_file."

