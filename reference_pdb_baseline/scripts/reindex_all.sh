benchmark_dir="/home/users/btrippe/projects/motif_scaffolding_benchmark/"
motif_specs_path="../../motif_specs.csv"
i=1
cat $motif_specs_path | tail -n 30 | while read l; do 
    echo ""
    motif=$(echo $l | awk -F',' '{print $1}')
    motif=$(printf "%02d_$motif" $i)
    contig=$(echo $l | awk -F',' '{print $2}')
    echo $motif $contig
    python reindex_reference_pdbs_and_write_scaffold_info.py $benchmark_dir $motif $contig
    i=$(( i + 1 ))
done 
