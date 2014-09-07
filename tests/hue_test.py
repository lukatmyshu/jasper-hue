from hue import hue
import fudge

import unittest

from unittest import TestCase

class HueTest(TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_isValid(self):
        self.assertTrue(hue.isValid("Turn the kitchen light on"))
        self.assertTrue(hue.isValid("Turn the bedroom lights off"))

    def test_handle(self):
        bridge = fudge.Fake("bridge").provides("get_group").calls(lambda: {"1":{"name":"Bedroom"}})
        bridge.expects("set_group")
        light_action = hue._handle(bridge, "Turn the bedroom lights on")
        group_id = light_action.light_group
        action = light_action.action

        self.assertEqual(group_id, "1")
        self.assertEqual(action, "on")
        fudge.verify()

if __name__ == "__main__":
    unittest.main()
