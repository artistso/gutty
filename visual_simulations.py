#!/usr/bin/env python3
"""
Visual Simulation Suite for Subjective Measurement Framework (SMF) v2.0.0
"""
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import sys
import math
sys.path.insert(0, '.')

# Import from the correct location
from tda.simulations.physics import run_robotics_simulation, run_fluid_dynamics
from tda.analysis.acd import analyze_golden_dangle_sensitivity

def create_robotics_3d_animation(frames=30):
    print("Generating 3D Robotics Animation...")
    fig = go.Figure()
    t = np.linspace(0, 2 * np.pi, frames)
    hip_pitches = 30 + 20 * np.sin(t)
    knee_pitches = -60 + 30 * np.cos(t)
    
    frame_data = []
    for i in range(frames):
        result = run_robotics_simulation(1.5, 1.5, hip_pitches[i], knee_pitches[i])
        frame_data.append(go.Scatter(
            x=[0, 1.5 * np.sin(np.radians(hip_pitches[i])), 
               1.5 * np.sin(np.radians(hip_pitches[i])) + 1.5 * np.sin(np.radians(hip_pitches[i] + knee_pitches[i]))],
            y=[0, -1.5 * np.cos(np.radians(hip_pitches[i])), 
               -1.5 * np.cos(np.radians(hip_pitches[i])) - 1.5 * np.cos(np.radians(hip_pitches[i] + knee_pitches[i]))],
            mode='lines+markers',
            line=dict(color='cyan', width=8),
            marker=dict(size=12, color='red')
        ))
    
    fig.add_trace(frame_data[0])
    frames_list = [go.Frame(data=[frame_data[i]]) for i in range(frames)]
    fig.frames = frames_list
    
    fig.update_layout(
        title="DARPA Bipedal Gait Animation (3D Kinematics)",
        xaxis=dict(range=[-3, 3], title="X Position (m)"),
        yaxis=dict(range=[-4, 1], title="Y Position (m)"),
        updatemenus=[dict(
            type="buttons",
            showactive=False,
            buttons=[dict(
                label="Play",
                method="animate",
                args=[None, {"frame": {"duration": 100, "redraw": True}, "fromcurrent": True}]
            )]
        )],
        template="plotly_dark",
        height=600
    )
    fig.write_html("robotics_animation.html")
    print("  → Saved: robotics_animation.html")
    return fig

def create_fluid_head_loss_plot():
    print("Generating Fluid Dynamics Visualization...")
    angles = np.linspace(10, 90, 50)
    velocities = np.linspace(1, 20, 50)
    A, V = np.meshgrid(angles, velocities)
    k_90 = 0.4
    k_theta = k_90 * (A / 90) ** 1.5
    head_loss = k_theta * (V ** 2) / (2 * 9.81)
    
    fig = go.Figure(data=[go.Surface(x=A, y=V, z=head_loss, colorscale='Viridis', colorbar=dict(title="Head Loss (m)"))])
    fig.update_layout(
        title="Fluid Head Loss: Angle × Velocity Surface",
        scene=dict(xaxis_title="Bend Angle (°)", yaxis_title="Velocity (m/s)", zaxis_title="Head Loss (m)"),
        template="plotly_dark",
        height=700
    )
    fig.write_html("fluid_head_loss_surface.html")
    print("  → Saved: fluid_head_loss_surface.html")
    return fig

def create_acd_sensitivity_plot():
    print("Generating ACD Sensitivity Analysis...")
    result = analyze_golden_dangle_sensitivity(ego_spectrum=np.linspace(0, 100, 25))
    ego_levels = [r["ego_level"] for r in result["results"]]
    optimal_angles = [r["optimal_angle_deg"] for r in result["results"]]
    efficiencies = [r["perceived_efficiency"] for r in result["results"]]
    
    fig = make_subplots(rows=1, cols=2, subplot_titles=("Golden Dangle Drift", "Perceived Efficiency"))
    fig.add_trace(go.Scatter(x=ego_levels, y=optimal_angles, mode='lines+markers', name="Optimal Angle", line=dict(color='gold', width=3)), row=1, col=1)
    fig.add_trace(go.Scatter(x=ego_levels, y=efficiencies, mode='lines+markers', name="Efficiency", line=dict(color='cyan', width=3)), row=1, col=2)
    fig.update_layout(title="Anthropological Cognitive Distortion (ACD) Sensitivity Analysis", template="plotly_dark", height=500, showlegend=False)
    fig.update_xaxes(title_text="Ego Level (%)", row=1, col=1)
    fig.update_xaxes(title_text="Ego Level (%)", row=1, col=2)
    fig.update_yaxes(title_text="Optimal Angle (°)", row=1, col=1)
    fig.update_yaxes(title_text="Efficiency Ratio", row=1, col=2)
    fig.write_html("acd_sensitivity_analysis.html")
    print("  → Saved: acd_sensitivity_analysis.html")
    return fig

def create_combined_dashboard():
    print("Generating Combined Dashboard...")
    fig = make_subplots(rows=2, cols=2, subplot_titles=("Robotics Reach", "Fluid Head Loss", "ACD Golden Dangle", "Multi-Domain"))
    
    hip_angles = np.linspace(-20, 90, 50)
    reaches = [abs(run_robotics_simulation(1.5, 1.5, hip, -60)["end_effector_y_m"]) for hip in hip_angles]
    fig.add_trace(go.Scatter(x=hip_angles, y=reaches, mode='lines', name="Robotics", line=dict(color='magenta', width=2)), row=1, col=1)
    
    velocities = np.linspace(1, 15, 50)
    losses = [run_fluid_dynamics(45, v)["head_loss_m"] for v in velocities]
    fig.add_trace(go.Scatter(x=velocities, y=losses, mode='lines', name="Fluid", line=dict(color='cyan', width=2)), row=1, col=2)
    
    acd_result = analyze_golden_dangle_sensitivity(ego_spectrum=np.linspace(0, 100, 20))
    ego_levels = [r["ego_level"] for r in acd_result["results"]]
    optimal_angles = [r["optimal_angle_deg"] for r in acd_result["results"]]
    fig.add_trace(go.Scatter(x=ego_levels, y=optimal_angles, mode='lines+markers', name="Golden Dangle", line=dict(color='gold', width=2)), row=2, col=1)
    
    domains = ["Robotics", "Fluid", "Bridge", "Quantum", "Cosmology"]
    baseline = [1.0, 1.0, 1.0, 1.0, 1.0]
    ego_50 = [0.85, 0.92, 0.78, 1.05, 1.0]
    fig.add_trace(go.Bar(x=domains, y=baseline, name="Baseline", marker_color='gray'), row=2, col=2)
    fig.add_trace(go.Bar(x=domains, y=ego_50, name="Ego=50%", marker_color='orange'), row=2, col=2)
    
    fig.update_layout(title="SMF v2.0.0 — Multi-Domain Visual Dashboard", template="plotly_dark", height=800, showlegend=False)
    fig.write_html("smf_dashboard.html")
    print("  → Saved: smf_dashboard.html")
    return fig

if __name__ == "__main__":
    print("\n" + "="*70)
    print("SUBJECTIVE MEASUREMENT FRAMEWORK — VISUAL SIMULATION SUITE")
    print("="*70 + "\n")
    
    create_robotics_3d_animation()
    create_fluid_head_loss_plot()
    create_acd_sensitivity_plot()
    create_combined_dashboard()
    
    print("\n" + "="*70)
    print("✓ All visualizations generated successfully!")
    print("Open the .html files in a browser to view interactive plots.")
    print("="*70 + "\n")
