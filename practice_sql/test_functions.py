import unittest

def add_numbers(a, b):
    """Returns the sum of a and b."""
    return a + b

def is_positive(n):
    """Returns True if n is greater than 0, False otherwise."""
    return n > 0

def find_pokemon(name):
    if name == "Pikachu":
        return "found"
    return None

class TestMyFunctions(unittest.TestCase):

    def test_add_numbers(self):
        self.assertEqual(add_numbers(2, 3), 5)

    def test_add_negative(self):
        self.assertEqual(add_numbers(-1, 1), 0)

    def test_is_positive_true(self):
        self.assertTrue(is_positive(5))

    def test_is_positive_false(self):
        self.assertFalse(is_positive(-3))

    def test_int_raises_value_error(self):
      self.assertRaises(ValueError, int, "abc")
    
    def test_find_pokemon_returns_value(self):
        self.assertIsNotNone(find_pokemon("Pikachu"))

    def test_add_zero(self):
        self.assertEqual(add_numbers(0, 0), 0)

if __name__ == '__main__':
    unittest.main()