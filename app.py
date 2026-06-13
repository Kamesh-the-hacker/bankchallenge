import sqlite3
import os
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

# ================= DATABASE SETUP =================
def init_db():
    if not os.path.exists("bank.db"):
        conn = sqlite3.connect("bank.db")
        cur = conn.cursor()

        cur.execute("""
        CREATE TABLE users(
            username TEXT,
            password TEXT
        )
        """)

        # default user
        cur.execute("INSERT INTO users VALUES('kundu','kundama')")

        conn.commit()
        conn.close()

init_db()

# ================= ROUTES =================

# 🏠 LOGIN PAGE
@app.route("/", methods=["GET", "POST"])
def login():
    msg = ""

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        conn = sqlite3.connect("bank.db")
        cur = conn.cursor()

        # ❌ INTENTIONALLY VULNERABLE (SQLi)
        query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
        result = cur.execute(query).fetchone()

        if result:
            return redirect("/dashboard")
        else:
            msg = "Invalid credentials"

        conn.close()

    return render_template("login.html", msg=msg)


# 🏦 DASHBOARD (FLAG HERE)
@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


# ================= RUN =================
if __name__ == "__main__":
    app.run(debug=True)