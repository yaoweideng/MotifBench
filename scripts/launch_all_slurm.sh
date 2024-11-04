eval_results_dir=/home/groups/btrippe/projects/motif_scaffolding/2024_11_03_rfdiffusion_eval/
results_bb_dir=/home/users/btrippe/projects/motif_scaffolding_benchmark/RFDiffusion_baseline/rfdiffusion_test_run
log_dir=$eval_results_dir/logs/
mkdir $log_dir
ls $results_bb_dir | while read motif_name; do
    out_fn=$log_dir/$motif_name.%j.out
    err_fn=$log_dir/$motif_name.%j.err
    sbatch --output=$out_fn --error=$err_fn ./evaluate_bbs.sh $motif_name
done
