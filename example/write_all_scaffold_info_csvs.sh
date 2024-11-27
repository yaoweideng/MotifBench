rfdiffusion_outputs_base=/home/groups/btrippe/projects/motif_scaffolding/2024_11_26/rfdiffusion/
ls $rfdiffusion_outputs_base | while read l; do
	python write_scaffold_info.py $rfdiffusion_outputs_base/$l $rfdiffusion_outputs_base/$l/scaffold_info.csv
done
