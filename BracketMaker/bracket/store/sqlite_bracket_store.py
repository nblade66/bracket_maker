import sqlite3
import pickle
from BracketMaker.bracket.bracket import Bracket
from BracketMaker.bracket.store.abstract_bracket_store import BracketStore

class SQLiteBracketStore(BracketStore):
    """SQLite implementation of BracketStore with user_id support."""
    def __init__(self, db_path="data/brackets/brackets.db"):
        self.db_path = db_path
        self._create_table()

    def _create_table(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS brackets (
                    id TEXT PRIMARY KEY,
                    user_id TEXT NOT NULL,
                    bracket_blob BLOB
                )
            """)
            conn.commit()

    def create(self, bracket_id, bracket: Bracket, user_id: str):
        # Check for global uniqueness of bracket_id
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.execute(
                "SELECT 1 FROM brackets WHERE id = ?",
                (bracket_id,)
            )
            if cur.fetchone():
                raise ValueError(f"Bracket with id {bracket_id} already exists.")
            blob = pickle.dumps(bracket)
            conn.execute(
                "INSERT INTO brackets (id, user_id, bracket_blob) VALUES (?, ?, ?)",
                (bracket_id, user_id, blob)
            )
            conn.commit()

    def read(self, bracket_id, user_id: str) -> Bracket | None:
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.execute(
                "SELECT bracket_blob FROM brackets WHERE id = ? AND user_id = ?",
                (bracket_id, user_id)
            )
            row = cur.fetchone()
            if row:
                return pickle.loads(row[0])
        return None

    def update(self, bracket_id, bracket: Bracket, user_id: str):
        if not self.read(bracket_id, user_id):
            raise KeyError(f"Bracket with id {bracket_id} does not exist for user {user_id}.")
        blob = pickle.dumps(bracket)
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                "UPDATE brackets SET bracket_blob = ? WHERE id = ? AND user_id = ?",
                (blob, bracket_id, user_id)
            )
            conn.commit()

    def delete(self, bracket_id, user_id: str):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                "DELETE FROM brackets WHERE id = ? AND user_id = ?",
                (bracket_id, user_id)
            )
            conn.commit()

    def list_all(self, user_id: str) -> list[Bracket]:
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.execute(
                "SELECT bracket_blob FROM brackets WHERE user_id = ?",
                (user_id,)
            )
            return [pickle.loads(row[0]) for row in cur.fetchall()]

    def bracket_id_exists(self, bracket_id: str) -> bool:
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.execute("SELECT 1 FROM brackets WHERE id = ?", (bracket_id,))
            return cur.fetchone() is not None
