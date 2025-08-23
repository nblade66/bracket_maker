from BracketMaker.participant.store.abstract_participant_store import ParticipantStore
from BracketMaker.participant.store.sqlite_participant_store import SQLiteParticipantStore
from BracketMaker.participant.participant import Participant

import csv

class FileLoader:
    """ Pass in a ParticipantStore that needs to have participants added.
        Will not check if the ParticipantStore is empty.
    """
    def __init__(self, store: ParticipantStore):
        self.store = store
    
    def load(self, file_path: str) -> ParticipantStore:
        if file_path.strip().endswith(".txt"):
            return self.load_from_txt(file_path)
        if file_path.strip().endswith(".csv"):
            return self.load_from_txt(file_path)
        
        raise ValueError("File type is incorrect. Accepted file types are .txt and .csv")


    def load_from_txt(self, file_path: str) -> ParticipantStore:
        """ Load participants from a new-line delineated file """
        with open(file_path, 'r') as f:
            for line in f.readlines():
                line = line.strip()
                self.store.add_participant(Participant(line))
        
        return self.store

    def load_from_csv(self, file_path: str) -> ParticipantStore:
        """
        Load participants from a CSV file with a specific header format.
        Uses 'Track Name' as the participant name and 'Album Name' as image path placeholder.
        """
        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                name = row.get("Track Name", "").strip()
                album = row.get("Album Name", "").strip()

                if name:
                    self.store.add_participant(Participant(name))

        return self.store
