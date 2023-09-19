
import abc
import os
import requests
from typing import List
import urllib.request

from Bio.PDB import PDBParser, Structure

from .constants import UNIPROT_URL, PDB_URL, PDB_EXT, RCSB_URL
from .structure import ProtStructure


class ProtRecord(abc.ABC):

    def __init__(self, rec_id: str, loc: str):

        self.rec_id = rec_id
        self.loc = loc

        return
    
    @abc.abstractmethod
    def _query(self):

        raise NotImplementedError

    @property
    def id(self) -> str:

        return self.rec_id
    

class UniProtRecord(ProtRecord):

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.base_url = UNIPROT_URL

        self._query()

        return

    def _query(self):

        result = requests.get(self.base_url + self.rec_id)

        if result.status_code != 200:
            raise Exception

        self.json = result.json()

        return
    
    def get_pdb_entry_ids(self) -> List[str]:

        pdb_ids = [
            evidence["source"]["id"] for ft in self.json["features"]
            for evidence in ft.get("evidences", [])
            if evidence["source"]["name"] == "PDB"
        ]

        return set(pdb_ids)


class PDBRecord(ProtRecord, ProtStructure):

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.pdb_fn = self.rec_id + PDB_EXT
        self.pdb_fp = os.path.join(self.loc, self.pdb_fn)
        self.pdb_parser = PDBParser(QUIET=True)

        self.base_url = PDB_URL

        self._query()

        return

    def _query(self):

        pdb_url = os.path.join(self.base_url, self.pdb_fn)

        if not os.path.exists(self.pdb_fp):
            urllib.request.urlretrieve(pdb_url, self.pdb_fp)

        return

    def load_structure(self) -> Structure.Structure:

        return self.pdb_parser.get_structure(self.rec_id, self.pdb_fp)
    
    def get_entity_uniprot_ids(self) -> List[str]:

        graphql_query = """
            query {
                entries(entry_ids:[\"""" + self.rec_id + """\"]){
                    polymer_entities {
                        rcsb_id
                            rcsb_polymer_entity_container_identifiers {
                                reference_sequence_identifiers {
                                    database_accession
                                    database_name
                            }
                        }
                    }
                }
            }
        """

        result = requests.post(RCSB_URL, json={"query": graphql_query})

        if result.status_code != 200:
            raise Exception
        
        result_json = result.json()
        uniprot_ids = {}
        for polymer_entity in result_json["data"]["entries"][0]["polymer_entities"]:
            uniprot_ids[polymer_entity["rcsb_id"]] = [ref_seq_id["database_accession"] for ref_seq_id in polymer_entity["rcsb_polymer_entity_container_identifiers"]["reference_sequence_identifiers"] if ref_seq_id["database_name"] == "UniProt"]

        return uniprot_ids
