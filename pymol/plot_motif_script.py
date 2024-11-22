# Script for visualizing motifs in native scaffolds from motif-specs file.  To
# visualize, in pymol run
# run plot_motif_script.py
# plot_motifs("../motif_specs.csv")


import csv

# Predefined list of colors to cycle through
colors = ['red', 'green', 'blue', 'yellow', 'magenta', 'cyan', 'orange',
          'purple', 'salmon', 'lime']

# Function to fetch PDB and color residues
def process_pdb(pdb, ranges, idx=None):
    cmd.fetch(pdb)
    cmd.util.cbc(pdb, first_color=7)
    cmd.set('transparency', 0.6, pdb)

    # Hide everything initially
    cmd.hide('everything', pdb)

    for i, res_range in enumerate(ranges):
        if res_range:
            chain = res_range[0]
            res_range = res_range[1:]
            selection_name = f'{pdb}_range_{i}'
            cmd.select(selection_name, f'model {pdb} and resi {res_range} and chain {chain}')

            # Choose a color from the list, cycling through it
            color = colors[i % len(colors)]
            cmd.color(color, selection_name)

            cmd.center(selection_name)
            cmd.show('sticks', f'{selection_name}')

            # Translate the selection's center of mass to the  origin
            # Calculate center of mass
            com = cmd.centerofmass(selection_name)

            # Delete the selection after applying color and visibility
            cmd.delete(selection_name)

    # Translate the selection's center of mass to the origin
    cmd.translate([-com[0], -com[1], -com[2]], pdb)

    # If idx is not None, rename
    if idx is not None:
        cmd.set_name(pdb, f"{idx:02d}_{pdb}")

def plot_motifs(csv_file):
    # Arrange the structures in a grid view
    cmd.set('grid_mode', 1)

    # Read CSV file
    pdb_index = 0 # index of column with name of csv
    motif_contig_index = 1 # index of column with motif contig
    with open(csv_file, mode='r') as file:
        csv_reader = csv.reader(file)

        for i, row in enumerate(csv_reader):
            if i==0: continue # skip header
            pdb = row[pdb_index]
            ranges = row[motif_contig_index].split(";")
            process_pdb(pdb, ranges, idx=i)
    cmd.hide('everything', f'solvent')
    cmd.orient()
