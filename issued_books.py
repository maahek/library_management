import sqlite3

db = sqlite3.connect("database.db")
db.execute("""
CREATE TABLE IF NOT EXISTS issued_books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_name TEXT,
    book_name TEXT,
    status TEXT
)
""")
db.commit()
db.close()
