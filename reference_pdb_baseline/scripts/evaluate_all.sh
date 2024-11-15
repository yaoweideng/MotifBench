ls | grep -v scripts |  while read l; do 
    if [ ! -f "/home/groups/btrippe/projects/motif_scaffolding/2024_11_07_reference/$l/summary.txt" ]; then
        rm -rf /home/groups/btrippe/projects/motif_scaffolding/2024_11_07_reference/$l
        ./scripts/evaluate_bbs.sh  $l
    else
        echo "$l" already has summary.txt
    fi
done
