from BracketMaker.bracket.bracket import Bracket
from BracketMaker.bracket.store.abstract_bracket_store import BracketStore
import sqlite3

class SQLiteBracketStore(BracketStore):
    """SQLite implementation of BracketStore."""
    def __init__(self, db_path=":memory:"):
        self.db_path = db_path
        self._create_table()

    def _create_table(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS brackets (
                    id TEXT PRIMARY KEY,
                    bracket_blob BLOB
                )
            """)
            conn.commit()

    def create(self, bracket_id, bracket: Bracket):
        import pickle
        if self.read(bracket_id):
            raise ValueError(f"Bracket with id {bracket_id} already exists.")
        blob = pickle.dumps(bracket)
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("INSERT INTO brackets (id, bracket_blob) VALUES (?, ?)", (bracket_id, blob))
            conn.commit()

    def read(self, bracket_id) -> Bracket | None:
        import pickle
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.execute("SELECT bracket_blob FROM brackets WHERE id = ?", (bracket_id,))
            row = cur.fetchone()
            if row:
                return pickle.loads(row[0])
        return None

    def update(self, bracket_id, bracket: Bracket):
        import pickle
        if not self.read(bracket_id):
            raise KeyError(f"Bracket with id {bracket_id} does not exist.")
        blob = pickle.dumps(bracket)
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("UPDATE brackets SET bracket_blob = ? WHERE id = ?", (blob, bracket_id))
            conn.commit()

    def delete(self, bracket_id):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("DELETE FROM brackets WHERE id = ?", (bracket_id,))
            conn.commit()

    def list_all(self) -> list[Bracket]:
        import pickle
        cur = []
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.execute("SELECT bracket_blob FROM brackets")
        return [pickle.loads(row[0]) for row in cur.fetchall()]
