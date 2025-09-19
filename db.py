import sqlite3


def fetch_all(path):
    with sqlite3.connect(path) as conn:
        c = conn.cursor()
        c.execute("SELECT name FROM targets")
        return [row[0] for row in c.fetchall()]

def add(path, name):
    with sqlite3.connect(path) as conn:
        c = conn.cursor()
        c.execute("INSERT INTO targets (name) VALUES (?)", (name,))
        conn.commit()
