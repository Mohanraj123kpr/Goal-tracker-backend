"""
Migration script — run once: python migrate.py
Adds: users table, due_date/plan/user_id columns to goals
"""
import sqlite3

conn = sqlite3.connect("goals.db")
cursor = conn.cursor()

# Create users table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT UNIQUE NOT NULL,
        name TEXT NOT NULL,
        hashed_password TEXT NOT NULL,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
""")
print("users table ready")

# Add columns to goals if missing
for col, definition in [
    ("due_date", "DATE"),
    ("plan", "TEXT"),
    ("user_id", "INTEGER REFERENCES users(id)"),
]:
    try:
        cursor.execute(f"ALTER TABLE goals ADD COLUMN {col} {definition}")
        print(f"Added column: {col}")
    except sqlite3.OperationalError:
        print(f"Column already exists: {col}")

conn.commit()
conn.close()
print("Migration complete.")
