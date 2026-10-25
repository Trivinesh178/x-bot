import sqlite3
import time
from contextlib import closing

DB_PATH = "grokcord.db"


def _conn():
    return sqlite3.connect(DB_PATH)


def init():
    with closing(_conn()) as conn, conn:
        conn.execute(
            """CREATE TABLE IF NOT EXISTS strikes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                guild_id INTEGER NOT NULL,
                user_id INTEGER NOT NULL,
                reason TEXT NOT NULL,
                created_at INTEGER NOT NULL
            )"""
        )
        conn.execute(
            """CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                channel_id INTEGER NOT NULL,
                user_id INTEGER NOT NULL,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                created_at INTEGER NOT NULL
            )"""
        )


# chat history (one conversation per user per channel)
def add_message(channel_id, user_id, role, content):
    with closing(_conn()) as conn, conn:
        conn.execute(
            "INSERT INTO messages (channel_id, user_id, role, content, created_at) VALUES (?, ?, ?, ?, ?)",
            (channel_id, user_id, role, content, int(time.time())),
        )


def get_history(channel_id, user_id, limit):
    with closing(_conn()) as conn:
        rows = conn.execute(
            "SELECT role, content FROM messages WHERE channel_id=? AND user_id=? ORDER BY id DESC LIMIT ?",
            (channel_id, user_id, limit),
        ).fetchall()
    rows.reverse()
    return [{"role": r, "content": c} for r, c in rows]


def clear_history(channel_id, user_id):
    with closing(_conn()) as conn, conn:
        conn.execute(
            "DELETE FROM messages WHERE channel_id=? AND user_id=?", (channel_id, user_id)
        )


# moderation strikes
def add_strike(guild_id, user_id, reason):
    with closing(_conn()) as conn, conn:
        conn.execute(
            "INSERT INTO strikes (guild_id, user_id, reason, created_at) VALUES (?, ?, ?, ?)",
            (guild_id, user_id, reason, int(time.time())),
        )
        row = conn.execute(
            "SELECT COUNT(*) FROM strikes WHERE guild_id=? AND user_id=?",
            (guild_id, user_id),
        ).fetchone()
    return row[0]


def get_strikes(guild_id, user_id):
    with closing(_conn()) as conn:
        return conn.execute(
            "SELECT reason, created_at FROM strikes WHERE guild_id=? AND user_id=? ORDER BY id DESC",
            (guild_id, user_id),
        ).fetchall()


def clear_strikes(guild_id, user_id):
    with closing(_conn()) as conn, conn:
        conn.execute(
            "DELETE FROM strikes WHERE guild_id=? AND user_id=?", (guild_id, user_id)
        )
