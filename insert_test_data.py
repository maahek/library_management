import sqlite3

db = sqlite3.connect("database.db")

db.execute("INSERT INTO students (name) VALUES ('Ates')")
db.execute("INSERT INTO students (name) VALUES ('Salar')")
db.execute("INSERT INTO students (name) VALUES ('Faris')")
db.execute("INSERT INTO issued_books (student_name, book_name, status) VALUES ('Arjun', 'Python', 'Issued')")
db.execute("INSERT INTO issued_books (student_name, book_name, status) VALUES ('Salar', 'Economics', 'Issued')")
db.execute("INSERT INTO issued_books (student_name, book_name, status) VALUES ('Faris', 'Economics', 'Due')")
db.commit()
db.close()
