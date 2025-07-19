import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft, fftfreq

# --- Parameters from the Time-Domain Echo Waveform ---
# Ensure these are consistent with the parameters used in plot_echo_waveform.py
t_ringdown_peak = 0.001 # Time of the peak of the main ringdown (seconds)
sigma_ringdown = 0.0003 # Width of the ringdown pulse (seconds)
A_ringdown = 1.0        # Amplitude of the ringdown

delta_t_echo = 0.001809 # Echo delay time (seconds), e.g., 1.8 ms
num_echoes = 4          # Number of echoes
A_echo_initial = 0.4    # Amplitude of the first echo relative to ringdown
R_reflection = 0.7      # Reflection coefficient (amplitude decay factor per echo)
sigma_echo = 0.0002     # Width of the echo pulses

f0 = 200  # Carrier frequency (Hz)

# --- Time Array for Waveform Generation (needs to be long enough for FFT resolution) ---
# For good frequency resolution, we need a longer time series and higher sampling rate
sampling_rate = 20000  # Hz (e.g., 20 kHz)
t_duration = t_ringdown_peak + (num_echoes + 2) * delta_t_echo # Extend duration a bit
t = np.arange(0, t_duration, 1/sampling_rate)
N_samples = len(t)

# --- Waveform Generation Functions (same as before) ---
def gaussian_wavelet(t_values, t_peak, A, sigma, freq):
    envelope = A * np.exp(-((t_values - t_peak)**2) / (2 * sigma**2))
    # Ensure carrier is zero outside a reasonable window to avoid artifacts
    # This is a simple way to make the wavelet more compact in time
    window_factor = np.exp(-((t_values - t_peak)**2) / (8 * sigma**2)) # Softer window
    carrier = np.sin(2 * np.pi * freq * (t_values - t_peak))
    return envelope * carrier * window_factor

# --- Generate Ringdown ---
h_ringdown = gaussian_wavelet(t, t_ringdown_peak, A_ringdown, sigma_ringdown, f0)
waveform = h_ringdown

# --- Generate Echoes ---
echo_times = [t_ringdown_peak + (n + 1) * delta_t_echo for n in range(num_echoes)]
echo_amplitudes = [A_echo_initial * (R_reflection**n) for n in range(num_echoes)]

for i in range(num_echoes):
    h_echo = gaussian_wavelet(t, echo_times[i], echo_amplitudes[i], sigma_echo, f0)
    waveform += h_echo

# --- Fourier Transform ---
# We are interested in the magnitude of the Fourier transform
yf = fft(waveform)
xf = fftfreq(N_samples, 1 / sampling_rate)

# Keep only the positive frequencies
positive_freq_mask = xf >= 0
xf_positive = xf[positive_freq_mask]
yf_positive_magnitude = np.abs(yf[positive_freq_mask]) / N_samples # Normalize amplitude

# --- Plotting the Spectrum ---
plt.style.use('seaborn-v0_8-whitegrid')
fig, ax = plt.subplots(figsize=(10, 6))

# Plotting a range around the carrier frequency f0
plot_freq_min = max(0, f0 - 1/(delta_t_echo * 0.5) ) # Show a few comb peaks around f0
plot_freq_max = f0 + 1/(delta_t_echo * 0.5)
freq_range_mask = (xf_positive >= plot_freq_min) & (xf_positive <= plot_freq_max)

ax.plot(xf_positive[freq_range_mask], yf_positive_magnitude[freq_range_mask], color='C0', linewidth=1.5)

ax.set_xlabel('Frequency (Hz)', fontsize=12)
ax.set_ylabel('Amplitude Spectral Density (Arbitrary Units)', fontsize=12)
ax.set_title(f'Frequency Spectrum of Echo Train ($\\Delta t_{{echo}} = {delta_t_echo*1000:.1f}$ ms)', fontsize=14, fontweight='bold')

# Annotate expected comb peaks
comb_spacing = 1 / delta_t_echo
# Find carrier peak index
carrier_peak_idx = np.argmin(np.abs(xf_positive - f0))
carrier_peak_freq = xf_positive[carrier_peak_idx]

# Determine the 'central' comb peak closest to f0
n_central_comb = np.round(carrier_peak_freq / comb_spacing)
central_comb_freq = n_central_comb * comb_spacing

# Plot vertical lines for a few comb peaks
for n_offset in range(-3, 4): # Show a few peaks around the central one
    peak_freq = central_comb_freq + n_offset * comb_spacing
    if plot_freq_min <= peak_freq <= plot_freq_max:
        ax.axvline(peak_freq, color='C3', linestyle='--', linewidth=0.8, alpha=0.7)
        # ax.text(peak_freq + comb_spacing*0.05, np.max(yf_positive_magnitude[freq_range_mask])*0.8,
        #         f'{peak_freq:.1f} Hz', rotation=90, fontsize=8, va='center', ha='left')

ax.text(0.95, 0.95, f'Comb spacing $\\approx 1/\\Delta t_{{echo}} \\approx {comb_spacing:.1f}$ Hz',
        horizontalalignment='right', verticalalignment='top', transform=ax.transAxes,
        fontsize=10, bbox=dict(boxstyle='round,pad=0.3', fc='wheat', alpha=0.5))


ax.grid(True, which="both", ls="-", alpha=0.7)
ax.set_xlim(plot_freq_min, plot_freq_max)
ax.tick_params(axis='both', which='major', labelsize=10)

plt.tight_layout()
plt.show()

# plt.savefig('echo_spectrum.pdf')
# print("Plot 'echo_spectrum.pdf' generated.")