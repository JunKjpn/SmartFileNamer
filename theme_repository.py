import sqlite3


def fetch_all(path):
    with sqlite3.connect(path) as conn:
        c = conn.cursor()
        c.execute("SELECT name FROM themes")
        return [row[0] for row in c.fetchall()]

def add(path, name):
    with sqlite3.connect(path) as conn:
        c = conn.cursor()
        c.execute("INSERT INTO themes (name) VALUES (?)", (name,))
        conn.commit()
