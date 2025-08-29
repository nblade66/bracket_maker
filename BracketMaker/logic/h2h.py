from BracketMaker.bracket.bracket import Bracket
from BracketMaker.bracket.bracket import Matchup
from BracketMaker.participant.participant import Participant

class H2H:
    """ Class to manage head-to-head bracket logic.
        What this means is that it will present each matchup one at a time,
        and allow selection of the winner, then move on to the next matchup.
    """
    def __init__(self, bracket):
        self.bracket = bracket
        self.round_index = 0
        self.match_index = 0

        self.current_matchup: tuple[int,Matchup] | None = None

    def get_current_matchup(self) -> tuple[int,Matchup] | None:
        """ Advances self.current_matchup to the next undecided matchup, or None if all are decided.
            Note that this will not advance as long as the current matchup remains undecided.
        """
        while self.round_index < len(self.bracket.rounds):
            rnd = self.bracket.rounds[self.round_index]
            while self.match_index < len(rnd):
                matchup = rnd[self.match_index]
                if not matchup.is_decided():
                    return (self.round_index + 1, matchup)
                self.match_index += 1
            # Move to next round
            self.round_index += 1
            self.match_index = 0
        return None

    def set_winner(self, winner: Participant):
        """Set the winner for the current matchup."""
        self.get_current_matchup()[1].set_winner(winner)
    
    def suggest_random_winner(self, matchup: Matchup) -> Participant:
        """ Suggest a random winner for the given matchup. """
        import random
        return random.choice([p for p in (matchup.participant1, matchup.participant2) if p is not None])
    
    def auto_resolve(self, winner_selector):
        """
        Resolve all undecided matchups using a provided winner_selector function.
        winner_selector(matchup) should return the participant to set as winner.
        """
        for round_num, rnd in enumerate(self.bracket.rounds, start=1):
            for matchup in rnd:
                if not matchup.is_decided():
                    winner = winner_selector(matchup)
                    if winner not in (matchup.participant1, matchup.participant2):
                        raise ValueError("winner_selector must return one of the matchup participants")
                    matchup.set_winner(winner)
        