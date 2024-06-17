import csv

# Function to fetch PDB and color residues
def process_pdb(pdb, ranges):
    cmd.fetch(pdb)
    cmd.color('green', pdb)
    for i, res_range in enumerate(ranges):
        if res_range:
            chain = res_range[0]
            res_range = res_range[1:]
            print("pdb, range:", pdb, res_range)
            selection_name = f'{pdb}_range_{i}'
            cmd.select(selection_name, f'model {pdb} and resi {res_range} and chain {chain}')
            cmd.color('red', selection_name)
            cmd.center(selection_name)
            cmd.show('sticks', f'{selection_name}')

    # Translate the selection's center of mass to the  origin
    # Calculate center of mass
    com = cmd.centerofmass(selection_name)

    # Translate the selection's center of mass to the origin
    cmd.translate([-com[0], -com[1], -com[2]], pdb)

def plot_motifs(csv_file):
    # Arrange the structures in a grid view
    cmd.set('grid_mode', 1)

    # Read CSV file
    with open(csv_file, mode='r') as file:
        csv_reader = csv.reader(file)
        header = next(csv_reader)
        pdb_index = header.index('PDB')
        ranges_indices = [header.index(col) for col in header if 'double contig' in col]

        for row in csv_reader:
            pdb = row[pdb_index]
            ranges = [row[i] for i in ranges_indices]
            process_pdb(pdb, ranges)
    cmd.hide('everything', f'solvent')
    cmd.orient()
