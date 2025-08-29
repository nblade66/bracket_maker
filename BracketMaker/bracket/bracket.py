# bracket.py

import random
from BracketMaker.participant.store.abstract_participant_store import ParticipantStore
from BracketMaker.participant.participant import Participant
from BracketMaker.utils import interleave
from typing import Self

class Matchup:
    """
    Represents a single matchup between two participants.
    Stores the two participants and the winner once decided.
    """
    def __init__(self, participant1: Participant | None, participant2: Participant | None,
                prev_matchup_1: Self | None, prev_matchup_2: Self | None):
        self.participant1 = participant1
        self.participant2 = participant2
        self.winner: Participant | None = None
        
        self.next_matchup = None
        self.prev_matchup_1 = prev_matchup_1
        self.prev_matchup_2 = prev_matchup_2

    def set_winner(self, winner: Participant | None):
        """ Sets the winner and updates any future matchups, as well.
            if the future matchups had a different participant, then
            set those participants to None, since now the winner is
            undecided.
        """
        if winner and winner not in [self.participant1, self.participant2]:
            raise ValueError("Winner must be one of the participants in the matchup.")
        
        # if the winner has not changed, do nothing
        if self.winner is winner:
            return
        
        # if the winner has changed, set the winner and set the next Matchup's corresponding
        # participant to the new winner.
        # Note that changing the next matchup's participant will also set all future round's
        # Matchups to None, since now the winner of the next Matchup is TBD.
        self.winner = winner

        if self.next_matchup:
            if self.next_matchup.prev_matchup_1 is self:
                self.next_matchup.set_participant1(winner)
            if self.next_matchup.prev_matchup_2 is self:
                self.next_matchup.set_participant2(winner)
    
    def set_participant1(self, participant: Participant | None):
        """ Set partipant1.
        
            If participant has changed, check that the participant is one of the
            participants in the previous matchup.
            Then set the participant and also set the winner to None because now the
            winner is TBD. This will cause the "None"'s to propogate down the bracket.
        """
        if self.participant1 is participant:
            return

        if participant not in [None, self.prev_matchup_1.participant1, self.prev_matchup_1.participant2]:
            raise ValueError("Participant is not a participant in the previous Matchup")
        self.participant1 = participant
        self.set_winner(None)

    def set_participant2(self, participant: Participant | None):
        """ Set partipant2.
        
            If participant has changed, check that the participant is one of the
            participants in the previous matchup.
            Then set the participant and also set the winner to None because now the
            winner is TBD. This will cause the "None"'s to propogate down the bracket.
        """
        if self.participant2 is participant:
            return

        if participant not in [None, self.prev_matchup_2.participant1, self.prev_matchup_2.participant2]:
            raise ValueError("Participant is not a participant in the previous Matchup")
        self.participant2 = participant
        self.set_winner(None)
    
    def is_decided(self) -> bool:
        return self.winner is not None

    def __repr__(self):
        p1 = self.participant1.name if self.participant1 else "TBD"
        p2 = self.participant2.name if self.participant2 else "TBD"
        winner = self.winner.name if self.winner else "TBD"
        return f"Matchup({p1} vs {p2} | Winner: {winner})"


