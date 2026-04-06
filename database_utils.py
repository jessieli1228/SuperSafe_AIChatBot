import sqlite3
import hashlib
import os

def initialize_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            username TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            salt TEXT NOT NULL
        )
    ''')
    conn.commit()

    c.execute('''
        CREATE TABLE IF NOT EXISTS chat_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            role TEXT NOT NULL,
            content TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(rowid)
        )
    ''')
    conn.commit()
    conn.close()

def get_user_id(username):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('SELECT rowid FROM users WHERE username = ?', (username,))
    user_id = c.fetchone()
    conn.close()
    return user_id[0] if user_id else None

def save_message(user_id, role, content):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('INSERT INTO chat_history (user_id, role, content) VALUES (?, ?, ?)', (user_id, role, content))
    conn.commit()
    conn.close()

def load_messages(user_id):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('SELECT role, content FROM chat_history WHERE user_id = ? ORDER BY rowid', (user_id,))
    messages = [{"role": row[0], "content": row[1]} for row in c.fetchall()]
    conn.close()
    return messages

def hash_password(password):
    salt = os.urandom(16)
    pwdhash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    return pwdhash.hex(), salt.hex()

def verify_password(entered_password, stored_hash, salt):
    salt_bytes = bytes.fromhex(salt)
    entered_pwdhash = hashlib.pbkdf2_hmac('sha256', entered_password.encode('utf-8'), salt_bytes, 100000)
    return entered_pwdhash.hex() == stored_hash

def clear_chat_history(user_id):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('DELETE FROM chat_history WHERE user_id = ?', (user_id,))
    conn.commit()
    conn.close()
