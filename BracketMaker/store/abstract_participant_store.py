# participant_store.py

from abc import ABC, abstractmethod
from BracketMaker.participant import Participant


class ParticipantStore(ABC):
    """Abstract base class for participant storage."""

    @abstractmethod
    def add_participant(self, participant: Participant) -> None:
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

