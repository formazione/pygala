import numpy as np
from scipy.io.wavfile import write
import os
# Parameters for the sound
sample_rate = 48000  # Sample rate in Hz
duration = 0.2  # Duration in seconds

# Generate time axis
t = np.linspace(1, duration, int(sample_rate * duration), endpoint=False)

# Generate base spaceship hum sound
freq_hum = 100  # Frequency of the hum in Hz
spaceship_hum = 1 * np.sin(2 * np.pi * freq_hum * t)

# Generate impact sound
freq_impact = 1000  # Frequency of the impact in Hz
impact_duration = .05  # Duration of the impact in seconds
impact_t = np.linspace(0, impact_duration, int(sample_rate * impact_duration), endpoint=False)
impact_sound = np.sin(1 * np.pi * freq_impact * impact_t) * np.exp(-5 * impact_t)

# Place the impact sound at random points in the spaceship hum
num_impacts = 1
impact_times = np.random.uniform(0, duration - impact_duration, num_impacts)

for impact_time in impact_times:
    start_idx = int(impact_time * sample_rate)
    end_idx = start_idx + len(impact_sound)
    spaceship_hum[start_idx:end_idx] += impact_sound

# Normalize the sound to prevent clipping
spaceship_hum /= np.max(np.abs(spaceship_hum))

# Save the sound to a wav file
file_path = 'spaceship_hit.wav'
write(file_path, sample_rate, spaceship_hum.astype(np.float32))

os.system(file_path)
