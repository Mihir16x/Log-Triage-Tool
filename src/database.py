import sqlite3
from pathlib import Path


DB_PATH = Path("logs.db")


def create_connection():
    return sqlite3.connect(DB_PATH)


def create_table():
    connection = create_connection()

    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            level TEXT NOT NULL,
            service TEXT NOT NULL,
            message TEXT NOT NULL
        )
        """
    )

    connection.commit()
    connection.close()


def insert_logs(logs: list[dict]):
    connection = create_connection()

    rows = [
        (
            log["timestamp"].isoformat(sep=" "),
            log["level"],
            log["service"],
            log["message"],
        )
        for log in logs
    ]

    connection.executemany(
        """
        INSERT INTO logs (
            timestamp,
            level,
            service,
            message
        )
        VALUES (?, ?, ?, ?)
        """,
        rows,
    )

    connection.commit()
    connection.close()


def clear_logs():
    connection = create_connection()
    connection.execute("DELETE FROM logs")
    connection.commit()
    connection.close()


def get_all_logs():
    connection = create_connection()
    connection.row_factory = sqlite3.Row

    rows = connection.execute(
        """
        SELECT *
        FROM logs
        ORDER BY timestamp
        """
    ).fetchall()

    connection.close()

    return [dict(row) for row in rows]