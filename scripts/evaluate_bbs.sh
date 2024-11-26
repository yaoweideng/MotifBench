#!/usr/bin/bash

# Check that a motif, gpu_id, and config file are specified
if [ "$#" -ne 3 ]; then
    echo "Usage: ./evaluate_bbs.sh motif_name gpu_id config_file"
    echo "For example: ./evaluate_bbs.sh 00_1BCF 0 config.txt"
    exit 1
fi

motif_name=$1
gpu_id=$2
config_file=$3

# Check if the configuration file exists
if [ ! -f "$config_file" ]; then
    echo "Error: Configuration file '$config_file' does not exist."
    exit 1
fi

# Source the configuration file
source "$config_file"

# Ensure necessary variables are set in the config file
if [ -z "$benchmark_dir" ] || [ -z "$foldseek_db_path" ] || [ -z "$base_output_dir" ]; then
    echo "Error: Configuration file is missing necessary settings."
    echo "Ensure it includes 'benchmark_dir', 'foldseek_db_path', and 'base_output_dir'."
    exit 1
fi

echo "Running on motif: $motif_name with GPU ID: $gpu_id"

# Set derived paths
output_dir=$base_output_dir/$motif_name/
bb_dir=$benchmark_dir/RFDiffusion_baseline/rfdiffusion_test_run/$motif_name

# Create output directory if it doesn't exist
if [ ! -d "$output_dir" ]; then
    mkdir -p "$output_dir"
fi

# Make motif_info.csv from scaffold_info.csv
motif_pdb_path=$benchmark_dir/motif_pdbs/$motif_name".pdb"
echo $benchmark_dir/scripts/write_motifInfo_from_scaffoldInfo.py  $bb_dir/scaffold_info.csv  $motif_pdb_path $bb_dir/motif_info_update.csv 
$benchmark_dir/scripts/write_motifInfo_from_scaffoldInfo.py  $bb_dir/scaffold_info.csv  $motif_pdb_path $bb_dir/motif_info.csv 


# Run benchmarking
cd $benchmark_dir/Scaffold-Lab/
python scaffold_lab/motif_scaffolding/motif_refolding.py \
    inference.motif_csv_path=$bb_dir/motif_info.csv \
    inference.backbone_pdb_dir=$bb_dir \
    inference.motif_pdb=$motif_pdb_path \
    inference.output_dir=$output_dir \
    inference.gpu_id=$gpu_id \
    evaluation.foldseek_database=$foldseek_db_path
