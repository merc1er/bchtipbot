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


class TestUsernameIsValid(unittest.TestCase):

    def test_other_types(self):
        # Only strings will be passed through Telegram API
        # e.g. 1 will be '1'
        pass

    def test_bad_usernames(self):
        self.assertFalse(checks.username_is_valid('baduname'))
        self.assertFalse(checks.username_is_valid('b@dun@me'))
        self.assertFalse(checks.username_is_valid('@123'))
        long_uname = '@iamaveryveryveryveryverylongusername'
        self.assertFalse(checks.username_is_valid(long_uname))

    def test_good_username(self):
        self.assertTrue(checks.username_is_valid('@merc1er'))


if __name__ == '__main__':
    unittest.main()
