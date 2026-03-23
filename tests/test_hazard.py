import unittest

from aethelgard_engine import AethelgardEngine


class TestHazard(unittest.TestCase):
    def setUp(self):
        self.engine = AethelgardEngine(grid_size=16, domain_size=5.0)

    def test_calculate_paradox_hazard_exists(self):
        """Test that calculate_paradox_hazard method exists."""
        self.assertTrue(hasattr(self.engine, 'calculate_paradox_hazard'))

    def test_calculate_paradox_hazard_output_range(self):
        """Test that hazard level is between 0 and 1."""
        hazard = self.engine.calculate_paradox_hazard()
        self.assertGreaterEqual(hazard, 0.0)
        self.assertLessEqual(hazard, 1.0)
