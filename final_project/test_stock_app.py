import unittest
import os
from auth import hash_password, register_user, login_user
from stocks import get_stock_price, buy_stock, cash_paycheck
from portfolio import get_user_balance
from database import initialize_database, DB_NAME


class TestStockApp(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Run once before all tests — fresh DB."""
        if os.path.exists(DB_NAME):
            os.remove(DB_NAME)
        initialize_database()

    def test_password_hashing_consistent(self):
        """Same input should produce same hash every time."""
        self.assertEqual(hash_password("test123"), hash_password("test123"))

    def test_password_hashing_different_inputs(self):
        """Different inputs should produce different hashes."""
        self.assertNotEqual(hash_password("abc"), hash_password("xyz"))

    def test_login_with_wrong_password_fails(self):
        """Login with bad password returns None."""
        register_user("bob", "correct_pw")
        self.assertIsNone(login_user("bob", "wrong_pw"))

    def test_login_with_correct_password_succeeds(self):
        """Login with right password returns a user_id."""
        register_user("alice", "secret123")
        result = login_user("alice", "secret123")
        self.assertIsNotNone(result)

    def test_buy_with_insufficient_funds_fails(self):
        """Buying without enough money returns False."""
        register_user("broke", "pw")
        user_id = login_user("broke", "pw")
        # User has $0 — can't afford anything
        self.assertFalse(buy_stock(user_id, "AAPL", 10))

    def test_get_stock_price_unknown_returns_none(self):
        """Looking up a fake symbol returns None."""
        self.assertIsNone(get_stock_price("FAKE"))

    def test_get_stock_price_known_returns_value(self):
        """Looking up a real symbol returns a number."""
        price = get_stock_price("AAPL")
        self.assertIsNotNone(price)