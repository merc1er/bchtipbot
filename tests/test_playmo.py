import unittest
from tipbot import playmo


class TestSession(unittest.TestCase):

    def test_init_session(self):
        keys = playmo.init_session()
        self.assertTrue(isinstance(keys.get("session_id"), int))
        self.assertEqual(len(keys.get("session_key")), 64)
