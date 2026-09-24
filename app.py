from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
from database.db import init_db, seed_db, create_user, verify_user, get_user_by_id

app = Flask(__name__)
app.secret_key = "dev-secret-key-for-spendly"

with app.app_context():
    init_db()
    seed_db()


# ------------------------------------------------------------------ #
# Routes                                                              #
# ------------------------------------------------------------------ #

@app.route("/")
def landing():
    return render_template("landing.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if session.get("user_id"):
        return redirect(url_for("landing"))

    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        if password != confirm_password:
            return render_template("register.html", error="Passwords do not match")

        try:
            create_user(name, email, password)
            return redirect(url_for("login"))
        except sqlite3.IntegrityError:
            return render_template("register.html", error="Email already registered")

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if session.get("user_id"):
        return redirect(url_for("landing"))

    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = verify_user(email, password)
        if user:
            session["user_id"] = user["id"]
            return redirect(url_for("landing"))

        return render_template("login.html", error="Invalid credentials")

    return render_template("login.html")


@app.route("/terms")
def terms():
    return render_template("terms.html")


@app.route("/privacy")
def privacy():
    return render_template("privacy.html")




# ------------------------------------------------------------------ #
# Placeholder routes — students will implement these                  #
# ------------------------------------------------------------------ #

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("landing"))


@app.route("/profile")
def profile():
    user_id = session.get("user_id")
    if not user_id:
        return redirect(url_for("login"))

    # Hardcoded mock data for UI validation phase
    user = {
        "name": "Demo User",
        "email": "demo@spendly.com",
        "member_since": "September 2026"
    }

    stats = {
        "total_spent": "₹12,450.00",
        "transactions": 42,
        "top_category": "Food"
    }

    recent_transactions = [
        {"date": "2026-09-20", "desc": "Lunch at Cafe", "cat": "Food", "amt": "-₹450.00"},
        {"date": "2026-09-19", "desc": "Bus Fare", "cat": "Transport", "amt": "-₹20.00"},
        {"date": "2026-09-18", "desc": "Monthly Internet", "cat": "Bills", "amt": "-₹799.00"},
        {"date": "2026-09-17", "desc": "Pharmacy", "cat": "Health", "amt": "-₹1,200.00"},
        {"date": "2026-09-15", "desc": "Cinema Ticket", "cat": "Entertainment", "amt": "-₹300.00"},
    ]

    categories = [
        {"name": "Food", "spent": 4500, "percent": 36},
        {"name": "Transport", "spent": 2100, "percent": 17},
        {"name": "Bills", "spent": 3200, "percent": 26},
        {"name": "Health", "spent": 1500, "percent": 12},
        {"name": "Other", "spent": 1150, "percent": 9},
    ]

    return render_template("profile.html", user=user, stats=stats, transactions=recent_transactions, categories=categories)


@app.route("/expenses/add")
def add_expense():
    return "Add expense — coming in Step 7"


@app.route("/expenses/<int:id>/edit")
def edit_expense(id):
    return "Edit expense — coming in Step 8"


@app.route("/expenses/<int:id>/delete")
def delete_expense(id):
    return "Delete expense — coming in Step 9"


if __name__ == "__main__":
    app.run(debug=True, port=5001)
