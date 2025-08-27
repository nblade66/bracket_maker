import uuid
from BracketMaker.bracket.bracket import Bracket
from BracketMaker.bracket.store.sqlite_bracket_store import SQLiteBracketStore

class BracketManager:
    """Manages Bracket objects for a specific user using a single BracketStore."""
    def __init__(self, user_id: str, store: SQLiteBracketStore = None):
        self.user_id = user_id
        self.store = store or SQLiteBracketStore()

    def add_bracket(self, bracket: Bracket, bracket_id: str = None) -> str:
        if bracket_id is None:
            # Ensure uniqueness by checking the store globally
            while True:
                candidate_id = str(uuid.uuid4())
                if not self.store.bracket_id_exists(candidate_id):
                    bracket_id = candidate_id
                    break
        else:
            if self.store.bracket_id_exists(bracket_id):
                raise ValueError(f"Bracket with id {bracket_id} already exists.")
        self.store.create(bracket_id, bracket, self.user_id)
        return bracket_id

    def get_bracket(self, bracket_id) -> Bracket | None:
        return self.store.read(bracket_id, self.user_id)

    def update_bracket(self, bracket_id, bracket: Bracket):
        self.store.update(bracket_id, bracket, self.user_id)

    def remove_bracket(self, bracket_id):
        self.store.delete(bracket_id, self.user_id)

    def list_brackets(self) -> list[Bracket]:
        return self.store.list_all(self.user_id)