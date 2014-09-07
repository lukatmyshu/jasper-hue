from hue import hue

import unittest

from unittest import TestCase

class HueTest(TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_isValid(self):
        self.assertTrue(hue.isValid("Turn the light on"))


if __name__ == "__main__":
    unittest.main()
