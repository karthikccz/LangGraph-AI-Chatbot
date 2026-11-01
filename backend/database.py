
from backend import conn
import sqlite3
# ============================================
# CHAT MANAGEMENT FUNCTIONS
# ============================================

def initialize_chat_titles():
    """
    Create a table to store custom chat names.
    """

    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS chat_titles (
            thread_id TEXT PRIMARY KEY,
            title TEXT NOT NULL
        )
    """)

    conn.commit()


# Create table when backend starts
initialize_chat_titles()


def get_all_chat_titles():

    cursor = conn.cursor()

    cursor.execute("""
        SELECT thread_id, title
        FROM chat_titles
    """)

    rows = cursor.fetchall()

    return {
        thread_id: title
        for thread_id, title in rows
    }


def save_chat_title(thread_id, title):

    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO chat_titles (thread_id, title)
        VALUES (?, ?)

        ON CONFLICT(thread_id)
        DO UPDATE SET title = excluded.title
    """, (str(thread_id), title))

    conn.commit()


def delete_chat(thread_id):

    """
    Permanently delete:
    1. LangGraph checkpoints
    2. Custom chat title
    """

    cursor = conn.cursor()

    # Delete LangGraph checkpoint data

    cursor.execute(
        "DELETE FROM checkpoints WHERE thread_id = ?",
        (str(thread_id),)
    )

    # Some LangGraph SQLite versions also use these tables.
    # Delete related data if tables exist.

    try:
        cursor.execute(
            "DELETE FROM writes WHERE thread_id = ?",
            (str(thread_id),)
        )
    except sqlite3.OperationalError:
        pass


    # Delete chat title

    cursor.execute(
        "DELETE FROM chat_titles WHERE thread_id = ?",
        (str(thread_id),)
    )

    conn.commit()