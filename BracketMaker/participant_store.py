# participant_store.py

from abc import ABC, abstractmethod
from typing import List, Optional
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
    def get_participant(self, participant_id: int) -> Optional[Participant]:
        pass

    @abstractmethod
    def list_participants(self) -> List[Participant]:
        pass

    @abstractmethod
    def clear(self) -> None:
        """Remove all participants."""
        pass


class InMemoryParticipantStore(ParticipantStore):
    """Stores participants in memory using a dictionary."""

    def __init__(self):
        self._participants: dict[int, Participant] = {}

    def add_participant(self, participant: Participant) -> None:
        self._participants[participant.id] = participant

    def remove_participant(self, participant_id: int) -> bool:
        return self._participants.pop(participant_id, None) is not None

    def get_participant(self, participant_id: int) -> Optional[Participant]:
        return self._participants.get(participant_id)

    def list_participants(self) -> List[Participant]:
        return list(self._participants.values())

    def clear(self) -> None:
        self._participants.clear()
