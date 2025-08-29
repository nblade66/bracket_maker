from BracketMaker.bracket.bracket import Bracket
from BracketMaker.participant.store.abstract_participant_store import ParticipantStore
from BracketMaker.participant.store.in_memory_participant_store import InMemoryParticipantStore
from BracketMaker.participant.participant import Participant

def test_bracket_initialization():
    store: ParticipantStore = InMemoryParticipantStore()
    store.add_participant(Participant(name="P1"))
    store.add_participant(Participant(name="P2"))
    store.add_participant(Participant(name="P3"))
    store.add_participant(Participant(name="P4"))
    store.add_participant(Participant(name="P5"))

    bracket = Bracket("test_bracket", store, rand_seed=111)

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

def test_get_undecided_matchups():
    store: ParticipantStore = InMemoryParticipantStore()
    store.add_participant(Participant(name="A"))
    store.add_participant(Participant(name="B"))
    store.add_participant(Participant(name="C"))
    store.add_participant(Participant(name="D"))
    bracket = Bracket("undecided_test", store, rand_seed=42)

    # All matchups should be undecided at start
    undecided = bracket.get_undecided_matchups()
    total_matchups = sum(len(rnd) for rnd in bracket.rounds)
    assert len(undecided) == total_matchups

    # Decide the first matchup in round 1
    first_round_first = bracket.rounds[0][0]
    first_round_first.set_winner(first_round_first.participant1)
    undecided_after = bracket.get_undecided_matchups()
    assert len(undecided_after) == total_matchups - 1

    # Decide all matchups
    for rnd in bracket.rounds:
        for matchup in rnd:
            if not matchup.is_decided():
                matchup.set_winner(matchup.participant1 or matchup.participant2)
    assert bracket.is_complete()
    assert bracket.get_undecided_matchups() == []