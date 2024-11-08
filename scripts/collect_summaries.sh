#!/bin/bash

# Check if a file path is provided as an argument
if [ "$#" -ne 2 ]; then
  echo "Usage: $0 <evaluation_output_dir> <output_csv>"
  exit 1
fi

# Input file containing the list of summary file paths
eval_dir=$1
all_summaries_fn=$eval_dir/all_summary_paths.txt
ls $eval_dir/*/summary.txt > $all_summaries_fn


# Output CSV file
output_file=$2

# Initialize the output CSV file with headers
echo "Path,Protein,Designability_Fraction,Diversity,Novelty_Score" > "$output_file"

# Loop through each summary file path in the input file
while IFS= read -r summary_file; do
  if [ -f "$summary_file" ]; then
    # Extract relevant fields from the summary file
    path=$(awk -F': ' '/evaluation results for/ {print $2}' "$summary_file")
    protein=$(awk -F': ' '/Evaluated Protein/ {print $2}' "$summary_file")
    designability_fraction=$(awk -F': ' '/Designability Fraction/ {gsub("%", "", $2); printf "%.2f", $2}' "$summary_file")
    diversity=$(awk -F': ' '/Diversity/ {printf "%.2f", $2}' "$summary_file")
    novelty_score=$(awk -F': ' '/Novelty Score/ {printf "%.2f", $2}' "$summary_file")

    # Append the extracted information to the output CSV
    echo "$path,$protein,$designability_fraction,$diversity,$novelty_score" >> "$output_file"
  else
    echo "Warning: File $summary_file not found. Skipping..."
  fi
done < "$all_summaries_fn"

echo "Data extraction complete. Results saved to $output_file."

