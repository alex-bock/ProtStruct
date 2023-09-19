
import abc

from .record import ProtRecord, UniProtRecord, PDBRecord


class ProtDatabase(abc.ABC):

    def __init__(self, download_loc: str = None):

        self.download_loc = "./data/structures/pdb/" if download_loc is None else download_loc
        self.records = {}
        self.record_obj = None

        return
    
    def pull_record(self, rec_id: str):

        if rec_id in self.records.keys():
            return

        self.records[rec_id] = self.record_obj(rec_id, self.download_loc)

        return
    
    def get_record(self, rec_id: str, pull: bool = False) -> ProtRecord:

        if rec_id not in self.records.keys():
            if not pull:
                raise KeyError(rec_id)
            else:
                self.pull_record(rec_id)

        return self.records[rec_id]
    

class UniProt(ProtDatabase):

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        self.record_obj = UniProtRecord

        return


class PDB(ProtDatabase):

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        self.record_obj = PDBRecord

        return
