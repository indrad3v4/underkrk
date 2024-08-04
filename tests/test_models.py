import unittest
from app.models import Rave

class TestRaveModel(unittest.TestCase):

    def setUp(self):
        self.rave = Rave(
            name="UnderKrakow",
            location="Krakow",
            date="2024-08-01",
            style="Ravecore",
            bpm=150,
            soundsystem=["Default Sound System"],
            lineup=["DJ Test"],
            participants=["Participant Test"],
            stages=["Main Stage"]
        )

    def test_initialization(self):
        self.assertEqual(self.rave.name, "UnderKrakow")
        self.assertEqual(self.rave.location, "Krakow")
        self.assertEqual(self.rave.date, "2024-08-01")
        self.assertEqual(self.rave.style, "Ravecore")
        self.assertEqual(self.rave.bpm, 150)
        self.assertEqual(self.rave.soundsystem, ["Default Sound System"])
        self.assertEqual(self.rave.lineup, ["DJ Test"])
        self.assertEqual(self.rave.participants, ["Participant Test"])
        self.assertEqual(self.rave.stages, ["Main Stage"])

    def test_add_soundsystem(self):
        self.rave.add_soundsystem("New Sound System")
        self.assertIn("New Sound System", self.rave.soundsystem)

    def test_add_lineup(self):
        self.rave.add_lineup("New DJ")
        self.assertIn("New DJ", self.rave.lineup)

    def test_add_participant(self):
        self.rave.add_participant("New Participant")
        self.assertIn("New Participant", self.rave.participants)

    def test_update_event(self):
        self.rave.update_event(name="New Name", location="New Location", date="2024-08-02", style="Techno", bpm=160)
        self.assertEqual(self.rave.name, "New Name")
        self.assertEqual(self.rave.location, "New Location")
        self.assertEqual(self.rave.date, "2024-08-02")
        self.assertEqual(self.rave.style, "Techno")
        self.assertEqual(self.rave.bpm, 160)

if __name__ == '__main__':
    unittest.main()
