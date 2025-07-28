import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# -- Simulation Parameters --
SATELLITES = st.slider("Number of Satellites", 1, 10, 6)
MODULES = st.slider("Modules per Satellite", 1, 10, 3)
ASTEROID_DETECTION = st.checkbox("Enable Asteroid Detection", value=True)
ENERGY_SHARING = st.checkbox("Enable Energy Sharing", value=True)

points = 500
theta = np.linspace(0, 2 * np.pi, points)

# -- Energy Function --
def compute_energy(modules, angle_shift):
    base = np.maximum(np.sin(theta + angle_shift), 0) * 100
    return base * modules

# -- Setup plot --
fig, ax = plt.subplots(1, 2, figsize=(10, 5))
plt.subplots_adjust(wspace=0.4)

# Earth + Orbits
ax[0].set_title("Orbit View")
ax[0].set_xlim(-1.5, 1.5)
ax[0].set_ylim(-1.5, 1.5)
ax[0].set_aspect('equal')
ax[0].add_patch(plt.Circle((0, 0), 0.1, color='green', label='Earth'))

colors = plt.cm.viridis(np.linspace(0, 1, SATELLITES))
energy_logs = []
total_energy = np.zeros(points)

for i in range(SATELLITES):
    angle_shift = (2 * np.pi * i) / SATELLITES
    x = np.cos(theta + angle_shift)
    y = np.sin(theta + angle_shift)
    ax[0].plot(x, y, linestyle="--", alpha=0.3)
    sat_pos = (np.cos(angle_shift), np.sin(angle_shift))
    ax[0].plot(*sat_pos, 'o', color=colors[i], label=f'Sat {i+1}')
    ax[0].plot([sat_pos[0], 0], [sat_pos[1], 0], color='red', linewidth=1)

    energy = compute_energy(MODULES, angle_shift)
    total_energy += energy
    energy_logs.append(energy)

# Energy Plot
ax[1].set_title("Solar Energy Collected")
ax[1].set_xlabel("Orbit Angle (radians)")
ax[1].set_ylabel("Energy (W)")
for i, energy in enumerate(energy_logs):
    ax[1].plot(theta, energy, label=f"Sat {i+1}", alpha=0.7)
ax[1].plot(theta, total_energy, color='black', linestyle='--', label="Total", linewidth=2)
ax[1].legend()

# Asteroid Detection
if ASTEROID_DETECTION:
    np.random.seed(42)
    detections = np.random.choice(points, 3, replace=False)
    detection_angles = theta[detections]
    detection_energy = total_energy[detections]
    ax[1].plot(detection_angles, detection_energy, 'rx', markersize=10, label="Asteroids")

# Energy Sharing
if ENERGY_SHARING and SATELLITES > 1:
    for i in range(SATELLITES - 1):
        p1 = (np.cos((2*np.pi*i)/SATELLITES), np.sin((2*np.pi*i)/SATELLITES))
        p2 = (np.cos((2*np.pi*(i+1))/SATELLITES), np.sin((2*np.pi*(i+1))/SATELLITES))
        ax[0].plot([p1[0], p2[0]], [p1[1], p2[1]], color='blue', linestyle=':', alpha=0.5)

st.pyplot(fig)

st.markdown("---")
st.success("✅ Simulation ready! Adjust sliders above to change satellite count, modules, or detection modes.")
st.caption("Built by you, powered by photons 🚀")
