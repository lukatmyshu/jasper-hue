from hue import hue
import fudge

import unittest

from unittest import TestCase

class HueTest(TestCase):
    def setUp(self):
        fudge.clear_calls()
        fudge.clear_expectations()

    def tearDown(self):
        fudge.clear_calls()

    def test_isValid(self):
        self.assertTrue(hue.isValid("Turn the kitchen light on"))
        self.assertTrue(hue.isValid("Turn the bedroom lights off"))
        self.assertTrue(hue.isValid("turn the bedroom light on"))
        self.assertTrue(hue.isValid("Turn the living room lights on"))

    def test_handle(self):
        bridge = fudge.Fake("bridge").provides("get_group").calls(lambda: {"1":{"name":"Bedroom"}})
        bridge.expects("set_group")
        light_action = hue._handle(bridge, "Turn the bedroom lights on")
        group_id = light_action.light_group
        action = light_action.action

        self.assertEqual(group_id, "1")
        self.assertEqual(action, "on")
        fudge.verify()


    def test_handle_Multiword(self):
        bridge = fudge.Fake("bridge").provides("get_group").calls(lambda: {"1":{"name":"Bedroom"}, "2":{"name":"LivingRoom"}})
        bridge.expects("set_group")
        light_action = hue._handle(bridge, "Turn the living room lights on")
        group_id = light_action.light_group
        action = light_action.action

        self.assertEqual(group_id, "2")
        self.assertEqual(action, "on")
        fudge.verify()

if __name__ == "__main__":
    unittest.main()
