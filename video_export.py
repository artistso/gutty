#!/usr/bin/env python3
"""
Video Export Tool for Subjective Measurement Framework (SMF) v2.0.0
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.animation import FuncAnimation
import sys
sys.path.insert(0, '.')

from tda.simulations.physics import run_robotics_simulation, run_fluid_dynamics
from tda.analysis.acd import analyze_golden_dangle_sensitivity

def export_robotics_gait_video(filename="robotics_gait.gif", fps=15, duration=3.0):
    print(f"Exporting Robotics Gait Video → {filename}")
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.set_xlim(-3, 3)
    ax.set_ylim(-4, 1)
    ax.set_aspect('equal')
    ax.grid(True, alpha=0.3)
    ax.set_title("DARPA Bipedal Gait Animation")
    ax.set_xlabel("X Position (m)")
    ax.set_ylabel("Y Position (m)")
    
    line, = ax.plot([], [], 'o-', color='cyan', linewidth=4, markersize=10)
    com_point, = ax.plot([], [], 'o', color='red', markersize=8)
    
    frames = int(fps * duration)
    t = np.linspace(0, 2 * np.pi, frames)
    hip_pitches = 30 + 20 * np.sin(t)
    knee_pitches = -60 + 30 * np.cos(t)
    
    def init():
        line.set_data([], [])
        com_point.set_data([], [])
        return line, com_point
    
    def animate(i):
        result = run_robotics_simulation(1.5, 1.5, hip_pitches[i], knee_pitches[i])
        x = [0, 1.5 * np.sin(np.radians(hip_pitches[i])), 
             1.5 * np.sin(np.radians(hip_pitches[i])) + 1.5 * np.sin(np.radians(hip_pitches[i] + knee_pitches[i]))]
        y = [0, -1.5 * np.cos(np.radians(hip_pitches[i])), 
             -1.5 * np.cos(np.radians(hip_pitches[i])) - 1.5 * np.cos(np.radians(hip_pitches[i] + knee_pitches[i]))]
        line.set_data(x, y)
        com_point.set_data([np.mean(x)], [np.mean(y)])
        return line, com_point
    
    ani = FuncAnimation(fig, animate, init_func=init, frames=frames, interval=1000/fps, blit=True)
    ani.save(filename, writer='pillow', fps=fps)
    plt.close()
    print(f"  → Saved: {filename}")
    return filename

def export_fluid_head_loss_video(filename="fluid_head_loss.gif", fps=10, duration=4.0):
    print(f"Exporting Fluid Head Loss Video → {filename}")
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.set_xlim(0, 20)
    ax.set_ylim(0, 8)
    ax.set_xlabel("Velocity (m/s)")
    ax.set_ylabel("Head Loss (m)")
    ax.set_title("Fluid Head Loss vs Velocity (45° Bend)")
    ax.grid(True, alpha=0.3)
    
    line, = ax.plot([], [], color='magenta', linewidth=3)
    velocities = np.linspace(0.5, 20, 80)
    losses = [run_fluid_dynamics(45, v)["head_loss_m"] for v in velocities]
    frames = int(fps * duration)
    
    def animate(i):
        line.set_data(velocities[:i+1], losses[:i+1])
        return line,
    
    ani = FuncAnimation(fig, animate, frames=frames, interval=1000/fps, blit=True)
    ani.save(filename, writer='pillow', fps=fps)
    plt.close()
    print(f"  → Saved: {filename}")
    return filename

def export_acd_sensitivity_video(filename="acd_sensitivity.gif", fps=8, duration=5.0):
    print(f"Exporting ACD Sensitivity Video → {filename}")
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    
    ego_levels = np.linspace(0, 100, 50)
    result = analyze_golden_dangle_sensitivity(ego_spectrum=ego_levels.tolist())
    optimal_angles = [r["optimal_angle_deg"] for r in result["results"]]
    efficiencies = [r["perceived_efficiency"] for r in result["results"]]
    
    line1, = ax1.plot([], [], 'o-', color='gold', linewidth=2, markersize=6)
    line2, = ax2.plot([], [], 'o-', color='cyan', linewidth=2, markersize=6)
    
    ax1.set_xlim(0, 100)
    ax1.set_ylim(0, 50)
    ax1.set_xlabel("Ego Level (%)")
    ax1.set_ylabel("Optimal Angle (°)")
    ax1.set_title("Golden Dangle Drift")
    ax1.grid(True, alpha=0.3)
    
    ax2.set_xlim(0, 100)
    ax2.set_ylim(0, max(efficiencies) * 1.1)
    ax2.set_xlabel("Ego Level (%)")
    ax2.set_ylabel("Efficiency Ratio")
    ax2.set_title("Perceived Efficiency")
    ax2.grid(True, alpha=0.3)
    
    frames = int(fps * duration)
    
    def animate(i):
        line1.set_data(ego_levels[:i+1], optimal_angles[:i+1])
        line2.set_data(ego_levels[:i+1], efficiencies[:i+1])
        return line1, line2
    
    ani = FuncAnimation(fig, animate, frames=frames, interval=1000/fps, blit=True)
    ani.save(filename, writer='pillow', fps=fps)
    plt.close()
    print(f"  → Saved: {filename}")
    return filename

if __name__ == "__main__":
    print("\n" + "="*70)
    print("SUBJECTIVE MEASUREMENT FRAMEWORK — VIDEO EXPORT TOOL")
    print("="*70 + "\n")
    
    export_robotics_gait_video("robotics_gait.gif")
    export_fluid_head_loss_video("fluid_head_loss.gif")
    export_acd_sensitivity_video("acd_sensitivity.gif")
    
    print("\n" + "="*70)
    print("✓ All videos exported successfully!")
    print("="*70 + "\n")
