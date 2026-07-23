import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

DATA_DIR = os.environ.get("DATA_DIR", "data")
DB_PATH = os.path.join(DATA_DIR, "todos.db")


def get_connection():
    os.makedirs(DATA_DIR, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS todos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task TEXT NOT NULL,
            done INTEGER NOT NULL DEFAULT 0,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
        """
    )
    conn.commit()
    conn.close()


@app.route("/")
def index():
    conn = get_connection()
    todos = conn.execute(
        "SELECT * FROM todos ORDER BY done ASC, created_at DESC"
    ).fetchall()
    conn.close()
    total = len(todos)
    done_count = sum(1 for t in todos if t["done"])
    return render_template(
        "index.html", todos=todos, total=total, done_count=done_count
    )


@app.route("/add", methods=["POST"])
def add():
    task = request.form.get("task", "").strip()
    if task:
        conn = get_connection()
        conn.execute("INSERT INTO todos (task) VALUES (?)", (task,))
        conn.commit()
        conn.close()
    return redirect(url_for("index"))


@app.route("/toggle/<int:todo_id>", methods=["POST"])
def toggle(todo_id):
    conn = get_connection()
    conn.execute(
        "UPDATE todos SET done = 1 - done WHERE id = ?", (todo_id,)
    )
    conn.commit()
    conn.close()
    return redirect(url_for("index"))


@app.route("/delete/<int:todo_id>", methods=["POST"])
def delete(todo_id):
    conn = get_connection()
    conn.execute("DELETE FROM todos WHERE id = ?", (todo_id,))
    conn.commit()
    conn.close()
    return redirect(url_for("index"))


init_db()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
