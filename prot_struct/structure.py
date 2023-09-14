
import abc
import os
import urllib

from Bio.PDB import Structure, PDBParser


PDB_EXT = ".pdb"
PDB_BASE_URL = "http://files.rcsb.org/download/"


class Structure(abc.ABC):

    def __init__(self):

        return
    
    @abc.abstractmethod
    def download_file(self, prot_id: str) -> str:

        raise NotImplementedError
    
    def load_structure(self, path: str, structure_id: str) -> Structure.Structure:

        structure = self.parser.get_structure(structure_id, path)

        return structure
    

class PDBStructure(Structure):

    def __init__(self, struct_dir: str = "./data/structures/pdb/"):

        self.parser = PDBParser(QUIET=True)
        self.structure_dir = struct_dir

        return
    
    def download_file(self, prot_id: str) -> str:
        
        pdb_file = prot_id + PDB_EXT
        pdb_url = os.path.join(PDB_BASE_URL, pdb_file)
        pdb_path = os.path.join(self.structure_dir, pdb_file)

        if not os.path.exists(pdb_path):
            urllib.request.urlretrieve(pdb_url, pdb_path)

        return pdb_path
