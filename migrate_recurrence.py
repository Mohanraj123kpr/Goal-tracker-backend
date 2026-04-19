"""
Migration: adds recurrence and last_reset columns to goals table.
Works for both PostgreSQL and SQLite.
Run once: python migrate_recurrence.py
"""
import os
from dotenv import load_dotenv
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./goals.db")

if DATABASE_URL.startswith("sqlite"):
    import sqlite3
    path = DATABASE_URL.replace("sqlite:///", "")
    conn = sqlite3.connect(path)
    cursor = conn.cursor()
    for col, definition in [
        ("recurrence", "TEXT NOT NULL DEFAULT 'none'"),
        ("last_reset",  "DATE"),
    ]:
        try:
            cursor.execute(f"ALTER TABLE goals ADD COLUMN {col} {definition}")
            print(f"Added column: {col}")
        except sqlite3.OperationalError:
            print(f"Column already exists: {col}")
    conn.commit()
    conn.close()
else:
    import psycopg2
    conn = psycopg2.connect(DATABASE_URL)
    conn.autocommit = True
    cursor = conn.cursor()
    for col, definition in [
        ("recurrence", "VARCHAR NOT NULL DEFAULT 'none'"),
        ("last_reset",  "DATE"),
    ]:
        try:
            cursor.execute(f"ALTER TABLE goals ADD COLUMN IF NOT EXISTS {col} {definition}")
            print(f"Added column: {col}")
        except Exception as e:
            print(f"Skipped {col}: {e}")
    cursor.close()
    conn.close()

print("Migration complete.")
