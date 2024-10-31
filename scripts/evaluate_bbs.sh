#!/bin/bash

# Check if exactly one argument is provided
if [ "$#" -ne 1 ]; then
    echo "Usage: ./evaluate_bbs.sh motif_name"
    echo "For example: ./evaluate_bbs.sh 00_1BCF"
    exit 1
fi
motif_name=$1
bb_dir=/projects/m000018/projects/RFDiffusion_benchmarking/test4/$motif_name/
motif_csv=/projects/m000018/projects/RFDiffusion_benchmarking/test4/$motif_name/motif_info.csv


# Set up paths 
foldseek_db_path=/projects/m000018/data/foldseek/pdb
script_dir=/users/btrippe/projects/motif_scaffolding_benchmark/Scaffold-Lab/
motif_dir=/users/btrippe/projects/motif_scaffolding_benchmark/motif_pdbs/

output_dir_base=/projects/m000018/projects/RFDiffusion_benchmarking/test4_eval/
output_dir=$output_dir_base/$motif_name/
mkdir $output_dir

# Run benchmarking
echo "running on " $motif_name
cd $script_dir
# >>> conda initialize >>>
# !! Contents within this block are managed by 'conda init' !!
__conda_setup="$('/cm/shared/apps/Mambaforge/24.3.0-0/bin/conda' 'shell.bash' 'hook' 2> /dev/null)"
if [ $? -eq 0 ]; then
    eval "$__conda_setup"
else
    if [ -f "/cm/shared/apps/Mambaforge/24.3.0-0/etc/profile.d/conda.sh" ]; then
        . "/cm/shared/apps/Mambaforge/24.3.0-0/etc/profile.d/conda.sh"
    else
        export PATH="/cm/shared/apps/Mambaforge/24.3.0-0/bin:$PATH"
    fi
fi
unset __conda_setup
# <<< conda initialize <<<
conda activate scaffold-lab
python scaffold_lab/motif_scaffolding/motif_refolding.py \
    inference.motif_csv_path=$motif_csv \
    inference.backbone_pdb_dir=$bb_dir \
    inference.native_pdbs_dir=$motif_dir \
    inference.output_dir=$output_dir \
    inference.hide_GPU_from_pmpnn=True \
    evaluation.foldseek_database=$foldseek_db_path \
    evaluation.foldseek_cores_for_pdbTM=4
