from BracketMaker.participant_store import InMemoryParticipantStore
from BracketMaker.participant import Participant

def load_from_txt(file_path: str) -> InMemoryParticipantStore:
    """ Load participants from a new-line delineated file """
    store: InMemoryParticipantStore = InMemoryParticipantStore()
    with open(file_path, 'r') as f:
        for line in f.readlines():
            line = line.strip()
            store.add_participant(Participant(line))
    
    return store
