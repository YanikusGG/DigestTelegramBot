import sqlite3
from config import DEFAULT_POSTS_LIMIT, DEFAULT_PERIOD

DB = None


def connect_db():
    global DB
    DB = sqlite3.connect('users.db')


def init_db():
    global DB
    if DB is not None:
        return
    connect_db()
    DB.cursor().execute("""CREATE TABLE IF NOT EXISTS users (
                   user_id INTEGER PRIMARY KEY,
                   channels TEXT,
                   posts_limit INTEGER,
                   posts_period INTEGER
                   );""")
    DB.commit()


def close_db():
    global DB
    if DB is not None:
        DB.close()
        DB = None


def row_exists(user_id: int):
    global DB
    cursor = DB.cursor()
    info = cursor.execute("SELECT * FROM users WHERE user_id=?", (user_id, )).fetchone()
    if info is None or len(info) == 0:
        return False
    else:
        return info


def add_row(user_id: int, channels: str, posts_limit: int, posts_period: int):
    global DB
    cursor = DB.cursor()
    info = cursor.execute("INSERT INTO users (user_id, channels, posts_limit, posts_period) "
                          "VALUES (?, ?, ?, ?)",
                          (user_id, channels, posts_limit, posts_period)).fetchone()
    DB.commit()


def remove_row(user_id: int):
    global DB
    cursor = DB.cursor()
    info = cursor.execute("DELETE FROM users "
                          "WHERE user_id=?",
                          (user_id, )).fetchone()
    DB.commit()


def get_row(user_id: int):
    global DB
    row = row_exists(user_id)
    if not row_exists(user_id):
        add_row(user_id, '', DEFAULT_POSTS_LIMIT, DEFAULT_PERIOD.total_seconds())
        row = row_exists(user_id)
    return row


def update_channels(user_id: int, channels: str):
    posts_limit = DEFAULT_POSTS_LIMIT
    period = DEFAULT_PERIOD.total_seconds()
    row = row_exists(user_id)
    if row:
        posts_limit = row[2]
        period = row[3]
        remove_row(user_id)

    add_row(user_id, channels, posts_limit, period)


def update_period(user_id: int, period: int):
    channels = ''
    posts_limit = DEFAULT_POSTS_LIMIT
    row = row_exists(user_id)
    if row:
        channels = row[1]
        posts_limit = row[2]
        remove_row(user_id)

    add_row(user_id, channels, posts_limit, period)


def update_posts_limit(user_id: int, posts_limit: int):
    channels = ''
    period = DEFAULT_PERIOD.total_seconds()
    row = row_exists(user_id)
    if row:
        channels = row[1]
        period = row[3]
        remove_row(user_id)

    add_row(user_id, channels, posts_limit, period)
