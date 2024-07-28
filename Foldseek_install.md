# Foldseek for novelty computation notes

### Install 
Download from here (https://github.com/steineggerlab/foldseek) with:
```
# Conda installer (Linux and macOS)
conda install -c conda-forge -c bioconda foldseek
```

### Downloading PDB database
* `foldseek databases PDB pdb tmp`
* downloads pdb database files and dumps them into current directory.

### Search for tmscore to pdb hits
* Run search against pdb with
`foldseek easy-search <query.pdb> <path_to_directory_with_database_files/pdb> <output.tsv> <path_to_arbitrary_temp_dir_for_reading_and_writing_intermediate_scratch_results> --format-output "query,target,qaln,taln,alntmscore"`
* We can then take maximum tmscore value in final column of output results

### TODO:
* Test time for querying for estimate to put into write-up.
* Check that faster with list of query pdb files.


Observation: in a test of comparing the original TMAlign tmscore implementation to the TMscore returned by foldseek, on the case tested the Foldseek TMscore was 0.844 but the TMalign score was 0.808 (so inflated by 0.036).  This may be significant and worth discussion...
