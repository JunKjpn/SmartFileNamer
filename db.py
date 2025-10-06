import sqlite3
from pathlib import Path
import FreeSimpleGUI as sg


def check(path):
    try:
        db_path = Path(path)

        with sqlite3.connect(db_path) as conn:
            c = conn.cursor()
            # 最低限のテーブルを用意
            c.execute("CREATE TABLE IF NOT EXISTS targets (name TEXT)")
        return True

    except sqlite3.OperationalError as e:
        sg.popup_error(f"データベースに接続できませんでした。\n{e}")
        raise SystemExit(1)  # アプリを終了


def fetch_all_targets(path):
    with sqlite3.connect(path) as conn:
        c = conn.cursor()
        c.execute("SELECT name FROM targets")
        return [row[0] for row in c.fetchall()]


def fetch_all_themes(path):
    with sqlite3.connect(path) as conn:
        c = conn.cursor()
        c.execute("SELECT text FROM themes")
        return [row[0] for row in c.fetchall()]

def add_targets(path, name):
    with sqlite3.connect(path) as conn:
        c = conn.cursor()
        c.execute("INSERT INTO targets (name) VALUES (?)", (name,))
        conn.commit()


def add_themes(path, text):
    with sqlite3.connect(path) as conn:
        c = conn.cursor()
        c.execute("SELECT 1 FROM themes WHERE text = ?", (text,))
        if c.fetchone() is None:
            c.execute("INSERT INTO themes (text) VALUES (?)", (text,))
            conn.commit()
            print("登録完了")
