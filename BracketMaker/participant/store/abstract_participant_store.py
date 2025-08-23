# participant_store.py

from abc import ABC, abstractmethod
from BracketMaker.participant.participant import Participant


class ParticipantStore(ABC):
    """Abstract base class for participant storage."""

    @abstractmethod
    def add_participant(self, participant: Participant) -> Participant:
        """ Adds participant to participant store. Assigns the participant a unique ID.

            Should raise a ValueError if participant already exists.
            Perhaps there should be an update_participant() function?

            Returns the added Participant (with the newly assigned ID)
        """
        pass

    @abstractmethod
    def remove_participant(self, participant_id: int) -> bool:
        pass

    @abstractmethod
    def get_participant(self, participant_id: int) -> Participant | None:
        pass

    @abstractmethod
    def list_participants(self) -> list[Participant]:
        pass

    @abstractmethod
    def clear(self) -> None:
        """Remove all participants."""
        pass

