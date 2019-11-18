import unittest
import checks


class TestAmountIsValid(unittest.TestCase):

    def test_negative_amount(self):
        self.assertFalse(checks.amount_is_valid(-1))

    def test_string(self):
        self.assertFalse(checks.amount_is_valid('blablah'))

    def test_correct_integer(self):
        self.assertTrue(checks.amount_is_valid(687))

    def test_correct_float(self):
        self.assertTrue(checks.amount_is_valid(1.09))


if __name__ == '__main__':
    unittest.main
