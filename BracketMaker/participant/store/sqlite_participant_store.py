import sqlite3
import os
from BracketMaker.participant.participant import Participant
from BracketMaker.participant.store.abstract_participant_store import ParticipantStore


class SQLiteParticipantStore(ParticipantStore):
    """Stores participants in a SQLite database with a unique db file name if not specified."""
    def __init__(self, db_path: str = None):
        if db_path is None:
            db_path = self._get_unique_db_path()
        self.db_path = db_path
        self._initialize_db()

    def _get_unique_db_path(self):
        base_dir = "data/participants"
        os.makedirs(base_dir, exist_ok=True)
        base_name = "participants"
        ext = ".db"
        i = 1
        while True:
            candidate = os.path.join(base_dir, f"{base_name}_{i}{ext}")
            if not os.path.exists(candidate):
                return candidate
            i += 1

    def _initialize_db(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS participants (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL
                    -- Add more fields here if needed
                )
            ''')
            conn.commit()

    def add_participant(self, participant: Participant) -> Participant:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO participants (name)
                VALUES (?)
                RETURNING id, name
            ''', (participant.name,))
            row = cursor.fetchone()
            conn.commit()
            return Participant(id=row[0], name=row[1])

    def remove_participant(self, participant_id: int) -> bool:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM participants WHERE id = ?', (participant_id,))
            conn.commit()
            return cursor.rowcount > 0

    def get_participant(self, participant_id: int) -> Participant | None:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT id, name FROM participants WHERE id = ?', (participant_id,))
            row = cursor.fetchone()
            if row:
                participant = Participant(name=row[1])
                participant.id = row[0]
                return participant
            return None

    def list_participants(self) -> list[Participant]:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT id, name FROM participants')
            rows = cursor.fetchall()
            return [Participant(id=row[0], name=row[1]) for row in rows]

    def clear(self) -> None:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM participants')
            conn.commit()
