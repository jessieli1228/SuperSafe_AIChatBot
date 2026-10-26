import sqlite3
import hashlib
import os

# Using a new filename to force the cloud to create a fresh, clean database
DB_NAME = "users_v2.db"

def hash_password(password):
    salt = os.urandom(16)
    pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'), salt, 100000)
    return pwdhash.hex(), salt.hex()

def verify_password(entered_password, stored_hash, salt):
    try:
        salt_bytes = bytes.fromhex(salt)
        entered_pwdhash = hashlib.pbkdf2_hmac('sha512', entered_password.encode('utf-8'), salt_bytes, 100000)
        return entered_pwdhash.hex() == stored_hash
    except Exception:
        return False

def initialize_db():
    try:
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        
        # 1. Create Users Table
        c.execute('''CREATE TABLE IF NOT EXISTS users 
                     (username TEXT PRIMARY KEY, password_hash TEXT, salt TEXT)''')
        
        # 2. Create Chat History Table
        c.execute('''CREATE TABLE IF NOT EXISTS chat_history 
                     (username TEXT, role TEXT, content TEXT, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
        
        # 3. Create the Admin Account (Demo Insurance)
        admin_user = "admin"
        admin_pass = "Demo-Admin-2026-SuperSafe!"
        
        c.execute("SELECT * FROM users WHERE username=?", (admin_user,))
        if not c.fetchone():
            salt = os.urandom(16)
            pwdhash = hashlib.pbkdf2_hmac('sha512', admin_pass.encode('utf-8'), salt, 100000)
            c.execute("INSERT INTO users VALUES (?, ?, ?)", (admin_user, pwdhash.hex(), salt.hex()))
            
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Database Init Error: {e}")

def save_chat_message(username, role, content):
    try:
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute("INSERT INTO chat_history (username, role, content) VALUES (?, ?, ?)", 
                  (username, role, content))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Save Chat Error: {e}")

def get_chat_history(username):
    try:
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute("SELECT role, content FROM chat_history WHERE username = ? ORDER BY timestamp ASC", 
                  (username,))
        history = c.fetchall()
        conn.close()
        return [{"role": row[0], "content": row[1]} for row in history]
    except Exception:
        return []