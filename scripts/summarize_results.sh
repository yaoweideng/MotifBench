#!/bin/bash

# Check if a file path and method are provided as arguments
if [ "$#" -ne 2 ]; then
  echo "Usage: $0 config.txt method"
  echo "method: esmfold, alphafold2, or both"
  exit 1
fi

# Source config
config_fn=$1
method=$2
source $config_fn

# Function to summarize results
summarize_results() {
  local method_prefix=$1
  local summary_by_case_fn=$base_output_dir/${method_prefix}_summary_by_problem.csv
  local summary_by_group_fn=$base_output_dir/${method_prefix}_summary_by_group.csv

  # Initialize csv file for results by case with header
  echo "Problem,Num_Solutions,Novelty,Success_rate" > "$summary_by_case_fn"

  # Loop through each summary file path in the input file
  ls $base_output_dir/*/${method_prefix}_summary.txt | while IFS= read -r summary_file; do
    if [ -f "$summary_file" ]; then
      # Extract relevant fields from the summary file
      protein=$(grep -oP 'Evaluated Protein\s*\|\s*\K\S+' "$summary_file")
      num_solutions=$(grep -oP 'Number of Unique Solutions\s*\(.*\)\s*\|\s*\K\d+' "$summary_file")
      novelty=$(grep -oP 'Novelty.*\|\s*\K[\d.]+' "$summary_file")
      success_rate=$(grep -oP 'Success Rate\s*\|\s*\K[\d.]+(?=%)' "$summary_file")

      # Append the extracted information to the output CSV
      echo "$protein,$num_solutions,$novelty,$success_rate" >> $summary_by_case_fn
    else
      echo "Warning: File $summary_file not found. Skipping..."
    fi
  done
  echo "Summary results by case written to $summary_by_case_fn"

  test_cases_fn=$benchmark_dir/test_cases.csv
  python $benchmark_dir/scripts/write_summary_by_group.py $test_cases_fn $summary_by_case_fn $summary_by_group_fn
  echo "Summary results by group written to $summary_by_group_fn"
}

# Summarize results based on the specified method
case $method in
  esmfold)
    summarize_results "esm"
    ;;
  alphafold2)
    summarize_results "af2"
    ;;
  esmfold_alphafold2)
    summarize_results "esm"
    summarize_results "af2"
    ;;
  *)
    echo "Invalid method specified. Use esmfold, alphafold2, or esmfold_alphafold2."
    exit 1
    ;;
esac
