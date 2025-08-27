from BracketMaker.bracket.bracket import Bracket
from BracketMaker.bracket.store.abstract_bracket_store import BracketStore

class BracketManager:
    """ Manages Bracket objects using BracketStore.
    """
    def __init__(self, store: BracketStore):
        if not store:
            pass # TODO create the store
        self.store = store

    def add_bracket(self, bracket_id, bracket: Bracket):
        self.store.create(bracket_id, bracket)

    def get_bracket(self, bracket_id) -> Bracket | None:
        return self.store.read(bracket_id)

    def update_bracket(self, bracket_id, bracket: Bracket):
        self.store.update(bracket_id, bracket)

    def remove_bracket(self, bracket_id):
        return self.store.delete(bracket_id)

    def list_brackets(self) -> list[Bracket]:
        return self.store.list_all()