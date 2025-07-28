# participant.py

from dataclasses import dataclass, field
import os
import itertools

@dataclass
class Participant:
    """
    Represents a participant in a bracket competition.
    For development purposes, the code related to image file is commented out.

    Each participant has a unique ID, a name, and a path to an associated image file.
    IDs are assigned by the ParticipantStore.
    Participants will not be shared between ParticipantStores.
    The class validates that the name is not empty.

    Attributes:
        id (int): Participant ID, assigned by the ParticipantStore
        name (str): Name of the participant.
        image_path (str): Path to an image file representing the participant.

    Raises:
        ValueError: If the name is empty or consists only of whitespace.
        FileNotFoundError: If the specified image file does not exist.
    """
    name: str
    # image_path: str
    id: int | None = field(init=False)
    is_bye: bool = field(default=False, init=True)

    def __post_init__(self):
        self.id = None
        self.name = self.name.strip()
        #self.image_path = self.image_path.strip()

        if not self.name:
            raise ValueError("Participant name cannot be empty.")

        #if not os.path.isfile(self.image_path):
        #    raise FileNotFoundError(f"Image file not found: {self.image_path}")

    def __repr__(self):
        return f"Participant(id={self.id}, name='{self.name}', image_path='{"self.image_path"}')"
