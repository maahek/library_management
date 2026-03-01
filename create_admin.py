from werkzeug.security import generate_password_hash
import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

hashed_password = generate_password_hash("admin123")

cursor.execute("INSERT INTO librarian (username, password) VALUES (?, ?)", ("admin", hashed_password))

conn.commit()
conn.close()

print("Admin user created successfully!")