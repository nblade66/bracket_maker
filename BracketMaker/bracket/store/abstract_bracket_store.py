from abc import ABC, abstractmethod
from BracketMaker.bracket.bracket import Bracket

class BracketStore(ABC):
    """
    Abstract base class for Bracket storage.
    All methods require a user_id to ensure brackets are associated with a specific user.
    Bracket IDs must be globally unique across all users.
    """

    @abstractmethod
    def create(self, bracket_id: str, bracket: Bracket, user_id: str):
        """
        Create a new bracket for the given user.
        Raises ValueError if the bracket_id already exists (for any user).
        """
        pass

    @abstractmethod
    def read(self, bracket_id: str, user_id: str) -> Bracket | None:
        """
        Retrieve a bracket by its ID and user_id.
        Returns the Bracket if found, else None.
        """
        pass

    @abstractmethod
    def update(self, bracket_id: str, bracket: Bracket, user_id: str):
        """
        Update an existing bracket for the given user.
        Raises KeyError if the bracket does not exist for the user.
        """
        pass

    @abstractmethod
    def delete(self, bracket_id: str, user_id: str):
        """
        Delete a bracket by its ID and user_id.
        Does nothing if the bracket does not exist.
        """
        pass

    @abstractmethod
    def list_all(self, user_id: str) -> list[Bracket]:
        """
        List all brackets belonging to the given user.
        Returns a list of Bracket objects.
        """
        pass

    @abstractmethod
    def list_all_with_ids(self, user_id: str) -> list[tuple[str, Bracket]]:
        """
        List all brackets belonging to the given user, returning (bracket_id, Bracket) tuples.
        Returns a list of (bracket_id, Bracket) tuples.
        """
        pass

    @abstractmethod
    def bracket_id_exists(self, bracket_id: str) -> bool:
        """
        Check if a bracket_id exists for any user (global uniqueness).
        Returns True if the bracket_id exists, False otherwise.
        """
        pass
