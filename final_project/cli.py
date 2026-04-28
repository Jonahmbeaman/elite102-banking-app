from database import initialize_database
from auth import register_user, login_user
from stocks import (
    get_all_stocks, cash_paycheck, buy_stock, sell_stock, get_current_tick
)
from portfolio import (
    get_user_balance, get_user_holdings, calculate_net_worth,
    show_price_history_chart, show_portfolio_chart
)

def main():
    initialize_database()

    while True:
        print("\n=== STONKS ===")
        print("1. Login")
        print("2. Register")
        print("3. Exit")
        choice = input(": ").strip()

        if choice == "1":
            user_id = login_screen()
            if user_id:
                main_menu(user_id)
        elif choice == "2":
            register_screen()
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")


def login_screen():
    username = input("Username: ").strip()
    password = input("Password: ").strip()

    user_id = login_user(username, password)
    if user_id:
        print(f"Welcome back, {username}!")
        return user_id
    else:
        print("Invalid credentials.")
        return None
    
def register_screen():
    username = input("Choose a username: ").strip()
    password = input("Choose a password: ").strip()

    if register_user(username, password):
        print(f"Account created! You can now log in.")
    else:
        print("Username already taken.")
    
def main_menu(user_id):
    while True:
        balance = get_user_balance(user_id)
        net_worth = calculate_net_worth(user_id)
        tick = get_current_tick()

        print(f"\n=== Tick: {tick} | Cash: ${balance:,.2f} | Net Worth: ${net_worth:,.2f} ===")
        print("1. Cash paycheck (+$1000 + advance market)")
        print("2. View stock market")
        print("3. Buy stock")
        print("4. Sell stock")
        print("5. View my portfolio")
        print("6. View stock price chart")
        print("7. View portfolio chart")
        print("8. Logout")
        choice = input("> ").strip()

        if choice == "1":
            cash_paycheck(user_id)
            print("Paycheck cashed! Market updated.")
        elif choice == "2":
            view_market()
        elif choice == "3":
            buy_screen(user_id)
        elif choice == "4":
            sell_screen(user_id)
        elif choice == "5":
            view_portfolio(user_id)
        elif choice == "6":
            symbol = input("Symbol: ").strip().upper()
            show_price_history_chart(symbol)
        elif choice == "7":
            show_portfolio_chart(user_id)
        elif choice == "8":
            print("Logged out.")
            break
        else:
            print("Invalid choice.")

def view_market():
    print("\n--- Stock Market ---")
    print(f"{'Symbol':<8}{'Name':<25}{'Price':>10}")
    for symbol, name, price in get_all_stocks():
        print(f"{symbol:<8}{name:<25}${price:>9,.2f}")

def view_portfolio(user_id):
    holdings = get_user_holdings(user_id)
    if not holdings:
        print("You don't own any stocks.")
        return

    print(f"\n--- My Portfolio ---")
    print(f"{'Symbol':<8}{'Shares':>8}{'Bought At':>12}{'Now':>10}{'P/L':>12}")
    for symbol, shares, purchase_price, current_price in holdings:
        pl = (current_price - purchase_price) * shares
        print(f"{symbol:<8}{shares:>8}${purchase_price:>11,.2f}${current_price:>9,.2f}${pl:>11,.2f}")


def buy_screen(user_id):
    symbol = input("Symbol to buy: ").strip().upper()
    try:
        shares = int(input("How many shares? "))
    except ValueError:
        print("Invalid number of shares.")
        return

    if shares <= 0:
        print("Shares must be positive.")
        return

    if buy_stock(user_id, symbol, shares):
        print(f"Bought {shares} shares of {symbol}.")
    else:
        print("Purchase failed (bad symbol or insufficient funds).")


def sell_screen(user_id):
    symbol = input("Symbol to sell: ").strip().upper()
    try:
        shares = int(input("How many shares? "))
    except ValueError:
        print("Invalid number of shares.")
        return

    if shares <= 0:
        print("Shares must be positive.")
        return

    if sell_stock(user_id, symbol, shares):
        print(f"Sold {shares} shares of {symbol}.")
    else:
        print("Sale failed (you may not own enough shares).")


if __name__ == "__main__":
    main()