import pytest
import tempfile
import os
import gc
from BracketMaker.participant.store.sqlite_participant_store import SQLiteParticipantStore
from BracketMaker.participant.participant import Participant

@pytest.fixture
def store():
    with tempfile.TemporaryDirectory() as tmpdir:
        path = os.path.join(tmpdir, "test.db")
        store = SQLiteParticipantStore(db_path=path)
        yield store
        
        # Added because Windows gives PermissionErrors if garbage collector doesn't run first
        gc.collect()    

def test_add_and_get_participant(store):
    participant = store.add_participant(Participant(name="Alice"))

    fetched = store.get_participant(participant.id)
    assert fetched is not None
    assert fetched.id == participant.id
    assert fetched.name == "Alice"


def test_list_participants(store):
    p1 = store.add_participant(Participant(name="Alice"))
    p2 = store.add_participant(Participant(name="Bob"))

    participants = store.list_participants()
    assert len(participants) == 2
    ids = {p.id for p in participants}
    assert ids == {p1.id, p2.id}


def test_remove_participant(store):
    participant = Participant(name="Charlie")
    participant = store.add_participant(participant)

    removed = store.remove_participant(participant.id)
    assert removed is True
    assert store.get_participant(participant.id) is None

    # Try removing again
    removed_again = store.remove_participant(participant.id)
    assert removed_again is False


def test_clear_participants(store):
    store.add_participant(Participant(name="Dave"))
    store.add_participant(Participant(name="Eve"))
    store.clear()

    assert store.list_participants() == []
