#!/bin/bash
path=/users/btrippe/projects/motif_scaffolding_benchmark/RFDiffusion_baseline/
scripts_dir=$path/scripts/run_scripts/
motif_dir=/users/btrippe/projects/motif_scaffolding_benchmark/motif_pdbs/
csv_path=$path/motif_specs_with_contigs_for_motif_files.csv
model_dir=/users/btrippe/projects/motif_scaffolding_benchmark/RFDiffusion_baseline/RFdiffusion/models/
apptainer_dir=/projects/m000018/docker/


cat $csv_path | while read l; do
    IFS=',' read -r motif_name length contig <<< "$l"
    contig=`echo $contig | tr ";" "/"`
    script_fn=$scripts_dir/run_$motif_name.sh
    echo "#!/bin/bash" > $script_fn
    echo "cd $apptainer_dir" >> $script_fn
    output_dir=/projects/m000018/projects/RFDiffusion_benchmarking/test4/$motif_name
    mkdir -p $output_dir
    output_prefix=$output_dir/${motif_name:3:7}
    
    # Command including apptainer call
    #cmd="echo python3 $path/run_inference.py inference.output_prefix=$output_prefix inference.input_pdb=$motif_dir/$motif_name.pdb contigmap.contigs=[$contig] contigmap.length=$length-$length inference.num_designs=100 inference.model_directory_path=$model_dir inference.write_trajectory=False | bash $path/apptainer_shell.sh" 
    log_dir=/projects/m000018/projects/RFDiffusion_benchmarking/logs/test4/
    std_out=$log_dir/$motif_name.out
    std_err=$log_dir/$motif_name.err
    
    cmd="python3 $path/run_inference.py inference.output_prefix=$output_prefix inference.input_pdb=$motif_dir/$motif_name.pdb contigmap.contigs=[$contig] contigmap.length=$length-$length inference.num_designs=100 inference.model_directory_path=$model_dir inference.write_trajectory=False >$std_out 2>$std_err &" 
    echo $cmd >> $script_fn
    chmod a+x $script_fn
done
