import unittest
from dataclasses import FrozenInstanceError
from tyrant.models.government import Government


class TestGovernment(unittest.TestCase):
    def test_immutability(self):
        """Tests that the Government dataclass is frozen and cannot be mutated."""
        government = Government(chancellor_uid=1, president_uid=2)
        with self.assertRaises(FrozenInstanceError):
            government.elected = True
        with self.assertRaises(FrozenInstanceError):
            government.chancellor_uid = 3
        with self.assertRaises(FrozenInstanceError):
            government.president_uid = 4
