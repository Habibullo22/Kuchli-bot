import sqlite3
from datetime import datetime

DB_NAME = "bot.db"


def create_payment(user_id, amount, method):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS payments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            amount INTEGER NOT NULL,
            method TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'pending',
            created_at TEXT NOT NULL
        )
    """)

    cursor.execute("""
        INSERT INTO payments
        (user_id, amount, method, status, created_at)
        VALUES (?, ?, ?, 'pending', ?)
    """, (
        user_id,
        amount,
        method,
        datetime.now().isoformat()
    ))

    payment_id = cursor.lastrowid

    conn.commit()
    conn.close()

    return payment_id


def get_payment(payment_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, user_id, amount, method, status, created_at
        FROM payments
        WHERE id = ?
    """, (payment_id,))

    result = cursor.fetchone()

    conn.close()

    return result


def update_payment_status(payment_id, status):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE payments
        SET status = ?
        WHERE id = ?
    """, (status, payment_id))

    conn.commit()
    conn.close()
