import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

# Database file located in the project root
DATABASE_PATH = 'spendly.db'

def get_db():
    """
    Returns a SQLite connection with foreign keys enabled
    and row_factory set to sqlite3.Row for name-based column access.
    """
    conn = sqlite3.connect(DATABASE_PATH)
    # Enable row factory to return rows as dict-like objects
    conn.row_factory = sqlite3.Row
    # Enforce foreign key constraints
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def create_user(name, email, password):
    """
    Creates a new user in the database.
    """
    hashed_password = generate_password_hash(password)
    conn = get_db()
    try:
        with conn:
            conn.execute(
                "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
                (name, email, hashed_password)
            )
    finally:
        conn.close()


def verify_user(email, password):
    """
    Verifies user credentials and returns the user row if successful.
    """
    conn = get_db()
    try:
        user = conn.execute(
            "SELECT id, password_hash FROM users WHERE email = ?",
            (email,)
        ).fetchone()

        if user and check_password_hash(user['password_hash'], password):
            return user
    finally:
        conn.close()
    return None


def get_user_by_id(user_id):
    """
    Retrieves user details by their ID.
    """
    conn = get_db()
    try:
        user = conn.execute(
            "SELECT id, name, email, created_at FROM users WHERE id = ?",
            (user_id,)
        ).fetchone()
        return user
    finally:
        conn.close()


def init_db():
    """
    Initializes the database by creating the users and expenses tables.
    """
    conn = get_db()
    try:
        with conn:
            # Create users table
            conn.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Create expenses table
            conn.execute("""
                CREATE TABLE IF NOT EXISTS expenses (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    amount REAL NOT NULL,
                    category TEXT NOT NULL,
                    date TEXT NOT NULL,
                    description TEXT,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            """)
    finally:
        conn.close()

def seed_db():
    """
    Populates the database with dummy records for development and testing.
    """
    conn = get_db()
    try:
        with conn:
            # 1. Check if users table already contains data to avoid duplication
            cursor = conn.execute("SELECT 1 FROM users LIMIT 1")
            if cursor.fetchone():
                return

            # 2. Seed Demo User
            hashed_password = generate_password_hash("demo123")
            cursor = conn.execute(
                "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
                ("Demo User", "demo@spendly.com", hashed_password)
            )
            user_id = cursor.lastrowid

            # 3. Seed 8 Demo Expenses
            # Fixed categories: Food, Transport, Bills, Health, Entertainment, Shopping, Other
            expenses = [
                (user_id, 15.50, 'Food', '2026-09-01', 'Lunch at Cafe'),
                (user_id, 5.00, 'Transport', '2026-09-01', 'Bus fare'),
                (user_id, 120.00, 'Bills', '2026-09-02', 'Internet bill'),
                (user_id, 45.00, 'Health', '2026-09-02', 'Pharmacy'),
                (user_id, 12.00, 'Entertainment', '2026-09-03', 'Cinema ticket'),
                (user_id, 60.00, 'Shopping', '2026-09-03', 'New shirt'),
                (user_id, 20.00, 'Other', '2026-09-04', 'Gift wrap'),
                (user_id, 10.00, 'Food', '2026-09-04', 'Snacks'),
            ]
            conn.executemany(
                "INSERT INTO expenses (user_id, amount, category, date, description) VALUES (?, ?, ?, ?, ?)",
                expenses
            )
    finally:
        conn.close()
