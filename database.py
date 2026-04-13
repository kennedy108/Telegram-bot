import sqlite3

# DATABASE MODULE
# Handles all database operations for storing
# and retrieving Telegram users

# Initilaizes a database and creates the user table
# if it does not exists
def init_db():
    connect = sqlite3.connect("users.db")
    cur = connect.cursor()
    cur.execute("""Create table if not exists users(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                chat_id INTEGER UNIQUE,
                username TEXT)""")
    connect.commit()
    connect.close()

# Saves the user to the data base

# @param chat_id the id of the users telegram
# @param username the telegram username
def save_user(chat_id, username):
    connect = sqlite3.connect("users.db")
    cur = connect.cursor()
    cur.execute("Insert or ignore into users (chat_id, username) values (? , ?)",
                (chat_id, username))
    connect.commit()
    connect.close()


# Gets the chat id of the user based off of there username

# @param username the telegram username
# @return the chat id of the user if found, otherwise return none
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


