from BracketMaker.store.in_memory_participant_store import InMemoryParticipantStore
from BracketMaker.participant import Participant

import csv

def load_from_txt(file_path: str) -> InMemoryParticipantStore:
    """ Load participants from a new-line delineated file """
    store: InMemoryParticipantStore = InMemoryParticipantStore()
    with open(file_path, 'r') as f:
        for line in f.readlines():
            line = line.strip()
            store.add_participant(Participant(line))
    
    return store

def load_from_csv(file_path: str) -> InMemoryParticipantStore:
    """
    Load participants from a CSV file with a specific header format.
    Uses 'Track Name' as the participant name and 'Album Name' as image path placeholder.
    """
    store: InMemoryParticipantStore = InMemoryParticipantStore()

    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            name = row.get("Track Name", "").strip()
            album = row.get("Album Name", "").strip()

            if name:
                store.add_participant(Participant(name))

    return store
