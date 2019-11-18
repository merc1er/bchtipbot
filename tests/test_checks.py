import unittest
import checks


class TestAmountIsValid(unittest.TestCase):

    def test_negative_amount(self):
        self.assertFalse(checks.amount_is_valid(-1))


if __name__ == '__main__':
    unittest.main()
