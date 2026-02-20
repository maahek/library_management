import sqlite3

db = sqlite3.connect("database.db")
cur = db.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS issued_books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER,
    student_name TEXT,
    book_id INTEGER,
    book_name TEXT,
    issue_date TEXT,
    return_date TEXT,
    status TEXT
)
""")

db.commit()
db.close()

print("issued_books table ready")
