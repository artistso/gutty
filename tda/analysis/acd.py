import math
from typing import Dict, Any, List

def simulate_cognitive_distortion(objective_value: float, ego_level: float) -> Dict[str, Any]:
    distortion_factor = 1.0 + (ego_level / 100.0) * 0.5
    perceived_value = objective_value * distortion_factor
    return {
        "objective_value": round(objective_value, 4),
        "perceived_value": round(perceived_value, 4),
        "distortion_factor": round(distortion_factor, 4),
        "ego_level": ego_level,
        "subjectivity_gap": round(perceived_value - objective_value, 4)
    }

def analyze_golden_dangle_sensitivity(ego_spectrum: List[float] = None) -> Dict[str, Any]:
    if ego_spectrum is None:
        ego_spectrum = [0.0, 25.0, 50.0, 75.0, 100.0]
    
    results = []
    for ego in ego_spectrum:
        best_angle = 1.0
        best_ratio = 0.0
        for angle in range(1, 46):
            rad = math.radians(angle)
            y_reach = 2.0 * math.cos(rad)
            k_theta = 0.4 * (angle / 90.0)**1.5
            head_loss = k_theta * (25.0 / (2 * 9.81))
            distorted_reach = y_reach * (1.0 + (ego / 100.0) * 0.5)
            distorted_loss = head_loss * (1.0 + (ego / 100.0) * 0.3)
            ratio = distorted_reach / distorted_loss if distorted_loss > 0 else 0
            if ratio > best_ratio:
                best_ratio = ratio
                best_angle = angle
        results.append({
            "ego_level": ego,
            "optimal_angle_deg": best_angle,
            "perceived_efficiency": round(best_ratio, 2)
        })
    
    return {
        "analysis": "golden_dangle_sensitivity",
        "results": results,
        "model": "acd_distorted_optimization"
    }
