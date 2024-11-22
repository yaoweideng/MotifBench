eval_results_dir=/home/groups/btrippe/projects/motif_scaffolding/2024_11_10_rfdiffusion_updates/
results_bb_dir=/home/users/btrippe/projects/motif_scaffolding_benchmark/RFDiffusion_baseline/rfdiffusion_test_run
log_dir=$eval_results_dir/logs/2024_11_12/
mkdir -p $log_dir
ls $results_bb_dir | while read motif_name; do
    out_fn=$log_dir/$motif_name.%j.out
    err_fn=$log_dir/$motif_name.%j.err
    gpu_id=0
    sbatch --output=$out_fn --error=$err_fn ./evaluate_bbs.sh $motif_name $gpu_id
done
