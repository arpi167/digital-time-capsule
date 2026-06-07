from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# -------------------------
# DATABASE INITIALIZATION
# -------------------------

def init_db():
    conn = sqlite3.connect("database/capsule.db")
    cursor = conn.cursor()

    # Users Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            email TEXT NOT NULL,
            password TEXT NOT NULL
        )
    """)

    # Capsules Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS capsules (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            message TEXT NOT NULL,
            unlock_date TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


init_db()

# -------------------------
# HOME PAGE
# -------------------------

@app.route("/")
def home():
    return render_template("home.html")


# -------------------------
# REGISTER
# -------------------------

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        conn = sqlite3.connect("database/capsule.db")
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
            (username, email, password)
        )

        conn.commit()
        conn.close()

        return redirect("/login")

    return render_template("register.html")


# -------------------------
# LOGIN
# -------------------------

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect("database/capsule.db")
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE username=? AND password=?",
            (username, password)
        )

        user = cursor.fetchone()

        conn.close()

        if user:
            return redirect("/dashboard")
        else:
            return "Invalid Username or Password"

    return render_template("login.html")


# -------------------------
# DASHBOARD
# -------------------------

@app.route("/dashboard")
def dashboard():

    conn = sqlite3.connect("database/capsule.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT title, message, unlock_date FROM capsules"
    )

    capsules = cursor.fetchall()

    conn.close()

    return render_template(
        "dashboard.html",
        capsules=capsules
    )


# -------------------------
# CREATE CAPSULE
# -------------------------

@app.route("/create-capsule", methods=["GET", "POST"])
def create_capsule():

    if request.method == "POST":

        title = request.form["title"]
        message = request.form["message"]
        unlock_date = request.form["unlock_date"]

        conn = sqlite3.connect("database/capsule.db")
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO capsules
            (title, message, unlock_date)
            VALUES (?, ?, ?)
            """,
            (title, message, unlock_date)
        )

        conn.commit()
        conn.close()

        return redirect("/dashboard")

    return render_template("create_capsule.html")


# -------------------------
# START APP
# -------------------------

if __name__ == "__main__":
    app.run(debug=True)