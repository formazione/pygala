import numpy as np
from scipy.io.wavfile import write
import sounddevice as sd
import tkinter as tk
from tkinter import ttk, filedialog
import os

# Function to generate sound
def generate_sound():
    global sound_data
    sample_rate = 44100
    duration = float(duration_var.get())
    freq = float(frequency_var.get())
    envelope = envelope_var.get()

    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    
    if envelope == 'Sine':
        sound = np.sin(2 * np.pi * freq * t)
    elif envelope == 'Noise':
        sound = np.random.normal(0, 1, len(t))
    elif envelope == 'Crash':
        sound = np.random.normal(0, 1, len(t)) * np.exp(-5 * t)

    sound /= np.max(np.abs(sound))
    sound_data = sound.astype(np.float32)

# Function to play sound
def play_sound():
    if sound_data is not None:
        sd.play(sound_data, 44100)
        sd.wait()

# Function to save sound
def save_sound():
    if sound_data is not None:
        save_path = filedialog.asksaveasfilename(defaultextension=".wav", filetypes=[("WAV files", "*.wav")])
        if save_path:
            write(save_path, 44100, sound_data)

# Create the main window
root = tk.Tk()
root.title("FX Sound Generator")

sound_data = None

# Sound name input
ttk.Label(root, text="Sound Name:").grid(row=0, column=0, padx=10, pady=10)
sound_name_var = tk.StringVar()
ttk.Entry(root, textvariable=sound_name_var).grid(row=0, column=1, padx=10, pady=10)

# Duration input
ttk.Label(root, text="Duration (s):").grid(row=1, column=0, padx=10, pady=10)
duration_var = tk.StringVar(value="1.0")
ttk.Entry(root, textvariable=duration_var).grid(row=1, column=1, padx=10, pady=10)

# Frequency input
ttk.Label(root, text="Frequency (Hz):").grid(row=2, column=0, padx=10, pady=10)
frequency_var = tk.StringVar(value="440")
ttk.Entry(root, textvariable=frequency_var).grid(row=2, column=1, padx=10, pady=10)

# Envelope selection
ttk.Label(root, text="Envelope:").grid(row=3, column=0, padx=10, pady=10)
envelope_var = tk.StringVar(value="Sine")
envelope_menu = ttk.Combobox(root, textvariable=envelope_var)
envelope_menu['values'] = ('Sine', 'Noise', 'Crash')
envelope_menu.grid(row=3, column=1, padx=10, pady=10)

# Generate button
generate_button = ttk.Button(root, text="Generate Sound", command=generate_sound)
generate_button.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

# Preview button
preview_button = ttk.Button(root, text="Preview Sound", command=play_sound)
preview_button.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

# Save button
save_button = ttk.Button(root, text="Save Sound", command=save_sound)
save_button.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

# Run the main loop
root.mainloop()
