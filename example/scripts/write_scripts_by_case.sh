#!/bin/bash
benchmark_dir=/home/users/btrippe/projects/motif_scaffolding_benchmark/
example_dir=$benchmark_dir/example/
output_base=/home/groups/btrippe/projects/motif_scaffolding/2024_11_26/rfdiffusion/
motif_dir=$benchmark_dir/motif_pdbs/
rfdiffusion_source_dir=/home/users/btrippe/projects/motif_scaffolding_benchmark_original/RFDiffusion_baseline/RFdiffusion/

csv_path=$example_dir/contig_specifications.csv
scripts_dir=$example_dir/scripts/run_scripts/
model_dir=$rfdiffusion_source_dir/models/
log_dir=$output_base/logs/
mkdir -p $log_dir

cat $csv_path | while read l; do
    IFS=',' read -r motif_name length contig <<< "$l"
    contig=`echo $contig | tr ";" "/"`
    script_fn=$scripts_dir/run_$motif_name.sh
    output_dir=$output_base/$motif_name/
    mkdir -p $output_dir
    output_prefix=$output_dir/$motif_name
    
    # Command including apptainer call
    #cmd="echo python3 $path/run_inference.py inference.output_prefix=$output_prefix inference.input_pdb=$motif_dir/$motif_name.pdb contigmap.contigs=[$contig] contigmap.length=$length-$length inference.num_designs=100 inference.model_directory_path=$model_dir inference.write_trajectory=False | bash $path/apptainer_shell.sh" 
    slurm_header="#!/usr/bin/bash
#SBATCH --time=12:00:00
#SBATCH -p gpu
#SBATCH --gpus=1
#SBATCH -c 4"
    printf "%s\n" "$slurm_header" > $script_fn
    echo "export NGC_API_KEY=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" >> $script_fn
    echo "docker_sifs_path=$GROUP_HOME/docker/" >> $script_fn
    echo "base_dir=/home/users/btrippe/projects/motif_scaffolding_benchmark_original/RFDiffusion_baseline/RFdiffusion/" >> $script_fn
    std_out=$log_dir/$motif_name.out
    std_err=$log_dir/$motif_name.err
    cmd="apptainer exec --nv \\
      --bind \$base_dir/models:\$base_dir/models \\
      --bind \$base_dir/inputs:\$base_dir/inputs \\
      --bind \$base_dir/outputs:\$base_dir/outputs \\
      --env NGC_API_KEY=\$NGC_API_KEY \\
      \$docker_sifs_path/rfdiffusion.sif \\
      python3 $example_dir/run_inference.py \\
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
