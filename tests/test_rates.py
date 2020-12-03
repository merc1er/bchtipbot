import unittest
from tipbot import rates
from .samples import UPDATE


class TestRate(unittest.TestCase):

    def test_get_rate(self):
        rate = rates.get_rate(UPDATE)
        self.assertIs(type(rate), float)
