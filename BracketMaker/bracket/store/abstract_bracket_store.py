from abc import ABC, abstractmethod
from BracketMaker.bracket.bracket import Bracket

class BracketStore(ABC):
    """Abstract base class for Bracket storage. Unique IDs are strings"""

    @abstractmethod
    def create(self, bracket_id, bracket: Bracket):
        pass

    @abstractmethod
    def read(self, bracket_id) -> Bracket | None:
        pass

    @abstractmethod
    def update(self, bracket_id, bracket: Bracket):
        pass

    @abstractmethod
    def delete(self, bracket_id):
        pass

    @abstractmethod
    def list_all(self) -> list[Bracket]:
        pass
