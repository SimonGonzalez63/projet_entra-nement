# db.py
import sqlite3
from pathlib import Path

DB_PATH = Path("quaytracker.db")

def get_connection():
    return sqlite3.connect(DB_PATH)

def init_db():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS ship (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL,
        type TEXT,
        status TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS zone (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        description TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS task (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT,
        ship_id INTEGER NOT NULL,
        zone_id INTEGER NOT NULL,
        status TEXT NOT NULL,
        start_date TEXT,
        end_date TEXT,
        FOREIGN KEY(ship_id) REFERENCES ship(id),
        FOREIGN KEY(zone_id) REFERENCES zone(id)
    )
    """)

    conn.commit()
    conn.close()
