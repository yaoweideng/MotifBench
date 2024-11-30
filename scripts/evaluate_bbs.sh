#!/usr/bin/bash
#SBATCH --time=12:00:00
#SBATCH -p gpu
#SBATCH --gpus=1
#SBATCH -c 4
#SBATCH --mem=128GB

# Check that a motif, and config file are specified
if [ "$#" -ne 2 ]; then
    echo "Usage: ./evaluate_bbs.sh motif_name config_file"
    echo "For example: ./evaluate_bbs.sh 01_1LDB config.txt"
    exit 1
fi

motif_name=$1
config_file=$2
echo "Running on motif: $motif_name"

# Check if the configuration file exists
if [ ! -f "$config_file" ]; then
    echo "Error: Configuration file '$config_file' does not exist."
    exit 1
fi

# Source the configuration file
source "$config_file"

# Ensure necessary variables are set in the config file
if [ -z "$scaffold_base_dir" ] || [ -z "$foldseek_db_path" ] || [ -z \
    "$base_output_dir" ] || [ -z "$benchmark_dir" ] ; then
    echo "Error: Configuration file is missing necessary settings."
    echo "Ensure it includes 'scaffold_base_dir', 'foldseek_db_path', \
        'base_output_dir', and 'benchmark_dir'."
    exit 1
fi

# Set derived paths
output_dir=$base_output_dir/$motif_name/
bb_dir=$scaffold_base_dir/$motif_name

# Create output directory if it doesn't exist
if [ ! -d "$output_dir" ]; then
    mkdir -p "$output_dir"
fi

# Make motif_info.csv from scaffold_info.csv
motif_pdb_path=$benchmark_dir/motif_pdbs/$motif_name".pdb"
python $benchmark_dir/scripts/write_motifInfo_from_scaffoldInfo.py \
    $bb_dir/scaffold_info.csv $motif_pdb_path $bb_dir/motif_info.csv

# Run Scaffold-Lab for evaluation
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
python $benchmark_dir/Scaffold-Lab/scaffold_lab/motif_scaffolding/motif_refolding.py \
    inference.motif_csv_path=$bb_dir/motif_info.csv \
    inference.backbone_pdb_dir=$bb_dir \
    inference.motif_pdb=$motif_pdb_path \
    inference.output_dir=$output_dir \
    evaluation.foldseek_database=$foldseek_db_path
