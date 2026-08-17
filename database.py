import sqlite3

DB_NAME = "bot.db"


def connect():
    return sqlite3.connect(DB_NAME)


def init_db():
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT,
            first_name TEXT,
            last_name TEXT,
            balance INTEGER DEFAULT 0
        )
    """)

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

    conn.commit()
    conn.close()


def save_user(
    user_id,
    username=None,
    first_name=None,
    last_name=None
):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO users
        (id, username, first_name, last_name, balance)
        VALUES (?, ?, ?, ?, 0)

        ON CONFLICT(id) DO UPDATE SET
            username = excluded.username,
            first_name = excluded.first_name,
            last_name = excluded.last_name
    """, (
        user_id,
        username,
        first_name,
        last_name
    ))

    conn.commit()
    conn.close()


def get_user(user_id):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, username, first_name, last_name, balance
        FROM users
        WHERE id = ?
    """, (user_id,))

    result = cursor.fetchone()

    conn.close()

    return result


def get_balance(user_id):
    user = get_user(user_id)

    if not user:
        return 0

    return user[4]


def add_balance(user_id, amount):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE users
        SET balance = balance + ?
        WHERE id = ?
    """, (amount, user_id))

    conn.commit()
    conn.close()


def remove_balance(user_id, amount):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE users
        SET balance = balance - ?
        WHERE id = ?
        AND balance >= ?
    """, (amount, user_id, amount))

    changed = cursor.rowcount

    conn.commit()
    conn.close()

    return changed > 0
