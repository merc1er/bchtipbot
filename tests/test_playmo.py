import unittest
from tipbot import playmo


class TestSession(unittest.TestCase):

    def test_init_session(self):
        keys = playmo.init_session()
        self.assertTrue(isinstance(keys.get("session_id"), int))
        self.assertEqual(len(keys.get("session_key")), 64)


class TestGameOverview(unittest.TestCase):

    def test_get_game_overview(self):
        info = playmo.get_game_overview(224)
        self.assertEqual(info.get("title"), "Fortnite Mini Battle Royale")
        self.assertEqual(info.get("entrance_fee"), 500)
