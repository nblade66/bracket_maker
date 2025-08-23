import sqlite3
from BracketMaker.participant.participant import Participant
from BracketMaker.participant.store.abstract_participant_store import ParticipantStore


class SQLiteParticipantStore(ParticipantStore):
    def __init__(self, db_path: str = "participants.db"):
        self.db_path = db_path
        self._initialize_db()

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
