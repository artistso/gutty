import math
from typing import Dict, Any

def simulate_quantum(delta_x: float) -> Dict[str, Any]:
    hbar = 1.054571817e-34
    momentum_uncertainty = hbar / (2 * delta_x)
    return {
        "delta_x_m": delta_x,
        "momentum_uncertainty": momentum_uncertainty,
        "hbar": hbar,
        "model": "heisenberg_uncertainty"
    }

def simulate_subatomic(particle: str, velocity_c: float) -> Dict[str, Any]:
    c = 299792458.0
    rest_masses = {
        "Muon": 1.883531627e-28,
        "Gluon": 0.0,
        "Boson (Higgs)": 2.246e-25,
    }
    if particle not in rest_masses:
        raise ValueError(f"Unsupported particle: {particle}")
    m0 = rest_masses[particle]
    gamma = 1.0 / math.sqrt(1 - velocity_c**2) if velocity_c < 1.0 else float('inf')
    relativistic_mass = m0 * gamma if m0 > 0 else 0.0
    return {
        "particle": particle,
        "velocity_fraction_c": velocity_c,
        "lorentz_factor_gamma": round(gamma, 4) if gamma != float('inf') else "infinite",
        "rest_mass_kg": m0,
        "relativistic_mass_kg": relativistic_mass if relativistic_mass > 0 else "massless",
        "model": "special_relativity"
    }
