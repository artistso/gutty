"""
Simple validation tests that work with the current package structure.
"""
import unittest
import math
import sys
sys.path.insert(0, '.')

# Direct imports
from tda.simulations.physics import calculate_base_dangle, run_bridge_simulation

class TestValidation(unittest.TestCase):
    def test_core_axiom(self):
        result = calculate_base_dangle(45.0, 10.0)
        self.assertAlmostEqual(result, 14.1421, places=4)
    
    def test_bridge(self):
        result = run_bridge_simulation(100.0, 45.0, 500.0)
        self.assertEqual(result["sag_dangle_m"], 25.0)

if __name__ == '__main__':
    unittest.main()
