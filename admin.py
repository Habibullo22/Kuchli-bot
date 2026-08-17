import sqlite3

from config import ADMIN_ID

DB_NAME = "bot.db"


def is_admin(user_id):
    return user_id == ADMIN_ID


def get_pending_payments():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, user_id, amount, method, created_at
        FROM payments
        WHERE status = 'pending'
        ORDER BY id DESC
    """)

    payments = cursor.fetchall()
    conn.close()

    return payments


def approve_payment(payment_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE payments
        SET status = 'approved'
        WHERE id = ? AND status = 'pending'
    """, (payment_id,))

    changed = cursor.rowcount

    conn.commit()
    conn.close()

    return changed > 0


def reject_payment(payment_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE payments
        SET status = 'rejected'
        WHERE id = ? AND status = 'pending'
    """, (payment_id,))

    changed = cursor.rowcount

    conn.commit()
    conn.close()

    return changed > 0
