import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
# Need to install hashing package via using: pip install werkzeug or python -m pip install werkzeug
# Then to run it do: python account_logic.py

DB_NAME = "account_db.sqlite"


def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def init_account_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            first_name TEXT,
            last_name TEXT
        )
    """)

    conn.commit()
    conn.close()


def register_user(username, password, first_name="", last_name=""):
    if not username or not password:
        return False, "Username and password are required."

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT user_id FROM users WHERE username = ?", (username,))
    existing_user = cursor.fetchone()

    if existing_user is not None:
        conn.close()
        return False, "Username already exists."

    hashed_password = generate_password_hash(password)

    cursor.execute("""
        INSERT INTO users (username, password_hash, first_name, last_name)
        VALUES (?, ?, ?, ?)
    """, (username, hashed_password, first_name, last_name))

    conn.commit()
    conn.close()

    return True, "User registered successfully."


def login_user(username, password):
    if not username or not password:
        return False, "Username and password are required."

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT user_id, username, password_hash, first_name, last_name
        FROM users
        WHERE username = ?
    """, (username,))
    user = cursor.fetchone()

    conn.close()

    if user is None:
        return False, "User not found."

    if check_password_hash(user["password_hash"], password):
        return True, f"Login successful. Welcome, {user['username']}."

    return False, "Invalid password."


def get_all_users():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT user_id, username, first_name, last_name
        FROM users
        ORDER BY user_id
    """)
    users = cursor.fetchall()

    conn.close()
    return users


if __name__ == "__main__":
    init_account_db()

    print("=== Create New User ===")
    username = input("Enter username: ")
    password = input("Enter password: ")
    first_name = input("Enter first name: ")
    last_name = input("Enter last name: ")

    success, message = register_user(username, password, first_name, last_name)
    print(message)

    print("\n=== Login Test ===")
    login_user_input = input("Enter username to login: ")
    login_pass_input = input("Enter password: ")

    success, message = login_user(login_user_input, login_pass_input)
    print(message)

    print("\nAll users:")
    for user in get_all_users():
        print(dict(user))