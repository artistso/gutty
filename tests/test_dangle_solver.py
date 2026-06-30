import unittest
import math
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tda.simulations.physics import (
    calculate_base_dangle,
    run_bridge_simulation,
    run_robotics_simulation,
    run_fluid_dynamics,
    run_human_subjectivity
)

class TestDangleAxiomCore(unittest.TestCase):
    def test_base_dangle_standard(self):
        result = calculate_base_dangle(45.0, 10.0)
        self.assertAlmostEqual(result, 14.1421356237, places=4)

    def test_base_dangle_90_degrees(self):
        result = calculate_base_dangle(90.0, 5.0)
        self.assertEqual(result, 5.0)

    def test_base_dangle_singularity(self):
        with self.assertRaises(ValueError):
            calculate_base_dangle(0.0, 10.0)

    def test_bridge_sag_calculation(self):
        result = run_bridge_simulation(100.0, 45.0, 500.0)
        self.assertEqual(result["sag_dangle_m"], 25.0)
        self.assertAlmostEqual(result["max_tension_kn"], 707.1068, places=3)

    def test_robotics_kinematics(self):
        result = run_robotics_simulation(3.0, 4.0, 0.0, 0.0)
        self.assertAlmostEqual(result["end_effector_y_m"], 0.0, places=4)

    def test_fluid_head_loss(self):
        result = run_fluid_dynamics(90.0, 10.0)
        self.assertAlmostEqual(result["head_loss_m"], 2.0387, places=4)

    def test_human_ego_distortion(self):
        real = run_human_subjectivity(45.0, 10.0, ego_level=0.0)
        ego_high = run_human_subjectivity(45.0, 10.0, ego_level=100.0)
        self.assertEqual(real["objective_length_m"], ego_high["objective_length_m"])
        self.assertGreater(ego_high["perceived_length_m"], real["perceived_length_m"])

if __name__ == '__main__':
    unittest.main()
