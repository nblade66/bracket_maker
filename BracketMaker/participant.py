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
    IDs are auto-generated to distinguish participants with the same name.
    The class validates that the name is not empty.

    Attributes:
        id (int): Auto-incremented unique identifier for the participant.
        name (str): Name of the participant.
        image_path (str): Path to an image file representing the participant.

    Raises:
        ValueError: If the name is empty or consists only of whitespace.
        FileNotFoundError: If the specified image file does not exist.
    """
    name: str
    # image_path: str
    id: int = field(init=False)
    is_bye: bool = field(default=False, init=True)

    # Class-level ID counter (auto-increments for each new participant)
    _id_counter = itertools.count(1)

    def __post_init__(self):
        self.id = next(self._id_counter)
        self.name = self.name.strip()
        #self.image_path = self.image_path.strip()

        if not self.name:
            raise ValueError("Participant name cannot be empty.")

        #if not os.path.isfile(self.image_path):
        #    raise FileNotFoundError(f"Image file not found: {self.image_path}")

    def __repr__(self):
        return f"Participant(id={self.id}, name='{self.name}', image_path='{"self.image_path"}')"
