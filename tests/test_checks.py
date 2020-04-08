import unittest
from tipbot import checks
from .samples import *


class TestAmountIsValid(unittest.TestCase):
    def test_negative_amount(self):
        self.assertFalse(checks.amount_is_valid(-1))

    def test_string(self):
        self.assertFalse(checks.amount_is_valid("blablah"))

    def test_correct_integer(self):
        self.assertTrue(checks.amount_is_valid(687))

    def test_correct_float(self):
        self.assertTrue(checks.amount_is_valid(1.09))


class TestUsernameIsValid(unittest.TestCase):
    def test_other_types(self):
        # username_is_valid should never be passed anything other than a string
        self.assertRaises(TypeError, checks.username_is_valid, 12)
        self.assertRaises(TypeError, checks.username_is_valid, 0.1)

    def test_bad_usernames(self):
        self.assertFalse(checks.username_is_valid("baduname"))
        self.assertFalse(checks.username_is_valid("b@dun@me"))
        self.assertFalse(checks.username_is_valid("@123"))
        long_uname = "@iamaveryveryveryveryverylongusername"
        self.assertFalse(checks.username_is_valid(long_uname))

    def test_good_username(self):
        self.assertTrue(checks.username_is_valid("@merc1er"))


class TestCheckAddress(unittest.TestCase):
    def test_correct_address(self):
        self.assertEqual(checks.check_address(UPDATE, ADDRESS), ADDRESS)

    def test_correct_no_prefix(self):
        self.assertEqual(checks.check_address(UPDATE, ADDR_NO_PREFIX), ADDRESS)

    # add tests for incorrect addresses


if __name__ == "__main__":
    unittest.main()
