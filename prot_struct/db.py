
import abc

from .record import ProtRecord, UniProtRecord, PDBRecord


class ProtDatabase(abc.ABC):

    def __init__(self, download_loc: str = None):

        self.download_loc = "" if download_loc is None else download_loc
        self.records = {}
        self.record_obj = None

        return
    
    def pull_record(self, prot_id: str):

        if prot_id in self.records.keys():
            return

        self.records[prot_id] = self.record_obj(prot_id, self.download_loc)

        return
    
    def get_record(self, prot_id: str, pull: bool = False) -> ProtRecord:

        if prot_id not in self.records.keys():
            if not pull:
                raise KeyError(prot_id)
            else:
                self.pull_record(prot_id)

        return self.records[prot_id]
    

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
