import sqlite3
import datetime
from contextlib import closing
import logging

DB_NAME = "numismatics_bot.db"

def init_db():
    with closing(sqlite3.connect(DB_NAME)) as conn:
        with conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS posted_articles (
                    url TEXT PRIMARY KEY,
                    title TEXT,
                    posted_date TIMESTAMP,
                    source TEXT
                )
            ''')

def is_duplicate(url: str) -> bool:
    with closing(sqlite3.connect(DB_NAME)) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM posted_articles WHERE url = ?", (url,))
        return cursor.fetchone() is not None

def mark_as_posted(url: str, title: str, source: str):
    with closing(sqlite3.connect(DB_NAME)) as conn:
        with conn:
            conn.execute('''
                INSERT INTO posted_articles (url, title, posted_date, source)
                VALUES (?, ?, ?, ?)
            ''', (url, title, datetime.datetime.now(), source))

def cleanup_old_entries(days=30):
    cutoff_date = datetime.datetime.now() - datetime.timedelta(days=days)
    with closing(sqlite3.connect(DB_NAME)) as conn:
        with conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM posted_articles WHERE posted_date < ?", (cutoff_date,))
            deleted = cursor.rowcount
            logging.info(f"Cleaned up {deleted} old database entries.")
            return deleted

def get_weekly_stats():
    cutoff_date = datetime.datetime.now() - datetime.timedelta(days=7)
    with closing(sqlite3.connect(DB_NAME)) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM posted_articles WHERE posted_date >= ?", (cutoff_date,))
        count = cursor.fetchone()[0]
        
        cursor.execute("SELECT DISTINCT source FROM posted_articles WHERE posted_date >= ?", (cutoff_date,))
        sources = [row[0] for row in cursor.fetchall()]
        
        return count, sources
