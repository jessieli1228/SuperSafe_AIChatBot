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
    conn.close()

def hash_password(password):
    salt = os.urandom(16)
    pwdhash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    return pwdhash.hex(), salt.hex()

def verify_password(entered_password, stored_hash, salt):
    salt_bytes = bytes.fromhex(salt)
    entered_pwdhash = hashlib.pbkdf2_hmac('sha256', entered_password.encode('utf-8'), salt_bytes, 100000)
    return entered_pwdhash.hex() == stored_hash
