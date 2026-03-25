import httpx
import sqlite3
import time
from datetime import datetime, timezone

DB_PATH = "data/monitor.db"
TARGET = "https://vmaf.contentnetwork.net/"


def init_db():
    con = sqlite3.connect(DB_PATH)
    con.execute("""
        CREATE TABLE IF NOT EXISTS checks (
            id INTEGER PRIMARY KEY,
            timestamp TEXT NOT NULL,
            status_code INTEGER,
            response_ms REAL,
            error TEXT
        )
    """)
    con.commit()
    con.close()


def check():
    try:
        start = time.monotonic()
        r = httpx.get(TARGET, timeout=10)
        elapsed = (time.monotonic() - start) * 1000
        return r.status_code, round(elapsed, 1), None
    except Exception as e:
        return None, None, str(e)


def record(status_code, response_ms, error):
    con = sqlite3.connect(DB_PATH)
    con.execute(
        "INSERT INTO checks (timestamp, status_code, response_ms, error)"
        " VALUES (?, ?, ?, ?)",
        (datetime.now(timezone.utc).isoformat(), status_code, response_ms, error),
    )
    con.commit()
    con.close()


def main():
    init_db()

    while True:
        status_code, response_ms, error = check()

        record(status_code, response_ms, error)

        time.sleep(300)


if __name__ == "__main__":
    main()
