import sqlite3

conn = sqlite3.connect("responses.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    skill TEXT,
    interest TEXT,
    cgpa REAL,
    result TEXT
)
""")

conn.commit()
conn.close()

print("Database Created Successfully")