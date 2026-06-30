from typing import Dict, Any

def simulate_cosmology(distance_mpc: float) -> Dict[str, Any]:
    H0 = 70.0
    recession_velocity = H0 * distance_mpc
    return {
        "distance_mpc": distance_mpc,
        "recession_velocity_kms": recession_velocity,
        "hubble_constant": H0,
        "model": "hubbles_law"
    }
