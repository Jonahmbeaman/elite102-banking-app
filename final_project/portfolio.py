import matplotlib.pyplot as plt
from database import get_connection
from stocks import get_stock_price

def get_user_balance(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT balance FROM users WHERE id = ?", (user_id,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else 0

def get_user_holdings(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT symbol, shares, purchase_price FROM holdings WHERE user_id = ?",
        (user_id,)
    )
    rows = cursor.fetchall()
    conn.close()

    holdings = []
    for symbol, shares, purchase_price in rows:
        current_price = get_stock_price(symbol)
        holdings.append((symbol, shares, purchase_price, current_price))
    return holdings

def calculate_net_worth(user_id):
    balance = get_user_balance(user_id)
    holdings = get_user_holdings(user_id)

    holdings_value = 0
    for symbol, shares, purchase_price, current_price in holdings:
        holdings_value += shares * current_price

    return balance + holdings_value

def show_price_history_chart(symbol):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT tick, price FROM price_history WHERE symbol = ? ORDER BY tick ASC",
        (symbol,)
    )
    rows = cursor.fetchall()
    conn.close()

    if not rows:
        print(f"No price history for {symbol} yet. Cash a paycheck first.")
        return

    ticks = [row[0] for row in rows]
    prices = [row[1] for row in rows]

    plt.plot(ticks, prices, marker='o')
    plt.title(f"{symbol} Price History")
    plt.xlabel("Paycheck #")
    plt.ylabel("Price ($)")
    plt.grid(True)
    plt.show()

def show_portfolio_chart(user_id):
    holdings = get_user_holdings(user_id)

    if not holdings:
        print("You don't own any stocks yet.")
        return

    symbols = [h[0] for h in holdings]
    values = [h[1] * h[3] for h in holdings]

    plt.bar(symbols, values)
    plt.title("Portfolio Value by Stock")
    plt.xlabel("Stock")
    plt.ylabel("Value ($)")
    plt.show()