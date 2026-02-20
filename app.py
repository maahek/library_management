from flask import Flask, render_template,request, redirect
from datetime import datetime, timedelta
from flask import jsonify
import os
import sqlite3

app = Flask(__name__)
UPLOAD_FOLDER = "static/uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
def get_db():
    return sqlite3.connect("database.db")

@app.route("/")
@app.route("/home")
def home():
    db = get_db()
    cur = db.cursor()

    # Total books
    cur.execute("SELECT COUNT(*) FROM books")
    total_books = cur.fetchone()[0]

    # Total students
    cur.execute("SELECT COUNT(*) FROM students")
    total_students = cur.fetchone()[0]

    # Issued books table
    cur.execute("SELECT student_name, book_name, status FROM issued_books")
    issued = cur.fetchall()

    # Chart data
    cur.execute("SELECT COUNT(*) FROM issued_books WHERE status='Issued'")
    issued_count = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM issued_books WHERE status='Due'")
    due_count = cur.fetchone()[0]

    available_books = total_books - issued_count

    db.close()

    return render_template(
        "home.html",
        total_books=total_books,
        total_students=total_students,
        issued=issued,
        issued_count=issued_count,
        due_count=due_count,
        available_books=available_books
    )
@app.route("/reports")
def reports():
    db = get_db()
    cur = db.cursor()

    # Total books
    cur.execute("SELECT COUNT(*) FROM books")
    total_books = cur.fetchone()[0]

    # Total students
    cur.execute("SELECT COUNT(*) FROM students")
    total_students = cur.fetchone()[0]

    # Issued books table
    cur.execute("SELECT student_name, book_name, status FROM issued_books")
    issued = cur.fetchall()

    # Chart data
    cur.execute("SELECT COUNT(*) FROM issued_books WHERE status='Issued'")
    issued_count = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM issued_books WHERE status='Due'")
    due_count = cur.fetchone()[0]

    available_books = total_books - issued_count

    cur.execute("""SELECT student_name, book_name, status FROM issued_books ORDER BY id DESC""")
    
    records = cur.fetchall()

    db.close()

    return render_template(
        "reports.html",
        total_books=total_books,
        total_students=total_students,
        issued=issued,
        issued_count=issued_count,
        due_count=due_count,
        available_books=available_books,
        records=records
    )

@app.route("/add_book", methods=["GET", "POST"])
def add_book():
    if request.method == "POST":
        name = request.form.get("name")
        author = request.form.get("author")
        quantity = request.form.get("quantity")
        description = request.form.get("description")
        image = request.files.get("image")
        image_path = None

        if image and image.filename != "":
            image_path = os.path.join(app.config["UPLOAD_FOLDER"], image.filename)
            image.save(image_path)

        db = get_db()
        cur = db.cursor()
        cur.execute(
            "INSERT INTO books (name, author, quantity, image, description) VALUES (?, ?, ?, ?, ?)",
            (name, author, quantity, image.filename if image else None, description)
        )
        db.commit()
        db.close()

        return redirect("/")
    return render_template("add_book.html")

@app.route("/issue_book", methods=["GET", "POST"])
def issue_book():

    db = get_db()
    cur = db.cursor()

    cur.execute("SELECT id, name, image FROM books")
    books = cur.fetchall()

    cur.execute("SELECT id, name FROM students")
    students = cur.fetchall()

    if request.method == "POST":

        print(request.form)

        student_id = request.form["student_id"]
        book_id = request.form["book_id"]

        issue_date = datetime.now().strftime("%Y-%m-%d")
        return_date = (datetime.now() + timedelta(days=14)).strftime("%Y-%m-%d")

        cur.execute("SELECT name FROM students WHERE id=?", (student_id,))
        student_name = cur.fetchone()[0]

        cur.execute("SELECT name FROM books WHERE id=?", (book_id,))
        book_name = cur.fetchone()[0]

        cur.execute("""
        INSERT INTO issued_books
        (student_id, student_name, book_id, book_name, issue_date, return_date, status)
        VALUES (?, ?, ?, ?, ?, ?, 'Issued')
        """, (student_id, student_name, book_id, book_name, issue_date, return_date))
        # decrease quantity
        cur.execute("""
                    UPDATE books
                    SET quantity = quantity - 1
                    WHERE id=?
                    """, (book_id,))

        db.commit()

        return redirect("/")

    return render_template("issue_book.html", books=books, students=students)

@app.route("/return_book/<int:id>")
def return_book_action(id):

    db = get_db()
    cur = db.cursor()

    # get book_id and return_date
    cur.execute("""
    SELECT book_id, return_date
    FROM issued_books
    WHERE id=?
    """, (id,))

    result = cur.fetchone()

    book_id = result[0]
    return_date = result[1]

    # calculate fine
    fine = 0

    today = datetime.now().date()
    due = datetime.strptime(return_date, "%Y-%m-%d").date()

    if today > due:
        days_late = (today - due).days
        fine = days_late * 5   # ₹5 per day

    # update issued_books
    cur.execute("""
    UPDATE issued_books
    SET status='Returned'
    WHERE id=?
    """, (id,))

    # increase book quantity
    cur.execute("""
    UPDATE books
    SET quantity = quantity + 1
    WHERE id=?
    """, (book_id,))

    db.commit()
    db.close()

    return redirect("/return_book")

@app.route("/return_book")
def return_book_page():

    db = get_db()
    cur = db.cursor()

    cur.execute("""
        SELECT id, student_name, book_name,
               issue_date, return_date, status
        FROM issued_books
        ORDER BY id DESC
    """)

    rows = cur.fetchall()
    db.close()

    today = datetime.now().date()

    records = []

    for row in rows:

        fine = 0
        overdue = False

        if row[5] == "Issued" and row[4]:

            due_date = datetime.strptime(row[4], "%Y-%m-%d").date()

            if today > due_date:
                overdue = True
                fine = (today - due_date).days * 5

        records.append({

            "id": row[0],
            "student": row[1],
            "book": row[2],
            "issue_date": row[3],
            "return_date": row[4],
            "status": row[5],
            "fine": fine,
            "overdue": overdue

        })

    return render_template(
        "return_book.html",
        records=records
    )


@app.route("/calculate_fine/<int:id>")
def calculate_fine(id):

    db = get_db()
    cur = db.cursor()

    cur.execute("""
        SELECT return_date
        FROM issued_books
        WHERE id=?
    """, (id,))

    result = cur.fetchone()

    fine = 0

    if result and result[0]:
        due_date = datetime.strptime(result[0], "%Y-%m-%d").date()
        today = datetime.now().date()

        if today > due_date:
            fine = (today - due_date).days * 5

    db.close()

    return jsonify({"fine": fine})

@app.route("/members")
def members():
    db = get_db()
    cur = db.cursor()

    cur.execute("SELECT * FROM students ORDER BY id DESC")

    rows = cur.fetchall()
    db.close()

    members = []

    for r in rows:
        members.append({
            "id": r[0],
            "name": r[1],
            "email": r[2],
            "phone": r[3]
        })
    return render_template("members.html", members=members)

@app.route("/add_member", methods=["GET", "POST"])
def add_member():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        phone = request.form["phone"]

        db = get_db()
        cur = db.cursor()

        cur.execute("""
INSERT INTO students (name, email, phone) VALUES (?, ?, ?)
""", (name, email, phone))
        
        db.commit()
        db.close()
        return redirect("/members")
    return render_template("add_member.html")

if __name__ == "__main__":
    app.run(debug=True)