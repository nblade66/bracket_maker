from BracketMaker.logic.h2h import H2H
from BracketMaker.bracket.bracket import Bracket
from BracketMaker.participant.store.in_memory_participant_store import InMemoryParticipantStore
from BracketMaker.participant.participant import Participant

import pytest

def make_bracket(names, rand_seed=1):
    store = InMemoryParticipantStore()
    for n in names:
        store.add_participant(Participant(name=n))
    return Bracket("test", store, rand_seed=rand_seed)

def test_get_current_matchup_and_set_winner():
    bracket = make_bracket(["A", "B", "C", "D"])
    h2h = H2H(bracket)
    # Should return first undecided matchup
    round_num, matchup = h2h.get_current_matchup()
    assert round_num == 1
    assert not matchup.is_decided()
    # Set winner for first matchup
    h2h.set_winner(matchup.participant1)
    # Next call should return next undecided matchup, still round 1
    round_num2, matchup2 = h2h.get_current_matchup()
    assert (round_num2, matchup2) != (round_num, matchup)
    assert round_num2 == 1
    h2h.set_winner(matchup2.participant1)
    # Now should advance to round 2
    round_num3, matchup3 = h2h.get_current_matchup()
    assert round_num3 == 2
    # Set all winners and check round numbers
    prev_round = round_num3
    while True:
        cur = h2h.get_current_matchup()
        if not cur:
            break
        r, m = cur
        # Round number should be >= previous
        assert r >= prev_round
        prev_round = r
        h2h.set_winner(m.participant1 or m.participant2)
    # Now all matchups are decided
    assert h2h.get_current_matchup() is None

def test_auto_resolve():
    bracket = make_bracket(["A", "B", "C", "D"])
    h2h = H2H(bracket)
    def always_p1(matchup):
        return matchup.participant1
    h2h.auto_resolve(always_p1)
    # All matchups should be decided
    for rnd in bracket.rounds:
        for m in rnd:
            assert m.is_decided()
    # Should raise if selector returns invalid winner
    bracket2 = make_bracket(["A", "B", "C", "D"])
    h2h2 = H2H(bracket2)
    with pytest.raises(ValueError):
        h2h2.auto_resolve(lambda m: Participant(name="Z"))
