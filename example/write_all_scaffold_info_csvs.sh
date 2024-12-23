# Check that config file is specified
if [ "$#" -ne 1 ]; then
    echo "Usage: ./write_all_scaffold_info_csvs.sh <config.txt>"
    exit 1
fi

# Source the configuration file
config_path=$1
source "$config_path"

# Ensure scaffold_base_dir is defined
if [ -z "$scaffold_base_dir" ] ; then 
    echo "Error: Configuration file is missing necessary settings."
    echo "Ensure it includes 'scaffold_base_dir' and 'python_path"
    exit 1
fi

ls $scaffold_base_dir | while read l; do
	$python_path write_scaffold_info.py $scaffold_base_dir/$l $scaffold_base_dir/$l/scaffold_info.csv contig_specifications.csv
done

