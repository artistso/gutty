#!/usr/bin/env python3
"""
Golden Dangle Dashboard — Advanced Interactive Analysis
Subjective Measurement Framework (SMF) v2.0.0
"""
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import ipywidgets as widgets
from IPython.display import display
import sys
import math
sys.path.insert(0, '.')

from tda.simulations.physics import run_robotics_simulation, run_fluid_dynamics, run_bridge_simulation
from tda.analysis.acd import analyze_golden_dangle_sensitivity, simulate_cognitive_distortion

def compute_golden_dangle_metrics(ego_level):
    robotics_y = abs(run_robotics_simulation(1.5, 1.5, 30, -60)["end_effector_y_m"])
    fluid_loss = run_fluid_dynamics(45, 5.0)["head_loss_m"]
    bridge_sag = run_bridge_simulation(200, 20, 1000)["sag_dangle_m"]
    acd = simulate_cognitive_distortion(1.0, ego_level)
    result = analyze_golden_dangle_sensitivity(ego_spectrum=[ego_level])
    optimal_angle = result["results"][0]["optimal_angle_deg"]
    efficiency = result["results"][0]["perceived_efficiency"]
    
    return {
        "ego_level": ego_level,
        "robotics_reach_m": round(robotics_y, 3),
        "fluid_loss_m": round(fluid_loss, 3),
        "bridge_sag_m": round(bridge_sag, 3),
        "acd_distortion_factor": acd["distortion_factor"],
        "optimal_angle_deg": optimal_angle,
        "perceived_efficiency": efficiency
    }

def create_golden_dangle_dashboard():
    print("Building Golden Dangle Dashboard...")
    initial_ego = 50.0
    data = compute_golden_dangle_metrics(initial_ego)
    
    fig = make_subplots(
        rows=2, cols=3,
        subplot_titles=("Robotics Reach", "Fluid Head Loss", "Bridge Sag",
                       "ACD Distortion", "Golden Dangle Angle", "Perceived Efficiency"),
        specs=[[{"type": "indicator"}, {"type": "indicator"}, {"type": "indicator"}],
               [{"type": "indicator"}, {"type": "indicator"}, {"type": "indicator"}]]
    )
    
    fig.add_trace(go.Indicator(mode="number+delta", value=data["robotics_reach_m"], title={"text": "Robotics Reach (m)"}, delta={'reference': 1.0, 'relative': True}), row=1, col=1)
    fig.add_trace(go.Indicator(mode="number+delta", value=data["fluid_loss_m"], title={"text": "Fluid Loss (m)"}, delta={'reference': 0.5, 'relative': True}), row=1, col=2)
    fig.add_trace(go.Indicator(mode="number+delta", value=data["bridge_sag_m"], title={"text": "Bridge Sag (m)"}, delta={'reference': 20.0, 'relative': True}), row=1, col=3)
    fig.add_trace(go.Indicator(mode="number+delta", value=data["acd_distortion_factor"], title={"text": "ACD Distortion Factor"}, delta={'reference': 1.0, 'relative': True}), row=2, col=1)
    fig.add_trace(go.Indicator(mode="number+delta", value=data["optimal_angle_deg"], title={"text": "Golden Dangle (°)"}, delta={'reference': 15.0, 'relative': True}), row=2, col=2)
    fig.add_trace(go.Indicator(mode="number+delta", value=data["perceived_efficiency"], title={"text": "Efficiency Ratio"}, delta={'reference': 5.0, 'relative': True}), row=2, col=3)
    
    fig.update_layout(title=f"Golden Dangle Dashboard — Ego Level: {initial_ego}%", template="plotly_dark", height=700, showlegend=False)
    
    ego_slider = widgets.FloatSlider(value=initial_ego, min=0.0, max=100.0, step=1.0, description='Ego Level (%)', continuous_update=True, style={'description_width': 'initial'}, layout=widgets.Layout(width='80%'))
    output = widgets.Output()
    
    def update_dashboard(change):
        with output:
            output.clear_output(wait=True)
            new_ego = change['new']
            new_data = compute_golden_dangle_metrics(new_ego)
            fig.data[0].value = new_data["robotics_reach_m"]
            fig.data[1].value = new_data["fluid_loss_m"]
            fig.data[2].value = new_data["bridge_sag_m"]
            fig.data[3].value = new_data["acd_distortion_factor"]
            fig.data[4].value = new_data["optimal_angle_deg"]
            fig.data[5].value = new_data["perceived_efficiency"]
            fig.update_layout(title=f"Golden Dangle Dashboard — Ego Level: {new_ego}%")
            print(f"\n{'='*60}")
            print(f"EGO LEVEL: {new_ego}%")
            print(f"{'='*60}")
            print(f"Robotics Reach:     {new_data['robotics_reach_m']:.3f} m")
            print(f"Fluid Head Loss:    {new_data['fluid_loss_m']:.3f} m")
            print(f"Bridge Sag:         {new_data['bridge_sag_m']:.3f} m")
            print(f"ACD Distortion:     {new_data['acd_distortion_factor']:.3f}x")
            print(f"Golden Dangle:      {new_data['optimal_angle_deg']:.1f}°")
            print(f"Perceived Efficiency: {new_data['perceived_efficiency']:.2f}")
            print(f"{'='*60}\n")
    
    ego_slider.observe(update_dashboard, names='value')
    
    def export_csv(b):
        df = pd.DataFrame([compute_golden_dangle_metrics(ego_slider.value)])
        df.to_csv("golden_dangle_export.csv", index=False)
        print("Exported to golden_dangle_export.csv")
    
    def export_html(b):
        fig.write_html("golden_dangle_dashboard.html")
        print("Exported to golden_dangle_dashboard.html")
    
    export_csv_btn = widgets.Button(description="Export CSV", button_style='success')
    export_html_btn = widgets.Button(description="Export HTML", button_style='info')
    export_csv_btn.on_click(export_csv)
    export_html_btn.on_click(export_html)
    
    controls = widgets.HBox([ego_slider, export_csv_btn, export_html_btn])
    display(widgets.VBox([controls, output]))
    fig.show()
    
    print("\n✓ Golden Dangle Dashboard ready!")
    print("Use the slider to explore ego bias effects in real time.\n")
    return fig

if __name__ == "__main__":
    print("\n" + "="*70)
    print("GOLDEN DANGLE DASHBOARD — ADVANCED INTERACTIVE ANALYSIS")
    print("="*70 + "\n")
    create_golden_dangle_dashboard()
