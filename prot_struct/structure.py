
import abc

from Bio.PDB import Structure


PDB_EXT = ".pdb"
PDB_BASE_URL = "http://files.rcsb.org/download/"


class ProtStructure(abc.ABC):

    def __init__(self):

        return

    @abc.abstractmethod
    def load_structure(self) -> Structure.Structure:

        raise NotImplementedError

    @property
    def structure(self):

        raise NotImplementedError
