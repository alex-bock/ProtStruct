
import abc

from .record import ProtRecord, PDBRecord


class ProtDatabase(abc.ABC):

    def __init__(self, download_loc: str = None):

        self.download_loc = "" if download_loc is None else download_loc

        return

    @abc.abstractmethod
    def pull_record(self, prot_id: str) -> ProtRecord:

        raise NotImplementedError


class PDB(ProtDatabase):

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.records = {}

        return

    def pull_record(self, prot_id: str):

        if prot_id in self.records.keys():
            return

        self.records[prot_id] = PDBRecord(prot_id, self.download_loc)

        return

    def get_record(self, prot_id: str, pull: bool = False) -> PDBRecord:

        if prot_id not in self.records.keys():
            if not pull:
                raise KeyError(prot_id)
            else:
                self.pull_record(prot_id)

        return self.records[prot_id]
