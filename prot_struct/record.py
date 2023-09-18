
import abc
import os
import urllib.request

from Bio.PDB import PDBParser, Structure

from .constants import PDB_URL, PDB_EXT
from .structure import ProtStructure


class ProtRecord(abc.ABC):

    def __init__(self, prot_id: str, loc: str):

        self.prot_id = prot_id
        self.loc = loc

        return

    @property
    def id(self) -> str:

        return self.prot_id


class PDBRecord(ProtRecord, ProtStructure):

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.pdb_fn = self.prot_id + PDB_EXT
        self.pdb_fp = os.path.join(self.loc, self.pdb_fn)
        self.parser = PDBParser(QUIET=True)

        self.base_url = PDB_URL

        self._download_pdb_file()

        return

    def _download_pdb_file(self):

        pdb_url = os.path.join(self.base_url, self.pdb_fn)

        if not os.path.exists(self.pdb_fp):
            urllib.request.urlretrieve(pdb_url, self.pdb_fp)

    def load_structure(self) -> Structure.Structure:

        return self.parser.get_structure(self.prot_id, self.pdb_fp)
