import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from unittest.mock import Mock
from app.models import Rave
from app.controllers import RaveController

class TestRaveController(unittest.TestCase):

    def setUp(self):
        self.rave_model = Rave(name="", location="", date="", style="", bpm=0, soundsystem=[], lineup=[], participants=[], stages=["Main Stage"])
        self.client = Mock()
        self.group_chat_id = "group_chat_id"
        self.verification_chat_id = "verification_chat_id"
        self.rave_controller = RaveController(self.rave_model, self.client, self.group_chat_id, self.verification_chat_id)

    def test_create_event(self):
        update = Mock()
        context = Mock()
        self.rave_controller.create_event(update, context)
        self.assertEqual(self.rave_model.name, "Event Name")

    def test_handle_link(self):
        update = Mock()
        context = Mock()
        self.rave_controller.handle_link(update, context)
        self.assertIn("Verification Link", self.rave_model.participants)

    def test_show_soundsystem_elements(self):
        update = Mock()
        context = Mock()
        self.rave_controller.show_soundsystem_elements(update, context)
        self.assertIn("Sound System Element", self.rave_model.soundsystem)

if __name__ == '__main__':
    unittest.main()
