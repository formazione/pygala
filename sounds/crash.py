import numpy as np
from scipy.io.wavfile import write
import os
# Parameters for the sound
sample_rate = 44100  # Sample rate in Hz
duration = 1  # Duration in seconds

# Generate time axis
t = np.linspace(1, duration, int(sample_rate * duration), endpoint=False)

# Generate base spaceship hum sound
freq_hum = 200  # Frequency of the hum in Hz
spaceship_hum = 0.5 * np.sin(2 * np.pi * freq_hum * t)
# Generate a short crash noise
crash_duration = 0.3  # Duration of the crash in seconds
crash_t = np.linspace(0, crash_duration, int(sample_rate * crash_duration), endpoint=False)

# Generate crash sound as white noise
crash_sound = np.random.normal(0, 1, len(crash_t))

# Apply an envelope to the crash sound to make it more like a burst
envelope = np.exp(-5 * crash_t)
crash_sound *= envelope

# Combine the crash sound with the spaceship hum
start_idx = int(sample_rate * 0.00)  # Start the crash sound at 0.5 seconds
end_idx = start_idx + len(crash_sound)
spaceship_hum[start_idx:end_idx] += crash_sound

# Normalize the sound to prevent clipping
spaceship_hum /= np.max(np.abs(spaceship_hum))

# Save the sound to a wav file
crash_file_path = 'spaceship_crash.wav'
write(crash_file_path, sample_rate, spaceship_hum.astype(np.float32))

os.system(crash_file_path)
