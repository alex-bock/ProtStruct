
import abc
import os
import requests
import urllib.request

from Bio.PDB import PDBParser, Structure

from .constants import UNIPROT_URL, PDB_URL, PDB_EXT
from .structure import ProtStructure


class ProtRecord(abc.ABC):

    def __init__(self, prot_id: str, loc: str):

        self.prot_id = prot_id
        self.loc = loc

        return

    @property
    def id(self) -> str:

        return self.prot_id
    

class UniProtRecord(ProtRecord):

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.base_url = UNIPROT_URL
        self.json = self._query_accession()

        return

    def _query_accession(self):

        result = requests.get(self.base_url + self.prot_id)

        if result.status_code == 200:
            result_json = result.json()
        else:
            raise Exception

        return result_json
    
    def find_pdb_ids(self):

        pdb_ids = set()

        for ft in self.json["features"]:
            for evidence in ft.get("evidences", []):
                if evidence["source"]["name"] == "PDB":
                    pdb_ids.add(evidence["source"]["id"])

        return pdb_ids


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

        return

    def load_structure(self) -> Structure.Structure:

        return self.parser.get_structure(self.prot_id, self.pdb_fp)
