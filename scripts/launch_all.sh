# Check that a motif, and config file are specified
if [ "$#" -ne 1 ]; then
    echo "Usage: ./launch_all_slurm.sh <config.txt>"
    exit 1
fi
# Source the configuration file
config_path=$1
source "$config_path"

# Ensure necessary variables are set in the config file
if [ -z "$scaffold_base_dir" ] || [ -z "$foldseek_db_path" ] || [ -z \
    "$base_output_dir" ] || [ -z "$benchmark_dir" ] ; then
    echo "Error: Configuration file is missing necessary settings."
    echo "Ensure it includes 'scaffold_base_dir', 'foldseek_db_path', \
        'base_output_dir', and 'benchmark_dir'."
    exit 1
fi
log_dir=$base_output_dir/logs/
mkdir -p $log_dir
ls $scaffold_base_dir | grep -E '^[0-9]{2}_.{4}$' | while read motif_name; do
    out_fn=$log_dir/$motif_name.%j.out
    err_fn=$log_dir/$motif_name.%j.err
    sbatch --output=$out_fn --error=$err_fn $benchmark_dir/scripts/evaluate_bbs.sh $motif_name $config_path
done
