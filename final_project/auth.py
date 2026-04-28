import hashlib
from database import get_connection

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(username, password):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM users WHERE username = ?", (username,))

    if cursor.fetchone():
        conn.close()
        return False
    
    cursor.execute(
        "INSERT INTO users (username, password_hash, balance) VALUES (?, ?, ?)",
        (username, hash_password(password), 0)
    )

    conn.commit()
    conn.close()
    return True

def login_user(username, password):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, password_hash FROM users WHERE username = ?",
        (username,)
    )
    result = cursor.fetchone()
    conn.close()

    if result is None:
        return None  # username doesn't exist

    user_id, stored_hash = result

    if hash_password(password) == stored_hash:
        return user_id
    return None