#!/usr/bin/bash

# Check that a motif and gpu_id are specified
if [ "$#" -ne 2 ]; then
    echo "Usage: ./evaluate_bbs.sh motif_name gpu_id"
    echo "For example: ./evaluate_bbs.sh 00_1BCF 0"
    exit 1
fi
motif_name=$1
gpu_id=$2
echo "running on " $motif_name

# Set paths
benchmark_dir=/home/users/btrippe/projects/motif_scaffolding_benchmark/
output_dir_base=/home/groups/btrippe/projects/motif_scaffolding/2024_11_20_debug/
foldseek_db_path=/home/groups/btrippe/datasets/foldseek/pdb_database/pdb
bb_dir=$benchmark_dir/RFDiffusion_baseline/rfdiffusion_test_run/$motif_name

output_dir=$output_dir_base/$motif_name/
if [ ! -d "$output_dir" ]; then
    mkdir -p "$output_dir"
fi

# Run benchmarking
cd $benchmark_dir/Scaffold-Lab/
python scaffold_lab/motif_scaffolding/motif_refolding.py \
    inference.motif_csv_path=$bb_dir/motif_info.csv \
    inference.backbone_pdb_dir=$bb_dir \
    inference.motif_pdb=$benchmark_dir/motif_pdbs/$motif_name".pdb" \
    inference.output_dir=$output_dir \
    inference.hide_GPU_from_pmpnn=True \
    inference.gpu_id=$gpu_id \
    evaluation.foldseek_database=$foldseek_db_path \
    evaluation.foldseek_cores_for_pdbTM=4
