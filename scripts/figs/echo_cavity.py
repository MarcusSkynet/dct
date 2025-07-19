import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# --- Parameters for the Schematic ---
Rs = 1.0  # Schwarzschild radius (normalized to 1 for plotting)
alpha_H = 0.361
R_core = np.sqrt(alpha_H) * Rs  # Approx 0.61 * Rs

# --- Plotting ---
plt.style.use('seaborn-v0_8-whitegrid')
fig, ax = plt.subplots(figsize=(8, 4)) # Wider aspect ratio

# Singularity point (replaced by core)
# ax.plot(0, 0, 'kx', markersize=10, label='Classical Singularity (r=0)\n(Replaced by Ledger Core)')

# Ledger Core
core_circle = patches.Circle((0, 0), R_core, edgecolor='purple', facecolor='lavender', linewidth=2, alpha=0.7, zorder=2)
ax.add_patch(core_circle)
ax.plot([0, R_core * np.cos(np.pi/4)], [0, R_core * np.sin(np.pi/4)], 'purple', linestyle='-', linewidth=1.5)
ax.text(R_core * 0.5 * np.cos(np.pi/2), R_core * 0.6 * np.sin(np.pi/3), '$R_{core}$',
        ha='center', va='center', fontsize=12, color='purple', bbox=dict(facecolor='white', alpha=0.5, pad=0.1))

# Event Horizon
horizon_circle = patches.Circle((0, 0), Rs, edgecolor='black', facecolor='none', linewidth=2, linestyle='--', zorder=1)
ax.add_patch(horizon_circle)
ax.plot([0, Rs * np.cos(-np.pi/6)], [0, Rs * np.sin(-np.pi/6)], 'k--', linewidth=1.5)
ax.text(Rs * 0.8 * np.cos(-np.pi/4), Rs * 0.8 * np.sin(-np.pi/4), '$R_s$',
        ha='center', va='center', fontsize=12, color='black', bbox=dict(facecolor='white', alpha=0.5, pad=0.1))


# Cavity Region (shaded annular region)
# To shade the annulus, we can use a trick with two circles or a wedge
# For simplicity, let's use a thick ring or just denote it with arrows and text
# Or, use a PathPatch for an annulus sector
theta1, theta2 = 45, 135 # Degrees for the sector
cavity_wedge = patches.Wedge(center=(0,0), r=Rs, theta1=theta1, theta2=theta2, width=(Rs-R_core),
                              facecolor='grey', alpha=0.3, zorder=0)
ax.add_patch(cavity_wedge)

# Arrow and text for cavity
cavity_mid_radius = (Rs + R_core) / 2
angle_cavity_text = np.deg2rad(90) # Place text at the top
ax.annotate('Echo Cavity Region\n($R_{core} < r < R_s$)',
            xy=(cavity_mid_radius * np.cos(angle_cavity_text), cavity_mid_radius * np.sin(angle_cavity_text)),
            xytext=(0, Rs * 1.3), # Text position
            ha='center', va='center', fontsize=11, color='dimgray',
            arrowprops=dict(facecolor='dimgray', shrink=0.05, width=1, headwidth=5, connectionstyle="arc3,rad=-0.2"))

# Arrows indicating reflection
# Incoming wave (example)
ax.arrow(Rs * 1.2, Rs * 0.3, - (Rs * 1.2 - R_core*0.9), - (Rs*0.3 - R_core*0.1*np.sin(np.pi/3)), # Simplified direction
         head_width=0.03, head_length=0.05, fc='C0', ec='C0', length_includes_head=True, zorder=3)
# Reflected wave from core
ax.arrow(R_core*0.9, R_core*0.1*np.sin(np.pi/3), (Rs*1.1 - R_core*0.9), (Rs*0.4 - R_core*0.1*np.sin(np.pi/3)),  # Simplified direction
         head_width=0.03, head_length=0.05, fc='C0', ec='C0', linestyle=':', length_includes_head=True, zorder=3)
ax.text(Rs*1.2, Rs*0.5, "Wave reflects\n in cavity", fontsize=9, color='C0', ha='center')


# Setting plot limits and appearance
ax.set_xlim(-Rs * 1.3, Rs * 1.3)
ax.set_ylim(-Rs * 1.1, Rs * 1.5) # Adjusted for text at top
ax.set_aspect('equal', adjustable='box')
ax.axis('off') # Turn off the Cartesian axes for a cleaner schematic

ax.set_title('Schematic of Ledger Core and Echo Cavity (DCT)', fontsize=14, fontweight='bold', pad=20)
plt.show()

# plt.savefig('cavity_schematic.pdf')
# print("Plot 'cavity_schematic.pdf' generated.")