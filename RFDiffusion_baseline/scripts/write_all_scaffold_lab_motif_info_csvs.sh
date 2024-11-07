rfdiffusion_outputs_base=/projects/m000018/projects/RFDiffusion_benchmarking/test4/
ls $rfdiffusion_outputs_base | while read l; do
	python write_scaffold_lab_motif_info_csv.py $rfdiffusion_outputs_base/$l  $rfdiffusion_outputs_base/$l/motif_info.csv  ../motif_specs_with_contigs_for_motif_files.csv
done
