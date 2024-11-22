#!/usr/bin/bash
# This script runs evaluate.sh on all motifs in the specified directory.  The
# evaluation for the next motif is launched whenever a next GPU becomes
# available.

gpu_count=8  # Number of GPUs available
i=0
results_bb_dir=/home/groups/btrippe/projects/motif_scaffolding/2024_11_03_rfdiffusion_eval/
log_dir=$results_bb_dir/logs/
mkdir $log_dir
ls $results_bb_dir | while read l; do
    # Find an available GPU by checking for processes using each GPU
    while true; do
        gpu_id=$((i % gpu_count))
        
        # Check if there are any processes running on this GPU
        if ! nvidia-smi -i $gpu_id | grep -q "No running processes found"; then
            # If GPU is busy, increment index to check the next GPU
            i=$((i + 1))
            sleep 1  # Wait for a second before rechecking
            continue
        fi

        # GPU is free; assign job to this GPU and increment index
        echo "Running $l on GPU $gpu_id"
        out_fn=$log_dir/$l.out
        err_fn=$log_dir/$l.err
        CUDA_VISIBLE_DEVICES=$gpu_id ./evaluate_bbs.sh $l $gpu_id >$out_fn 2> $err_fn &
        i=$((i + 1))
        sleep 60  # Add a small delay before starting the next job
        break
    done
done
