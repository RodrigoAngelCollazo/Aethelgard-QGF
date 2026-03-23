"""
Security regression tests for Aethelgard-QGF engines.
Focuses on input validation and resource exhaustion prevention.
"""

import unittest

import numpy as np

from aethelgard_engine import AethelgardEngine

try:
    from aethelgard_engine_gpu import AethelgardEngineGPU
    GPU_MODULE_AVAILABLE = True
except ImportError:
    GPU_MODULE_AVAILABLE = False


class TestEngineSecurity(unittest.TestCase):

    def test_engine_init_validation(self):
        """Test validation in AethelgardEngine.__init__."""
        # Valid cases should not raise
        try:
            AethelgardEngine(grid_size=32, domain_size=10.0)
            AethelgardEngine(grid_size=1, domain_size=0.1)
            AethelgardEngine(grid_size=256, domain_size=100.0)
        except ValueError:
            self.fail("AethelgardEngine raised ValueError unexpectedly on valid inputs")

        # Invalid grid_size
        with self.assertRaises(ValueError):
            AethelgardEngine(grid_size=0, domain_size=10.0)
        with self.assertRaises(ValueError):
            AethelgardEngine(grid_size=-10, domain_size=10.0)
        with self.assertRaises(ValueError):
            AethelgardEngine(grid_size=257, domain_size=10.0)  # Too large

        # Invalid domain_size
        with self.assertRaises(ValueError):
            AethelgardEngine(grid_size=32, domain_size=0.0)
        with self.assertRaises(ValueError):
            AethelgardEngine(grid_size=32, domain_size=-5.0)

    def test_engine_solve_validation(self):
        """Test validation in AethelgardEngine.solve_field_equations."""
        engine = AethelgardEngine(grid_size=16, domain_size=5.0)

        # Create valid inputs
        valid_mass = np.zeros((16, 16, 16))
        valid_entropy = np.zeros((16, 16, 16))

        # Valid call
        try:
            engine.solve_field_equations(valid_mass, valid_entropy, iterations=10)
        except ValueError:
            self.fail("solve_field_equations raised ValueError unexpectedly")

        # Invalid iterations
        with self.assertRaises(ValueError):
            engine.solve_field_equations(valid_mass, valid_entropy, iterations=0)
        with self.assertRaises(ValueError):
            engine.solve_field_equations(valid_mass, valid_entropy, iterations=-5)
        with self.assertRaises(ValueError):
            engine.solve_field_equations(valid_mass, valid_entropy, iterations=10001) # Too many

        # Mismatched array shapes
        wrong_shape = np.zeros((15, 16, 16))
        with self.assertRaises(ValueError):
            engine.solve_field_equations(wrong_shape, valid_entropy, iterations=10)
        with self.assertRaises(ValueError):
            engine.solve_field_equations(valid_mass, wrong_shape, iterations=10)


class TestGPUEngineSecurity(unittest.TestCase):

    def setUp(self):
        if not GPU_MODULE_AVAILABLE:
            self.skipTest("GPU module not available")

    def test_gpu_engine_init_validation(self):
        """Test validation in AethelgardEngineGPU.__init__."""
        # Valid cases
        try:
            AethelgardEngineGPU(grid_size=32, domain_size=10.0, use_gpu=False)
        except ValueError:
            self.fail("AethelgardEngineGPU raised ValueError unexpectedly")

        # Invalid grid_size
        with self.assertRaises(ValueError):
            AethelgardEngineGPU(grid_size=0, domain_size=10.0, use_gpu=False)
        with self.assertRaises(ValueError):
            AethelgardEngineGPU(grid_size=257, domain_size=10.0, use_gpu=False)

        # Invalid domain_size
        with self.assertRaises(ValueError):
            AethelgardEngineGPU(grid_size=32, domain_size=0.0, use_gpu=False)
        with self.assertRaises(ValueError):
            AethelgardEngineGPU(grid_size=32, domain_size=-5.0, use_gpu=False)

    def test_gpu_engine_solve_validation(self):
        """Test validation in AethelgardEngineGPU.solve_field_equations."""
        engine = AethelgardEngineGPU(grid_size=16, domain_size=5.0, use_gpu=False)

        valid_mass = np.zeros((16, 16, 16))
        valid_entropy = np.zeros((16, 16, 16))

        # Valid call
        try:
            engine.solve_field_equations(valid_mass, valid_entropy, iterations=10)
        except ValueError:
            self.fail("solve_field_equations raised ValueError unexpectedly")

        # Invalid iterations
        with self.assertRaises(ValueError):
            engine.solve_field_equations(valid_mass, valid_entropy, iterations=0)
        with self.assertRaises(ValueError):
            engine.solve_field_equations(valid_mass, valid_entropy, iterations=10001)

        # Mismatched array shapes
        wrong_shape = np.zeros((15, 16, 16))
        with self.assertRaises(ValueError):
            engine.solve_field_equations(wrong_shape, valid_entropy, iterations=10)


if __name__ == '__main__':
    unittest.main()
