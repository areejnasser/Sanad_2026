"""The memory log: every sighting is stored as text (object, room, time)."""
import os
import sqlite3
from datetime import datetime
from config import DB_PATH

SCHEMA = """
CREATE TABLE IF NOT EXISTS sightings (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    object     TEXT NOT NULL,
    room       TEXT NOT NULL,
    confidence REAL NOT NULL,
    seen_at    TEXT NOT NULL            -- ISO time, local clock
);
CREATE INDEX IF NOT EXISTS idx_object_time ON sightings(object, seen_at);
"""


class Memory:
    def __init__(self, path: str = DB_PATH):
        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
        self.db = sqlite3.connect(path, check_same_thread=False)
        self.db.executescript(SCHEMA)

    def add(self, obj: str, room: str, confidence: float, when: datetime | None = None):
        when = when or datetime.now()
        self.db.execute(
            "INSERT INTO sightings(object, room, confidence, seen_at) VALUES (?,?,?,?)",
            (obj, room, round(confidence, 3), when.isoformat(timespec="seconds")))
        self.db.commit()

    def last_seen(self, obj: str):
        """Most recent sighting of an object, or None."""
        row = self.db.execute(
            "SELECT object, room, confidence, seen_at FROM sightings "
            "WHERE object=? ORDER BY seen_at DESC LIMIT 1", (obj,)).fetchone()
        if not row:
            return None
        return {"object": row[0], "room": row[1], "confidence": row[2],
                "seen_at": datetime.fromisoformat(row[3])}

    def history(self, obj: str, limit: int = 10):
        rows = self.db.execute(
            "SELECT room, confidence, seen_at FROM sightings WHERE object=? "
            "ORDER BY seen_at DESC LIMIT ?", (obj, limit)).fetchall()
        return [{"room": r[0], "confidence": r[1], "seen_at": r[2]} for r in rows]

    def delete_all(self):
        """Privacy: the user or family can wipe the log."""
        self.db.execute("DELETE FROM sightings")
        self.db.commit()
