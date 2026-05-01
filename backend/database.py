import sqlite3
import json

DB_PATH = "chain.db"


def init_db():
    """Create the blocks table if it doesn't exist."""
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS blocks (
            idx       INTEGER PRIMARY KEY,
            sender    TEXT NOT NULL,
            receiver  TEXT NOT NULL,
            amount    REAL NOT NULL,
            category  TEXT NOT NULL,
            prev_hash TEXT NOT NULL,
            hash      TEXT NOT NULL,
            timestamp REAL NOT NULL
        )
    """)
    conn.commit()
    conn.close()


def save_block(block: dict):
    """Save a new block to the database."""
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        "INSERT OR IGNORE INTO blocks VALUES (?,?,?,?,?,?,?,?)",
        (
            block["index"],
            block["sender"],
            block["receiver"],
            block["amount"],
            block["category"],
            block["previous_hash"],
            block["hash"],
            block["timestamp"]
        )
    )
    conn.commit()
    conn.close()


def load_all_blocks() -> list:
    """Load all blocks from database, ordered by index."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    rows = conn.execute("SELECT * FROM blocks ORDER BY idx").fetchall()
    conn.close()
    return [dict(row) for row in rows]


def clear_db():
    """Clear all blocks (for testing/reset)."""
    conn = sqlite3.connect(DB_PATH)
    conn.execute("DELETE FROM blocks")
    conn.commit()
    conn.close()