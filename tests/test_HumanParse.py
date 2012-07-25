__author__ = 'orf'

import unittest
from Massive.lib import TargetParser
import datetime

# Prefixed with 'I want to [LOOSE/GAIN]'
TEST_TEXT = [
    ("6 pounds in 3 months"),
    ("12 kilograms in the next 6 months"),
    ("1.5 stone in 3 days"),
    ("12 stone and 2 pounds in a month"),
    #("im invalid bro!"),

]


class MyTestCase(unittest.TestCase):

    def setUp(self):
        self.parser = TargetParser.TargetParser()

    def test_something(self):

        for t in TEST_TEXT:
            self.parser.Parse(t)

if __name__ == '__main__':
    unittest.main()