class Bracket:
    """
    Represents the entire tournament bracket.
    Organizes participants into matchups per round.
    Uses a static pre-constructed bracket and updates each Matchup's participants.

    Note that "BYE" paticipants are participants, but they should not be added to the
    participant list. "BYE" participants should only exist in the first round (for a standard
    tournament bracket structure).

    Meanwhile, "None" participants are participant slots that are not filled yet because the
    previous round has not completed yet.

    The structure of the bracket is a list[list[Matchup]] where each next round is the
    next item in the list. Each Matchup has a reference to the next Matchup that is in
    the next round, so this is kind of like an array list/linked list hybrid.

    participants: none of the participants in this list should be a "BYE" participant (is_bye set to True)
    """
    def __init__(self, name: str, participant_store: ParticipantStore, rand_seed: int | None = None):
        if not participant_store:
            raise ValueError("A Participant Store is required.")

        if len(participant_store.list_participants()) < 2:
            raise ValueError("At least two participants are required for a tournament.")

        if any(participant.is_bye for participant in participant_store.list_participants()):
            raise ValueError("No participants should be a BYE. Those are added automatically")

        self.name = name
        self.participant_store = participant_store
        self.rounds: list[list[Matchup]] = []
        self.rand_seed = rand_seed
        self._setup_bracket(self.participant_store.list_participants())

    def _setup_bracket(self, participants: list[Participant]):
        """ Creates a shuffled bracket of Matchup objects from a list of participants """
        # Create matchups from adjacent participants
        first_round: list[Matchup] = self._create_first_round(participants)
        self.rounds.append(first_round)

        # Keep creating rounds until the last round only has 1 Matchup left
        # This also sets up the linked list
        while len(self.rounds[-1]) > 1:
            self.rounds.append(self._create_next_round(self.rounds[-1]))
        
        # Set winners for all matchups that have byes in the first round (only first round
        # should have byes)
        # TODO I think this should be handled automatically by the Matchup Class
        for matchup in self.rounds[0]:
            if matchup.participant1.is_bye:
                matchup.set_winner(matchup.participant2)
            if matchup.participant2.is_bye:
                matchup.set_winner(matchup.participant1)

    def _create_first_round(self, participants: list[Participant]) -> list[Matchup]:
        """ Creates the first round of matchups.
        
            Completes the list of participants, so that the number of participants
            is a power of two. Any empty slots are filled with "BYE" participants.
            
            Also ensures that the two halves of the bracket are balanced and have the same
            (or different of one) number of "BYE" participants.
            
            Also ensures that no two "BYE" participants are matched up."""
        # Shuffle participants
        shuffled = participants[:]

        # set the seed for random; this is mostly for testing purposes
        if self.rand_seed:
            random.seed(self.rand_seed)
        random.shuffle(shuffled)

        # Ensure number of participants is a power of 2 by adding BYEs (None)
        num_participants = len(shuffled)
        next_power_of_two = 1
        while next_power_of_two < num_participants:
            next_power_of_two <<= 1

        # Split the participant list in half and assign byes to each side to ensure both sides
        # have the same number of byes; if number of participants is odd, the left side will have
        # an extra bye always.
        half_participants = num_participants // 2
        left_participants = shuffled[:half_participants]
        right_participants = shuffled[half_participants:]

        left_byes = (next_power_of_two // 2) - len(left_participants)
        right_byes = (next_power_of_two // 2) - len(right_participants)

        left_bye_participants = [Participant(name="BYE", is_bye=True)] * left_byes
        right_bye_participants = [Participant(name="BYE", is_bye=True)] * right_byes

        left_half = interleave(left_participants, left_bye_participants)
        right_half = interleave(right_participants, right_bye_participants)

        shuffled = left_half + right_half
        
        first_round = []
        for i in range(0, len(shuffled), 2):
            first_round.append(Matchup(shuffled[i], shuffled[i+1], None, None))
        
        return first_round
    
    def _create_next_round(self, current_round: list[Matchup]) -> list[Matchup]:
        """ Create the next round of Matchups based on the current round.
            Set the current round's Matchups to reference the next round's appropriate
            Matchup.
        """
        next_round: list[Matchup] = []
        for i in range(0, len(current_round), 2):
            matchup_1 = current_round[i]
            matchup_2 = current_round[i+1]
            new_matchup = Matchup(matchup_1.winner, matchup_2.winner, matchup_1, matchup_2)
            matchup_1.next_matchup = new_matchup
            matchup_2.next_matchup = new_matchup

            next_round.append(new_matchup)
        
        return next_round

    def is_complete(self) -> bool:
        """
        Returns True if the tournament has been completed (only one winner remains).
        """
        return len(self.rounds) > 0 and len(self.rounds[-1]) == 1 and self.rounds[-1][0].is_decided()
    
    def get_winner(self) -> Participant | None:
        if self.is_complete():
            return self.rounds[-1][0].winner
        return None
    
    def get_matchup(self, round: int, index: int) -> Matchup | None:
        if round < len(self.rounds) and index < len(self.rounds[round]):
            return self.rounds[round][index]
        return None
    
    def add_participant(self, participant: Participant, matchup_index: int):
        """ Adds participant to self.participant_store and the designated matchup. Participants
            can only be added to the first round if there is a bye in that spot. Otherwise,
            remove a participant from a Matchup before adding a new participant.
            
            Raises a ValueError if the participant already exists or the matchup
            already has two participants.
        """
        if any(p.id == participant.id for p in self.participant_store.list_participants()):
            raise ValueError(f"Participant with ID {participant.id} already exists.")
        if matchup_index >= len(self.rounds[0]):
            raise IndexError("Invalid matchup index.")
        
        matchup = self.rounds[0][matchup_index]
        if matchup.participant1 and not matchup.participant1.is_bye and matchup.participant2 and not matchup.participant2.is_bye:
            raise ValueError("Matchup already has two participants.")
        
        # Don't add the participant to the participant list if it is a "BYE" participant
        if not participant.is_bye:
            self.participant_store.add_participant(participant)

        if not matchup.participant1 or matchup.participant1.is_bye:
            matchup.participant1 = participant
        else:
            matchup.participant2 = participant

        matchup.set_winner(None)
    
    def get_participant_by_id(self, participant_id: int) -> Participant | None:
        for p in self.participant_store.list_participants():
            if p.id == participant_id:
                return p
        
        return None
    
    def get_participant_by_name(self, name: str) -> list[Participant]:
        """ Finds all participants with a certain name """
        return [p for p in self.participant_store.list_participants() if p.name == name]
    
    def remove_participant(self, participant_id: int) -> Participant | None:
        """ Removes the participant with participant_id from self.participant_store and
            the corresponding matchup where the participant is. Any matchups in later
            rounds that the participant was part of are set to TBD.

            Note that if you wish for a participant to be a "BYE", then you would
            need to add a "BYE" participant to the matchup. This function will leave
            the matchup with a "None" participant.

            Returns the removed Participant or None if the Participant was not found.
        """
        participant = self.get_participant_by_id(participant_id=participant_id)
        if not participant:
            return None
        self.participant_store.remove_participant(participant_id=participant_id)
        for rnd in self.rounds:
            for matchup in rnd:
                if matchup.participant1 is participant:
                    # this also sets any subsequent round participants to None
                    matchup.set_participant1(None)  
                    return participant 
                if matchup.participant2 is participant:
                    # this also sets any subsequent round participants to None
                    matchup.set_participant2(None)
                    return participant
                        
        return None
    
    def list_participants(self) -> list[Participant]:
        return self.participant_store.list_participants()[:]
    
    def get_matchup_by_participant_id(self, participant_id: int) -> list[tuple[Matchup, int, int]] | None:
        """ Gets a matchup by the participant id.
            
            Returns a list of tuples of (Matchup, Round Number, Matchup Index)
            Returns None if the participant was not found.
        """
        results = []
        for r_index, rnd in enumerate(self.rounds):
            for m_index, matchup in enumerate(rnd):
                if (matchup.participant1 and matchup.participant1.id == participant_id) or \
                   (matchup.participant2 and matchup.participant2.id == participant_id):
                    results.append((matchup, r_index, m_index))
        return results if results else None

    def get_matchup_by_participant_ids(self, participant1_id: int, participant2_id: int) -> tuple[Matchup, int, int] | None:
        """ Gets a matchup by the ids of the two participants in the matchup.
            
            Participants should only matchup once in the bracket, so this returns
            a single tuple of (Matchup, Round Number, Matchup Index).
        """
        for r_index, rnd in enumerate(self.rounds):
            for m_index, matchup in enumerate(rnd):
                ids = [
                    matchup.participant1.id if matchup.participant1 else None,
                    matchup.participant2.id if matchup.participant2 else None
                ]
                if participant1_id in ids and participant2_id in ids:
                    return (matchup, r_index, m_index)
        return None

    def get_undecided_matchups(self) -> list[tuple[int, Matchup]]:
        """Return a list of (round_num, matchup) for all undecided matchups in order."""
        undecided = []
        for round_num, rnd in enumerate(self.rounds, start=1):
            for matchup in rnd:
                if not matchup.is_decided():
                    undecided.append((round_num, matchup))
        return undecided

    def __repr__(self):
        repr_str = self.name + "\n"
        for i, rnd in enumerate(self.rounds, 1):
            repr_str += f"Round {i}:\n"
            for m in rnd:
                repr_str += f"  {m}\n"
        return repr_str
