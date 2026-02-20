import sqlite3

db = sqlite3.connect("database.db")
db.execute("""
CREATE TABLE IF NOT EXISTS books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    author TEXT,
    quantity INTEGER,
    image TEXT,
    description TEXT
)
""")
db.commit()
db.close()

print("Database and table created successfully.")

