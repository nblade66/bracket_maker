from BracketMaker.core.bracket import Bracket
from BracketMaker.store.abstract_participant_store import ParticipantStore
from BracketMaker.store.in_memory_participant_store import InMemoryParticipantStore
from BracketMaker.participant import Participant

def test_bracket_initialization():
    store: ParticipantStore = InMemoryParticipantStore()
    store.add_participant(Participant(name="P1"))
    store.add_participant(Participant(name="P2"))
    store.add_participant(Participant(name="P3"))
    store.add_participant(Participant(name="P4"))
    store.add_participant(Participant(name="P5"))

    bracket = Bracket(store.list_participants(), rand_seed=111)

    print(bracket)
    
    # Round 1
    assert(bracket.rounds[0][0].participant1.name == "P4")
    assert(bracket.rounds[0][0].participant2.name == "BYE")
    assert(bracket.rounds[0][1].participant1.name == "P1")
    assert(bracket.rounds[0][1].participant2.name == "BYE")
    assert(bracket.rounds[0][2].participant1.name == "P5")
    assert(bracket.rounds[0][2].participant2.name == "BYE")
    assert(bracket.rounds[0][3].participant1.name == "P3")
    assert(bracket.rounds[0][3].participant2.name == "P2")

    # Round 2
    assert(bracket.rounds[1][0].participant1.name == "P4")
    assert(bracket.rounds[1][0].participant2.name == "P1")
    assert(bracket.rounds[1][1].participant1.name == "P5")
    assert(bracket.rounds[1][1].participant2 is None)