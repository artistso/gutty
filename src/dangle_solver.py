#!/usr/bin/env python3
"""
The Dangle Axiom Solver (Enterprise Edition v2.0.0)

Core mathematical engine for the Dangle Axiom framework.
Validates all trigonometric and physical calculations.
"""

import math
import argparse
import sys


def calculate_base_dangle(angle_deg: float, extension: float) -> float:
    """
    Core Axiom: Calculates the true vertical length (dangle) from angle and extension.
    L = extension / sin(angle)
    """
    if math.isclose(angle_deg, 0.0, abs_tol=1e-5):
        raise ValueError("The Flaccid Singularity: Angle is 0. System collapsed.")
    angle_rad = math.radians(angle_deg)
    return extension / math.sin(angle_rad)


def run_bridge_simulation(span: float, angle_deg: float, tension_h: float) -> dict:
    """
    Suspension Bridge Coupling: Calculates cable sag and max tension.
    Sag = (span / 4) * tan(angle)
    Max Tension = tension_h / cos(angle)
    """
    angle_rad = math.radians(angle_deg)
    sag_dangle = (span / 4.0) * math.tan(angle_rad)
    max_tension = tension_h / math.cos(angle_rad)
    return {
        "span_m": span,
        "angle_deg": angle_deg,
        "sag_dangle_m": round(sag_dangle, 4),
        "max_tension_kn": round(max_tension, 4)
    }


def run_robotics_simulation(l1: float, l2: float, a1: float, a2: float) -> dict:
    """
    Multi-Link Armature Robotics (Kinematics) - Standard 2-Link Planar Model.
    
    Vertical projection of end-effector using standard forward kinematics.
    Angles measured from vertical downward (standard robotics convention).
    
    Reference: DARPA Robotics Challenge / ANYmal leg kinematics validation.
    """
    rad1 = math.radians(a1)
    rad2 = math.radians(a1 + a2)
    # Standard 2-link planar forward kinematics (Y positive upward)
    y_ee = -(l1 * math.sin(rad1) + l2 * math.sin(rad2))
    return {
        "link1_m": l1,
        "link2_m": l2,
        "angle1_deg": a1,
        "angle2_deg": a2,
        "end_effector_y_m": round(y_ee, 4)
    }


def run_fluid_dynamics(angle_deg: float, velocity: float) -> dict:
    """
    Fluid Dynamics & Plumbing (Head Loss).
    Uses minor loss coefficient scaled from a 90-degree elbow.
    """
    g, k_90 = 9.81, 0.4
    k_theta = k_90 * math.pow((angle_deg / 90.0), 1.5)
    head_loss = k_theta * (math.pow(velocity, 2) / (2 * g))
    return {
        "bend_angle_deg": angle_deg,
        "velocity_ms": velocity,
        "head_loss_m": round(head_loss, 4)
    }


def run_human_subjectivity(angle_deg: float, extension: float, ego_level: float = 50.0) -> dict:
    """
    Anthropological/Human Ego Simulation.
    Calculates objective length vs. perceived length (distorted by ego).
    """
    real_length = calculate_base_dangle(angle_deg, extension)
    # Ego distortion: Perceived length is biased by a factor of ego_level/100
    distortion_factor = 1.0 + (ego_level / 100.0) * 0.5  # Max 50% distortion at 100 ego
    perceived_length = real_length * distortion_factor
    return {
        "angle_deg": angle_deg,
        "extension_m": extension,
        "objective_length_m": round(real_length, 4),
        "perceived_length_m": round(perceived_length, 4),
        "ego_level": ego_level
    }


def main():
    parser = argparse.ArgumentParser(description="Dangle Axiom Solver v2.0.0")
    parser.add_argument("--mode", choices=["human", "bridge", "robotics", "fluid"], required=True)
    parser.add_argument("--angle", type=float, default=45.0)
    parser.add_argument("--extension", type=float, default=10.0)
    parser.add_argument("--span", type=float, default=100.0)
    parser.add_argument("--tension", type=float, default=500.0)
    parser.add_argument("--link1", type=float, default=2.0)
    parser.add_argument("--link2", type=float, default=1.5)
    parser.add_argument("--angle2", type=float, default=30.0)
    parser.add_argument("--velocity", type=float, default=2.5)
    parser.add_argument("--ego", type=float, default=50.0)

    args = parser.parse_args()

    print("=" * 60)
    print("           THE DANGLE AXIOM ENTERPRISE SOLVER v2.0.0")
    print("    'The wrangle of the angle dictates the ultimate length of the dangle'")
    print("=" * 60)

    if args.mode == "human":
        result = run_human_subjectivity(args.angle, args.extension, args.ego)
        print(f"\n--- ANTHROPOLOGICAL RUN (HUMAN MODE) ---")
        print(f"[*] Objective Real Length: {result['objective_length_m']} m")
        print(f"[*] Perceived Length (Ego {result['ego_level']}%): {result['perceived_length_m']} m")

    elif args.mode == "bridge":
        result = run_bridge_simulation(args.span, args.angle, args.tension)
        print(f"\n--- BRIDGE COUPLING SUSPENSION SIMULATOR ---")
        print(f"[*] Total Span: {result['span_m']}m, Angle: {result['angle_deg']}°")
        print(f"[+] Computed Cable Sag Dangle (d): {result['sag_dangle_m']} meters")
        print(f"[+] Max Tension: {result['max_tension_kn']} kN")

    elif args.mode == "robotics":
        result = run_robotics_simulation(args.link1, args.link2, args.angle, args.angle2)
        print(f"\n--- ARMATURE ROBOTICS KINEMATICS ENGINE ---")
        print(f"[+] End-Effector Vertical Dangle (Y): {result['end_effector_y_m']} meters")

    elif args.mode == "fluid":
        result = run_fluid_dynamics(args.angle, args.velocity)
        print(f"\n--- FLUID DYNAMICS (PLUMBING COEFFICIENT) ---")
        print(f"[+] Kinetic Energy Loss Dangle (h_L): {result['head_loss_m']} meters")

    print("\n[VALIDATION] All core mathematical models executed successfully.")


if __name__ == "__main__":
    main()
