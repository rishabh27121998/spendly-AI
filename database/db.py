import os
import sqlite3
from datetime import date, timedelta

from werkzeug.security import generate_password_hash

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "expense_tracker.db")

CATEGORIES = ["Food", "Transport", "Bills", "Health", "Entertainment", "Shopping", "Other"]


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TEXT DEFAULT (datetime('now'))
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            date TEXT NOT NULL,
            description TEXT,
            created_at TEXT DEFAULT (datetime('now')),
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    """)
    conn.commit()
    conn.close()


def seed_db():
    conn = get_db()
    existing = conn.execute("SELECT 1 FROM users LIMIT 1").fetchone()
    if existing is not None:
        conn.close()
        return

    password_hash = generate_password_hash("demo123")
    cursor = conn.execute(
        "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
        ("Demo User", "demo@spendly.com", password_hash),
    )
    user_id = cursor.lastrowid

    today = date.today()
    first_of_month = today.replace(day=1)
    days_elapsed = (today - first_of_month).days
    offsets = [round(days_elapsed * i / 7) for i in range(8)]
    sample_dates = [(first_of_month + timedelta(days=o)).isoformat() for o in offsets]

    sample_expenses = [
        (user_id, 450.0, "Food", sample_dates[0], "Groceries at DMart"),
        (user_id, 220.0, "Food", sample_dates[1], "Lunch with colleagues"),
        (user_id, 150.0, "Transport", sample_dates[2], "Uber to office"),
        (user_id, 1200.0, "Bills", sample_dates[3], "Electricity bill"),
        (user_id, 600.0, "Health", sample_dates[4], "Pharmacy - medicines"),
        (user_id, 350.0, "Entertainment", sample_dates[5], "Movie tickets"),
        (user_id, 1499.0, "Shopping", sample_dates[6], "New shoes"),
        (user_id, 100.0, "Other", sample_dates[7], "Miscellaneous"),
    ]
    conn.executemany(
        "INSERT INTO expenses (user_id, amount, category, date, description) "
        "VALUES (?, ?, ?, ?, ?)",
        sample_expenses,
    )
    conn.commit()
    conn.close()
