import sqlite3

db = sqlite3.connect("database.db")
cursor = db.cursor()

cursor.execute("SELECT * FROM books")
rows = cursor.fetchall()

print(rows)
