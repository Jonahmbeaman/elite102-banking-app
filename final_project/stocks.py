import random
from database import get_connection

def get_all_stocks():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT symbol, name, price FROM stocks")
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_stock_price(symbol):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT price FROM stocks WHERE symbol = ?", (symbol))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None

def update_stock_prices():
    conn = get_connection()
    cursor = conn.cursor()

    next_tick = get_current_tick() + 1

    cursor.execute("SELECT symbol, price FROM stocks")
    stocks = cursor.fetchall()

    for symbol, old_price in stocks:
        change_pct = random.uniform(-0.05, 0.05)
        new_price = round(old_price * (1 + change_pct), 2)

        if new_price < 1.00:
            new_price = 1.00

        cursor.execute(
            "UPDATE stocks SET price = ? WHERE symbol = ?",
            (new_price, symbol)
        )
        cursor.execute(
            "INSERT INTO price_history (symbol, price, tick) VALUES (?, ?, ?)",
            (symbol, new_price, next_tick)
        )
        
    conn.commit()
    conn.close()

def get_current_tick():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT MAX(tick) FROM price_history")
    result = cursor.fetchone()
    conn.close()
    return result[0] if result[0] is not None else 0

def cash_paycheck(user_id, amount=1000):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE users SET balance = balance + ? WHERE id = ?",
        (amount, user_id)
    )

    conn.commit()
    conn.close()

    update_stock_prices()


def buy_stock(user_id, symbol, shares):

    price = get_stock_price(symbol)
    if price is None:
        return False

    total_cost = price * shares

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT balance FROM users WHERE id = ?", (user_id,))
    balance = cursor.fetchone()[0]

    if balance < total_cost:
        conn.close()
        return False

    cursor.execute(
        "UPDATE users SET balance = balance - ? WHERE id = ?",
        (total_cost, user_id)
    )

    cursor.execute(
        "SELECT id, shares FROM holdings WHERE user_id = ? AND symbol = ?",
        (user_id, symbol)
    )
    existing = cursor.fetchone()

    if existing:
        cursor.execute(
            "UPDATE holdings SET shares = shares + ? WHERE id = ?",
            (shares, existing[0])
        )
    else:
        cursor.execute(
            "INSERT INTO holdings (user_id, symbol, shares, purchase_price) VALUES (?, ?, ?, ?)",
            (user_id, symbol, shares, price)
        )

    conn.commit()
    conn.close()
    return True



def sell_stock(user_id, symbol, shares):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, shares FROM holdings WHERE user_id = ? AND symbol = ?",
        (user_id, symbol)
    )
    existing = cursor.fetchone()

    if not existing or existing[1] < shares:
        conn.close()
        return False 

    holding_id, current_shares = existing
    price = get_stock_price(symbol)
    profit = price * shares

    cursor.execute(
        "UPDATE users SET balance = balance + ? WHERE id = ?",
        (profit, user_id)
    )

    if current_shares == shares:
        cursor.execute("DELETE FROM holdings WHERE id = ?", (holding_id,))
    else:
        cursor.execute(
            "UPDATE holdings SET shares = shares - ? WHERE id = ?",
            (shares, holding_id)
        )

    conn.commit()
    conn.close()
    return True