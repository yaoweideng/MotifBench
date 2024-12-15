# Check that a motif, and config file are specified
if [ "$#" -ne 1 ]; then
    echo "Usage: ./reindex_all.sh config_file"
    echo "For example: ./reindex_all.sh config.txt"
    exit 1
fi

# Source the configuration file
source "$config_file"

# Ensure necessary variables are set in the config file
if [ -z "$benchmark_dir" ] ; then
    echo "Error: Configuration file is missing necessary settings."
    echo "Ensure it includes 'benchmark_dir'."
    exit 1
fi

test_cases_path=$benchmark_dir"/test_cases.csv"
i=1
cat $test_cases_path | tail -n 30 | while read l; do 
    echo ""
    motif=$(echo $l | awk -F',' '{print $1}')
    motif=$(printf "%02d_$motif" $i)
    motif_residues=$(echo $l | awk -F',' '{print $2}')
    echo $motif $motif_residues
    python reindex_reference_pdbs_and_write_scaffold_info.py $benchmark_dir $motif $motif_residues
    i=$(( i + 1 ))
done 
