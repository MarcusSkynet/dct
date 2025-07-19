import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

# --- Parameters for the Echo Waveform (same as your setup) ---
t_ringdown_peak = 0.001
sigma_ringdown = 0.0003
A_ringdown = 1.0 # Initial plot had this at 1.0, but your image shows peak around 0.23. Let's use a value consistent with your image for label placement.
                 # If your actual A_ringdown is 1.0, the labels will adjust.
                 # For the image you sent, let's assume the plotted A_ringdown was scaled down for the y-axis.
                 # Let's use the actual peak value from your waveform for y-pos.

delta_t_echo = 0.001809
num_echoes = 4
A_echo_initial = A_ringdown * 0.25 # Example: first echo is 25% of ringdown peak in your image
R_reflection = 0.7
sigma_echo = 0.0002
f0 = 200

# Time array
t_start = -0.001 # Start a bit earlier to see the rise
t_end = t_ringdown_peak + (num_echoes + 0.5) * delta_t_echo
t = np.linspace(t_start, t_end, 2000)

# --- Waveform Generation Functions ---
def gaussian_wavelet(t_values, t_peak, A, sigma, freq):
    envelope = A * np.exp(-((t_values - t_peak)**2) / (2 * sigma**2))
    # Using a window to make pulses more distinct in time if needed
    window_factor = np.exp(-((t_values - t_peak)**2) / (6 * sigma**2)) # Slightly wider window
    carrier = np.sin(2 * np.pi * freq * (t_values - t_peak))
    return envelope * carrier * window_factor

# --- Generate Ringdown ---
# For this example, let's scale A_ringdown to match your image's y-axis roughly
# Say the peak of your plotted ringdown is at y=0.23
# We can generate it with A=1 and then scale the whole waveform if needed, or just adjust A_ringdown here.
# For label placement, what matters is the *actual y-value of the peak*.
# Let's assume the `waveform` variable correctly holds your plotted data.

# --- Generate Ringdown (assuming waveform is already generated as in your plot) ---
# For the purpose of placing labels, we need the peak y-values.
# Let's simulate the waveform again to get those peaks.
h_ringdown_actual = gaussian_wavelet(t, t_ringdown_peak, A_ringdown, sigma_ringdown, f0)
waveform_actual = h_ringdown_actual

echo_times_actual = [t_ringdown_peak + (n + 1) * delta_t_echo for n in range(num_echoes)]
echo_amplitudes_actual = [A_echo_initial * (R_reflection**n) for n in range(num_echoes)]

for i in range(num_echoes):
    h_echo_actual = gaussian_wavelet(t, echo_times_actual[i], echo_amplitudes_actual[i], sigma_echo, f0)
    waveform_actual += h_echo_actual
    
# --- Plotting (assuming `waveform_actual` is what you plotted) ---
plt.style.use('seaborn-v0_8-whitegrid')
fig, ax = plt.subplots(figsize=(10, 6))

ax.plot(t * 1000, waveform_actual, color='C0', linewidth=1.5) # Plot the actual waveform

ax.set_xlabel('Time (ms)', fontsize=12)
ax.set_ylabel('Strain (Arbitrary Units)', fontsize=12)
ax.set_title('Simulated Gravitational Wave Signal with Echoes (DCT)', fontsize=14, fontweight='bold')
ax.grid(True, which="both", ls="-", alpha=0.7)
ax.axhline(0, color='black', linewidth=0.5, linestyle='--')
ax.set_xlim(t_start * 1000, t_end * 1000 + 0.5)
# Based on your image, y-limits are roughly -0.25 to 0.25
y_plot_peak = np.max(waveform_actual) # Actual peak of the ringdown in the data
ax.set_ylim(-y_plot_peak * 1.1, y_plot_peak * 1.2)


# --- REVISED ANNOTATIONS ---
# Fixed y-offset in data coordinates for labels
label_y_offset_data = y_plot_peak * 0.08  # e.g., 8% of the main ringdown peak height

# Ringdown Label
# Find the actual peak value of the ringdown portion
ringdown_peak_y_val = np.max(h_ringdown_actual) # Max of the first pulse
ax.text(t_ringdown_peak * 1000, ringdown_peak_y_val + label_y_offset_data, 'Ringdown',
        ha='center', va='bottom', fontsize=10, color='black')

# Echo Labels
for i in range(num_echoes):
    # Find the actual peak y-value of this specific echo pulse
    # This requires isolating the echo; for simplicity, we'll use the defined echo_amplitudes
    # If echoes are positive-going peaks:
    current_echo_peak_y_val = echo_amplitudes_actual[i]
    # If echoes can also be negative, we'd need to find the peak of abs(echo_pulse)
    # Assuming positive peaks for simplicity of label placement:
    
    if current_echo_peak_y_val > 0.01: # Only label if echo is somewhat significant
        ax.text(echo_times_actual[i] * 1000, (ringdown_peak_y_val * 0.3)+ label_y_offset_data, f'Echo {i+1}',
                ha='center', va='bottom', fontsize=9, color='C3')

plt.tight_layout()
plt.show()

# plt.savefig('echo_waveform.pdf')
# print("Plot 'echo_waveform.pdf' generated.")