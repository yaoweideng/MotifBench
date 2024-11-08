ls ../ | grep -v scripts | while read l; do 
    python write_scaffold_lab_motif_info_csv.py ../$l ../$l/motif_info.csv ../../RFDiffusion_baseline/motif_specs_with_contigs_for_motif_files.csv
done 
