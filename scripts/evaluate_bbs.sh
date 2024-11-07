#!/usr/bin/bash
#SBATCH --time=12:00:00
#SBATCH -p gpu
#SBATCH --gpus=1
#SBATCH -c 4
#SBATCH --mem=128GB

# Check if exactly one argument is provided
if [ "$#" -ne 1 ]; then
    echo "Usage: ./evaluate_bbs.sh motif_name"
    echo "For example: ./evaluate_bbs.sh 00_1BCF"
    exit 1
fi
motif_name=$1
gpu_id=0
benchmark_dir=/home/users/btrippe/projects/motif_scaffolding_benchmark/

bbs_base_dir=$benchmark_dir/RFDiffusion_baseline/rfdiffusion_test_run/
bb_dir=$bbs_base_dir/$motif_name/
motif_csv=$bb_dir/motif_info.csv

# Set up paths 
foldseek_db_path=/home/groups/btrippe/datasets/foldseek/pdb_database/pdb
script_dir=$benchmark_dir/Scaffold-Lab/
motif_pdb=$benchmark_dir/motif_pdbs/$motif_name".pdb"

output_dir_base=/home/groups/btrippe/projects/motif_scaffolding/2024_11_03_rfdiffusion_eval/
output_dir=$output_dir_base/$motif_name/
mkdir $output_dir

# Run benchmarking
echo "running on " $motif_name
cd $script_dir

# >>> conda initialize >>>
# !! Contents within this block are managed by 'conda init' !!
__conda_setup="$('/home/groups/btrippe/miniconda3/bin/conda' 'shell.bash' 'hook' 2> /dev/null)"
if [ $? -eq 0 ]; then
    eval "$__conda_setup"
else
    if [ -f "/home/groups/btrippe/miniconda3/etc/profile.d/conda.sh" ]; then
        . "/home/groups/btrippe/miniconda3/etc/profile.d/conda.sh"
    else
        export PATH="/home/groups/btrippe/miniconda3/bin:$PATH"
    fi
fi
unset __conda_setup
# <<< conda initialize <<<
conda activate scl
python scaffold_lab/motif_scaffolding/motif_refolding.py \
    inference.motif_csv_path=$motif_csv \
    inference.backbone_pdb_dir=$bb_dir \
    inference.motif_pdb=$motif_pdb \
    inference.output_dir=$output_dir \
    inference.hide_GPU_from_pmpnn=True \
    inference.gpu_id=$gpu_id \
    evaluation.foldseek_database=$foldseek_db_path \
    evaluation.foldseek_cores_for_pdbTM=4
