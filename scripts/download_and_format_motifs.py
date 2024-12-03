import os
import shutil
import urllib.request
import numpy as np
from Bio.PDB import PDBParser, Select, Chain, Structure, Model, PDBIO

motif_chain_id_order = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

def parse_contig_string(contig_string):
    contig_segments = []
    for motif_segment in contig_string.split(";"):
        segment_dict = {"chain": motif_segment[0]}
        if "-" in motif_segment:
            segment_dict["start"], segment_dict["end"] = map(int, motif_segment[1:].split("-"))
        else:
            segment_dict["start"] = segment_dict["end"] = int(motif_segment[1:])
        contig_segments.append(segment_dict)
    return contig_segments

def check_if_in_segment(segments, chain, residue):
    for segment in segments:
        if segment["chain"] == chain and segment["start"] <= residue <= segment["end"]:
            return True
    return False

class AltLocSelect(Select):
    def accept_atom(self, atom):
        return atom.altloc in ('A', ' ') and atom.occupancy == 1.0

def remove_alt_conformations(structure):
    for model in structure:
        for chain in model:
            for residue in chain:
                atoms_to_remove = [atom for atom in residue if atom.altloc not in ('A', ' ')]
                for atom in atoms_to_remove:
                    if len([a for a in residue if a.get_name() == atom.get_name()]) > 1:
                        residue.detach_child(atom.id)
                for atom in residue:
                    atom.set_altloc(' ')
                    atom.set_occupancy(1.0)
    return structure

def load_pdb(pdb_id, reference_pdb_dir="./reference_pdbs/"):
    pdb_fn = os.path.join(reference_pdb_dir, f"{pdb_id}.pdb")
    if pdb_id != "1QY3":
        urllib.request.urlretrieve(f"http://files.rcsb.org/download/{pdb_id}.pdb", pdb_fn)
    else:
        # If 1QY3, use modified pdb file with reversion of R96A mutation.
        pdb_fn = "../test_cases/ESM3/1qy3_A96R.pdb"
    parser = PDBParser()
    return parser.get_structure(pdb_id, pdb_fn)

def parse_motif_into_new_structure(structure, motif_segments, redesign_segments):
    motif_structure = Structure.Structure("motif")
    motif_structure.add(Model.Model(0))
    for i, segment in enumerate(motif_segments):
        chain = Chain.Chain(motif_chain_id_order[i])
        motif_structure[0].add(chain)
        for residue in structure[0][segment["chain"]]:
            if segment["start"] <= residue.id[1] <= segment["end"]:
                for atom in list(residue):
                    if atom.element == "H": residue.detach_child(atom.id)
                if check_if_in_segment(redesign_segments, segment["chain"], residue.id[1]):
                    for atom in list(residue):
                        if atom.id not in ["N", "CA", "C", "O"]:
                            residue.detach_child(atom.id)
                    residue.resname = "UNK"
                residue = residue.copy()
                residue.id = (" ", residue.id[1] - segment["start"] + 1, " ")
                chain.add(residue)
    return motif_structure

def center_pdb(motif_fn):
    parser = PDBParser()
    structure = parser.get_structure("motif", motif_fn)
    com = np.mean([atom.coord for atom in structure.get_atoms()], axis=0)
    for atom in structure.get_atoms():
        atom.set_coord(atom.coord - com)
    io = PDBIO()
    io.set_structure(structure)
    io.save(motif_fn)

def build_contig_string(structure, motif_segments):
    first_residue = next(res.id[1] for res in structure[0][motif_segments[0]["chain"]] if res.id[1] != " ")
    contig_string = ""
    for i, segment in enumerate(motif_segments):
        chain = motif_chain_id_order[i]
        if i == 0:
            contig_string += f"{segment['start'] - first_residue};{chain};"
        else:
            contig_string += f"{segment['start'] - motif_segments[i - 1]['end'] - 1};{chain};"
    last_residue = max(res.id[1] for res in structure[0][segment["chain"]] if res.id[0] == " ")
    contig_string += f"{last_residue - segment['end']}"
    return contig_string

def save_motif_pdb(motif_string, motif_pdb_dir="./motif_pdbs/", reference_pdb_dir="./reference_pdbs/", idx=None):
    pdb_id, motif_residues, redesign_residues, total_length, _ = motif_string.split(",")
    structure = load_pdb(pdb_id, reference_pdb_dir)
    structure = remove_alt_conformations(structure)
    motif_segments = parse_contig_string(motif_residues)
    redesign_segments = parse_contig_string(redesign_residues) if redesign_residues else []
    motif_structure = parse_motif_into_new_structure(structure, motif_segments, redesign_segments)
    contig_string = build_contig_string(structure, motif_segments)
    header = f"REMARK 1 Reference PDB ID: {pdb_id}\nREMARK 2 Motif Segment Placement in Reference PDB: {contig_string}\nREMARK 3 Length for Designed Scaffolds: {total_length}\n"
    motif_fn = os.path.join(motif_pdb_dir, f"{idx:02d}_{pdb_id}.pdb" if idx else f"{pdb_id}.pdb")
    io = PDBIO()
    io.set_structure(motif_structure)
    io.save(motif_fn, AltLocSelect(), write_end=True)
    center_pdb(motif_fn)
    with open(motif_fn, "r+") as f:
        content = f.read()
        f.seek(0, 0)
        f.write(header + content)

motif_specs_path = "../motif_specs.csv"
motif_pdb_dir = "../motif_pdbs/"
reference_pdb_dir = "../reference_pdbs/"
os.makedirs(motif_pdb_dir, exist_ok=True)
os.makedirs(reference_pdb_dir, exist_ok=True)

with open(motif_specs_path, "r") as f:
    f.readline()
    for idx, line in enumerate(f):
        save_motif_pdb(line.strip(), motif_pdb_dir, reference_pdb_dir, idx + 1)

def clean_pdb(filepath):
    if os.path.isfile(filepath):
        with open(filepath, "r") as f:
            lines = f.readlines()
        with open(filepath, "w") as f:
            for line in lines:
                f.write("TER\n" if line.startswith("TER") else line)

def set_bfactor_to_zero(filepath):
    tmp_fn = filepath + ".tmp"
    with open(filepath, "r") as infile, open(tmp_fn, "w") as outfile:
        for line in infile:
            if line.startswith(("ATOM", "HETATM")):
                outfile.write(line[:60] + f"{0.00:6.2f}" + line[66:])
            else:
                outfile.write(line)
    shutil.move(tmp_fn, filepath)

for filename in os.listdir(motif_pdb_dir):
    filepath = os.path.join(motif_pdb_dir, filename)
    clean_pdb(filepath)
    set_bfactor_to_zero(filepath)
