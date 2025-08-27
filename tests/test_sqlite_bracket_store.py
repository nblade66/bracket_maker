""" Test for SQLiteBracketStore """
import pytest
import tempfile
import os
import gc
from BracketMaker.bracket.bracket import Bracket
from BracketMaker.bracket.store.sqlite_bracket_store import SQLiteBracketStore
from BracketMaker.participant.store.in_memory_participant_store import InMemoryParticipantStore
from BracketMaker.participant.participant import Participant

@pytest.fixture
def store():
    with tempfile.TemporaryDirectory() as tmpdir:
        path = os.path.join(tmpdir, "test_brackets.db")
        store = SQLiteBracketStore(db_path=path)
        yield store
        
        # Added because Windows gives PermissionErrors if garbage collector doesn't run first
        gc.collect()

def create_sample_bracket():
    participant_store = InMemoryParticipantStore()
    participant_store.add_participant(Participant(name="P1"))
    participant_store.add_participant(Participant(name="P2"))
    participant_store.add_participant(Participant(name="P3"))
    participant_store.add_participant(Participant(name="P4"))
    participant_store.add_participant(Participant(name="P5"))
    return Bracket("test_bracket", participant_store, rand_seed=111)

def test_create_and_read_bracket(store):
    bracket = create_sample_bracket()
    user_id = "user123"
    store.create("bracket1", bracket, user_id)

    fetched = store.read("bracket1", user_id)
    assert fetched is not None
    assert isinstance(fetched, Bracket)
    assert len(fetched.rounds) == len(bracket.rounds)

def test_create_duplicate_bracket_id_fails(store):
    bracket = create_sample_bracket()
    user_id1 = "user1"
    user_id2 = "user2"
    bracket_id = "duplicate_id"

    # First creation should succeed
    store.create(bracket_id, bracket, user_id1)

    # Second creation with same bracket_id (even for a different user) should fail
    with pytest.raises(ValueError):
        store.create(bracket_id, bracket, user_id2)
