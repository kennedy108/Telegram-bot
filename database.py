import sqlite3

def init_db():
    connect = sqlite3.connect("users.db")
    cur = connect.cursor()
    cur.execute("""Create table if not exists users(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                chat_id INTEGER UNIQUE,
                username TEXT)""")
    connect.commit()
    connect.close()

def save_user(chat_id, username):
    connect = sqlite3.connect("users.db")
    cur = connect.cursor()
    cur.execute("Insert or ignore into users (chat_id, username) values (? , ?)",
                (chat_id, username))
    connect.commit()
    connect.close()

def get_user(username):
    connect = sqlite3.connect("users.db")
    cur = connect.cursor()
    cur.execute("SELECT chat_id FROM users WHERE username = ?", (username,))
    row = cur.fetchone()
    connect.close()
    if row:
        return row[0]
    else:
        return None


