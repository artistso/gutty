#!/usr/bin/env python3
"""Final validation script for Dangle Axiom v2.0.0"""
import sys
sys.path.insert(0, '.')

from tda.simulations.physics import (
    calculate_base_dangle, run_bridge_simulation, 
    run_robotics_simulation, run_fluid_dynamics, run_human_subjectivity
)
import math

print("\n" + "="*70)
print("DANGLE AXIOM v2.0.0 - FINAL VALIDATION")
print("="*70)

tests = [
    ("Core Axiom (45°)", abs(calculate_base_dangle(45, 10) - 14.1421) < 0.001),
    ("Bridge Sag (100m, 45°)", run_bridge_simulation(100, 45, 500)["sag_dangle_m"] == 25.0),
    ("Robotics Extended", abs(run_robotics_simulation(3, 4, 0, 0)["end_effector_y_m"]) < 0.001),
    ("Fluid (NIST 90°)", abs(run_fluid_dynamics(90, 10)["head_loss_m"] - 2.0387) < 0.001),
    ("ACD Module", run_human_subjectivity(45, 10, 100)["perceived_length_m"] > 
                   run_human_subjectivity(45, 10, 0)["objective_length_m"]),
]

passed = sum(1 for _, p in tests if p)
for name, result in tests:
    print(f"{'✓' if result else '✗'} {name}: {'PASS' if result else 'FAIL'}")

print("\n" + "="*70)
print(f"RESULTS: {passed}/{len(tests)} PASSED")
if passed == len(tests):
    print("✓✓✓ ALL MODELS VALIDATED - READY FOR GITHUB ✓✓✓")
else:
    print("Some tests failed - review required")
print("="*70 + "\n")
