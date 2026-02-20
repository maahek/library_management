import sqlite3

db = sqlite3.connect("database.db")
db.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    email TEXT,
    phone TEXT
)
""")
db.commit()
db.close()