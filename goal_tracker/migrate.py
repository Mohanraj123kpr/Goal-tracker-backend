"""
Simple migration script to add due_date and plan columns to existing goals table.
Run once: python migrate.py
"""
import sqlite3

conn = sqlite3.connect("goals.db")
cursor = conn.cursor()

# Add due_date column if it doesn't exist
try:
    cursor.execute("ALTER TABLE goals ADD COLUMN due_date DATE")
    print("Added due_date column")
except sqlite3.OperationalError:
    print("due_date column already exists")

# Add plan column if it doesn't exist
try:
    cursor.execute("ALTER TABLE goals ADD COLUMN plan TEXT")
    print("Added plan column")
except sqlite3.OperationalError:
    print("plan column already exists")

conn.commit()
conn.close()
print("Migration complete.")
