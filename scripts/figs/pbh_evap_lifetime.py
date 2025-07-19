import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

# Constants
M_planck_val = 1.0  # Normalized Planck mass for calculation
alpha_H = 0.3607
K_hawking = 1.0 # Proportionality constant for t_evap = K * M^3 # CORRECTED LINE

# --- Mass Ranges ---
# Full range for log-log plot
log_M_min_full_hawking = -1 # Go below M_planck for Hawking curve (e.g., 0.1 M_planck)
log_M_min_full_dct = 0    # DCT remnants start at M_planck
log_M_max_full = 15
masses_hawking_plot = np.logspace(log_M_min_full_hawking, log_M_max_full, 400)
masses_dct_plot = np.logspace(log_M_min_full_dct, log_M_max_full, 400)


# Zoomed-in range for linear plot
M_min_zoom = M_planck_val
M_max_zoom = 100 * M_planck_val # CORRECTED: Use M_planck_val
masses_zoom_plot = np.linspace(M_min_zoom, M_max_zoom, 400)

# --- Evaporation Time Calculations ---
def get_hawking_evap_time(mass_array):
    # Standard Hawking evaporates to zero from any initial mass M
    return K_hawking * (mass_array**3)

def get_dct_evap_time_to_remnant(mass_array):
    # DCT evaporates to M_planck_val remnant
    t_evap_dct = np.zeros_like(mass_array)
    for i, m_pbh in enumerate(mass_array):
        if m_pbh > M_planck_val:
            # Time to evaporate from m_pbh down to M_planck_val
            t_evap_dct[i] = (K_hawking / (1 - alpha_H)) * (m_pbh**3 - M_planck_val**3)
        elif m_pbh == M_planck_val:
            t_evap_dct[i] = 0 # Takes zero time to become a remnant if it starts as one
        else: # m_pbh < M_planck_val
            t_evap_dct[i] = np.nan # Not a classical BH evaporating down to a remnant
    return t_evap_dct

# Calculate for full range
t_hawking_full = get_hawking_evap_time(masses_hawking_plot)
t_dct_full = get_dct_evap_time_to_remnant(masses_dct_plot)

# Calculate for zoom range
t_hawking_zoom = get_hawking_evap_time(masses_zoom_plot)
t_dct_zoom = get_dct_evap_time_to_remnant(masses_zoom_plot)


# --- Plotting ---
plt.style.use('seaborn-v0_8-whitegrid')
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6)) # Two plots horizontally

# --- Plot 1: Full Log-Log Scale ---
ax1.loglog(masses_hawking_plot, t_hawking_full,
           label='Standard Hawking Evaporation (to M=0)', color='C0', linestyle='-', linewidth=2)
# Filter NaNs for DCT plot which starts at M_planck_val
valid_dct_full = ~np.isnan(t_dct_full)
ax1.loglog(masses_dct_plot[valid_dct_full], t_dct_full[valid_dct_full],
           label=f'DCT ($\\alpha_H={alpha_H}$)\n(Evaporates to $M_P$ remnant)', color='C3', linestyle='--', linewidth=2)

ax1.set_xlabel('Initial PBH Mass ($M_{PBH}$ / $M_{Planck}$)', fontsize=11)
ax1.set_ylabel('Evaporation Lifetime ($t_{evap}$ / $t_{P,evap}$)', fontsize=11)
ax1.set_title('PBH Evaporation Lifetime (Full Scale)', fontsize=13, fontweight='bold')
ax1.axvline(M_planck_val, color='gray', linestyle=':', linewidth=1.5, label='$M_P$ (Remnant Mass Scale)')
ax1.legend(fontsize=9)
ax1.grid(True, which="both", ls="-", alpha=0.7)
# Ensure y-axis starts appropriately for log scale
min_y_val_ax1 = np.nanmin(t_hawking_full[t_hawking_full > 0])
if min_y_val_ax1 > 0 : ax1.set_ylim(bottom=min_y_val_ax1 * 0.1)


# --- Plot 2: Zoomed-In Linear Scale near Planck Mass ---
ax2.plot(masses_zoom_plot, t_hawking_zoom,
         label='Standard Hawking (to $M=0$)', color='C0', linestyle='-', linewidth=2)
# Filter NaNs for DCT plot
valid_dct_zoom = ~np.isnan(t_dct_zoom)
ax2.plot(masses_zoom_plot[valid_dct_zoom], t_dct_zoom[valid_dct_zoom],
         label=f'DCT (to $M=M_P$ remnant)', color='C3', linestyle='--', linewidth=2)

# Mark the point where DCT remnant forms (time to become remnant is 0 if starting at M_P)
ax2.plot(M_planck_val, 0, marker='o', markersize=6, color='C3', markeredgecolor='black', label='DCT Remnant State $(M_P, t=0)$')

ax2.set_xlabel('Initial PBH Mass ($M_{PBH}$ / $M_{Planck}$)', fontsize=11)
ax2.set_ylabel('Time to reach $M=0$ (Hawking) or $M=M_P$ (DCT)\n($t_{evap}$ / $t_{P,evap}$)', fontsize=11)
ax2.set_title('Zoomed View near Planck Mass (Linear Scale)', fontsize=13, fontweight='bold')
ax2.legend(fontsize=9)
ax2.grid(True, which="both", ls="-", alpha=0.7)
ax2.axvline(M_planck_val, color='gray', linestyle=':', linewidth=1.5)

# Adjust limits for zoom plot
ax2.set_xlim(M_planck_val * 0.8, M_max_zoom) # Start slightly before M_planck
max_t_hawking_zoom_val = K_hawking * (M_max_zoom**3) # Time for Hawking to evaporate M_max_zoom
ax2.set_ylim(-max_t_hawking_zoom_val*0.05, max_t_hawking_zoom_val * 1.1) # Start y-axis from slightly below 0

fig.suptitle('PBH Evaporation Lifetime: Standard Hawking vs. Dimensional Collapse Theory', fontsize=16, fontweight='bold')
plt.tight_layout(rect=[0, 0, 1, 0.96]) # Adjust layout to make space for suptitle
plt.show()

# plt.savefig('pbh_evaporation_with_zoom.pdf', bbox_inches='tight')
# print("Plot 'pbh_evaporation.pdf' generated.")