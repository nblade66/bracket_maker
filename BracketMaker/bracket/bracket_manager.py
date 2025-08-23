from abc import ABC, abstractmethod
from .bracket import Bracket

class BracketStore(ABC):
    """Abstract base class for Bracket storage."""

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


class SQLiteBracketStore(BracketStore):
    """SQLite implementation of BracketStore."""
    def __init__(self, db_path=":memory:"):
        import sqlite3
        self.conn = sqlite3.connect(db_path)
        self._create_table()

    def _create_table(self):
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS brackets (
                id TEXT PRIMARY KEY,
                bracket_blob BLOB
            )
        """)
        self.conn.commit()

    def create(self, bracket_id, bracket: Bracket):
        import pickle
        if self.read(bracket_id):
            raise ValueError(f"Bracket with id {bracket_id} already exists.")
        blob = pickle.dumps(bracket)
        self.conn.execute("INSERT INTO brackets (id, bracket_blob) VALUES (?, ?)", (bracket_id, blob))
        self.conn.commit()

    def read(self, bracket_id) -> Bracket | None:
        import pickle
        cur = self.conn.execute("SELECT bracket_blob FROM brackets WHERE id = ?", (bracket_id,))
        row = cur.fetchone()
        if row:
            return pickle.loads(row[0])
        return None

    def update(self, bracket_id, bracket: Bracket):
        import pickle
        if not self.read(bracket_id):
            raise KeyError(f"Bracket with id {bracket_id} does not exist.")
        blob = pickle.dumps(bracket)
        self.conn.execute("UPDATE brackets SET bracket_blob = ? WHERE id = ?", (blob, bracket_id))
        self.conn.commit()

    def delete(self, bracket_id):
        self.conn.execute("DELETE FROM brackets WHERE id = ?", (bracket_id,))
        self.conn.commit()

    def list_all(self) -> list[Bracket]:
        import pickle
        cur = self.conn.execute("SELECT bracket_blob FROM brackets")
        return [pickle.loads(row[0]) for row in cur.fetchall()]


class BracketManager:
    """Manages Bracket objects using BracketStore."""
    def __init__(self, store: BracketStore):
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