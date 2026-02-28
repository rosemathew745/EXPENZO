from flask import Flask, render_template, request, redirect
import sqlite3
import datetime

app = Flask(__name__)

@app.route('/stock')
def stock():
    return render_template('stock.html')
# Create database
def init_db():
    conn = sqlite3.connect("expenses.db")
    c = conn.cursor()

    c.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            amount REAL,
            month TEXT
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS budget (
            id INTEGER PRIMARY KEY,
            amount REAL
        )
    ''')

    conn.commit()
    conn.close()

init_db()

@app.route("/")
def index():
    conn = sqlite3.connect("expenses.db")
    c = conn.cursor()

    current_month = datetime.datetime.now().strftime("%B %Y")

    c.execute("SELECT * FROM expenses WHERE month=?", (current_month,))
    expenses = c.fetchall()

    c.execute("SELECT SUM(amount) FROM expenses WHERE month=?", (current_month,))
    total = c.fetchone()[0]
    total = total if total else 0

    c.execute("SELECT amount FROM budget WHERE id=1")
    budget_data = c.fetchone()
    budget = budget_data[0] if budget_data else 0

    remaining = budget - total
    alert = total > budget and budget != 0

    c.execute("SELECT month, SUM(amount) FROM expenses GROUP BY month")
    history = c.fetchall()

    conn.close()

    return render_template(
        "index.html",
        expenses=expenses,
        total=total,
        budget=budget,
        remaining=remaining,
        alert=alert,
        month=current_month,
        history=history
    )

@app.route("/add", methods=["POST"])
def add():
    title = request.form["title"]
    amount = float(request.form["amount"])
    month = datetime.datetime.now().strftime("%B %Y")

    conn = sqlite3.connect("expenses.db")
    c = conn.cursor()
    c.execute("INSERT INTO expenses (title, amount, month) VALUES (?, ?, ?)",
              (title, amount, month))
    conn.commit()
    conn.close()

    return redirect("/")

@app.route("/delete/<int:id>")
def delete(id):
    conn = sqlite3.connect("expenses.db")
    c = conn.cursor()
    c.execute("DELETE FROM expenses WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect("/")

@app.route("/set_budget", methods=["POST"])
def set_budget():
    amount = float(request.form["budget"])

    conn = sqlite3.connect("expenses.db")
    c = conn.cursor()

    c.execute("DELETE FROM budget")
    c.execute("INSERT INTO budget (id, amount) VALUES (1, ?)", (amount,))

    conn.commit()
    conn.close()

    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)