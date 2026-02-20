import sqlite3

db = sqlite3.connect("database.db")
cur = db.cursor()

# add issue_date column
try:
    cur.execute("ALTER TABLE issued_books ADD COLUMN issue_date TEXT")
except:
    print("issue_date already exists")

# add return_date column
try:
    cur.execute("ALTER TABLE issued_books ADD COLUMN return_date TEXT")
except:
    print("return_date already exists")

# add student_id column
try:
    cur.execute("ALTER TABLE issued_books ADD COLUMN student_id INTEGER")
except:
    print("student_id already exists")

# add book_id column
try:
    cur.execute("ALTER TABLE issued_books ADD COLUMN book_id INTEGER")
except:
    print("book_id already exists")

db.commit()
db.close()

print("Columns added successfully")
