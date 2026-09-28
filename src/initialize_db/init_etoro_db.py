import sqlite3
from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

DB_PATH = Path(os.getenv("ETORO_DB_PATH", ""))
if not DB_PATH:
    raise ValueError("ETORO_DB_PATH environment variable is not set.")


def get_connection() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row

    return connection


def init_db() -> None:
    with get_connection() as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS h_deposits (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                amount REAL NOT NULL,
                currency TEXT NOT NULL DEFAULT 'USD',
                deposited_at TEXT NOT NULL,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
        """)

        connection.commit()


if __name__ == "__main__":
    init_db()
    print(f"Database initialized: {DB_PATH}")