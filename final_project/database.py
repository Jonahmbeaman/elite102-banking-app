import sqlite3

DB_NAME = 'stocks.db'

def get_connection():
    return sqlite3.connect(DB_NAME)

def initialize_database():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            balance REAL DEFAULT 0
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS stocks (
            symbol TEXT PRIMARY KEY,
            name TEXT UNIQUE NOT NULL,
            price REAL NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS holdings (
            id INTEGER PRIMARY KEY,
            user_id INTEGER NOT NULL,
            symbol TEXT NOT NULL,
            shares INTEGER NOT NULL,
            purchase_price REAL NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS price_history (
            id INTEGER PRIMARY KEY,
            symbol TEXT NOT NULL,
            price REAL NOT NULL,
            tick INTEGER NOT NULL
        )
    ''')

    seed_stocks_if_empty(cursor)

    conn.commit()
    conn.close()

def seed_stocks_if_empty(cursor):
    cursor.execute("SELECT COUNT(*) FROM stocks")
    count = cursor.fetchone()[0]

    if count == 0:
        starter_stocks = [
            ('AAPL', 'Apple Inc.', 175.00),
            ('GOOG', 'Alphabet', 142.00),
            ('TSLA', 'Tesla', 245.00),
            ('MSFT', 'Microsoft', 380.00),
            ('AMZN', 'Amazon', 155.00),
            ('NVDA', 'NVIDIA', 480.00),
            ('META', 'Meta Platforms', 350.00),
            ('NFLX', 'Netflix', 460.00),
            ('AMD', 'Advanced Micro Devices', 130.00),
            ('DIS', 'Walt Disney Co.', 95.00),
        ]
        cursor.executemany(
            "INSERT INTO stocks (symbol, name, price) VALUES (?, ?, ?)",
            starter_stocks
        )
