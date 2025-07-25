from BracketMaker.participant import Participant
from BracketMaker.store.abstract_participant_store import ParticipantStore

class InMemoryParticipantStore(ParticipantStore):
    """Stores participants in memory using a dictionary."""

    def __init__(self):
        self._participants: dict[int, Participant] = {}

    def add_participant(self, participant: Participant) -> None:
        self._participants[participant.id] = participant

    def remove_participant(self, participant_id: int) -> bool:
        return self._participants.pop(participant_id, None) is not None

    def get_participant(self, participant_id: int) -> Participant | None:
        return self._participants.get(participant_id)

    def list_participants(self) -> list[Participant]:
        return list(self._participants.values())

    def clear(self) -> None:
        self._participants.clear()