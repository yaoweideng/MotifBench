#!/bin/bash

# Check if a file path is provided as an argument
if [ "$#" -ne 3 ]; then
  echo "Usage: $0 config.txt RFdiffusion_dir/ Docker_dir/"
  exit 1
fi

# Source config
config_fn=$1
source $config_fn
if [ -z "$scaffold_base_dir" ] || [ -z "$benchmark_dir" ] ; then
    echo "Error: Configuration file is missing necessary settings."
    echo "Ensure it includes 'scaffold_base_dir' and 'benchmark_dir'"
    exit 1
fi

RFdiffusion_dir=$2
Docker_dir=$2

model_dir=$Docker_dir/models/

example_dir=$benchmark_dir/example/
motif_dir=$benchmark_dir/motif_pdbs/

csv_path=$example_dir/contig_specifications.csv
scripts_dir=$example_dir/run_scripts/
mkdir -p $scripts_dir
log_dir=$scaffold_base_dir/logs/
mkdir -p $log_dir

cat $csv_path | tail -n +2 | while read l; do
    IFS=',' read -r motif_name length contig <<< "$l"
    contig=`echo $contig | tr ";" "/"`
    script_fn=$scripts_dir/run_$motif_name.sh
    output_dir=$scaffold_base_dir/$motif_name/
    mkdir -p $output_dir
    output_prefix=$output_dir/$motif_name
    
    # Command including apptainer call
    slurm_header="#!/usr/bin/bash
#SBATCH --time=12:00:00
#SBATCH -p owners
#SBATCH --gpus=1
#SBATCH -c 4"
    printf "%s\n" "$slurm_header" > $script_fn
    echo "docker_sifs_path=$Docker_dir/" >> $script_fn
    echo "base_dir=$RFdiffusion_dir" >> $script_fn
    std_out=$log_dir/$motif_name.out
    std_err=$log_dir/$motif_name.err
    cmd="apptainer exec --nv \\
      --bind \$base_dir/models:\$base_dir/models \\
      --bind \$base_dir/inputs:\$base_dir/inputs \\
      --bind \$base_dir/outputs:\$base_dir/outputs \\
      \$docker_sifs_path/rfdiffusion.sif \\
      python3 $RFdiffusion_dir/scripts/run_inference.py \\
            inference.output_prefix=$output_prefix \\
            inference.input_pdb=$motif_dir/$motif_name.pdb \\
            contigmap.contigs=[$contig] \\
            contigmap.length=$length-$length \\
            inference.num_designs=100 \\
            inference.model_directory_path=$model_dir \\
            inference.write_trajectory=False >$std_out 2>$std_err"
    printf "%s\n" "$cmd" >> $script_fn

    chmod a+x $script_fn
done
