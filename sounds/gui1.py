import numpy as np
from scipy.io.wavfile import write
import tkinter as tk
from tkinter import ttk, filedialog
import os

# Function to generate and save sound
def generate_sound():
    sample_rate = 44100
    duration = float(duration_var.get())
    freq = float(frequency_var.get())
    envelope = envelope_var.get()
    save_path = filedialog.asksaveasfilename(defaultextension=".wav", filetypes=[("WAV files", "*.wav")])
    
    if not save_path:
        return

    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    
    if envelope == 'Sine':
        sound = np.sin(2 * np.pi * freq * t)
    elif envelope == 'Noise':
        sound = np.random.normal(0, 1, len(t))
    elif envelope == 'Crash':
        sound = np.random.normal(0, 1, len(t)) * np.exp(-5 * t)

    sound /= np.max(np.abs(sound))
    write(save_path, sample_rate, sound.astype(np.float32))

# Create the main window
root = tk.Tk()
root.title("FX Sound Generator")

# Duration input
ttk.Label(root, text="Duration (s):").grid(row=0, column=0, padx=10, pady=10)
duration_var = tk.StringVar(value="1.0")
ttk.Entry(root, textvariable=duration_var).grid(row=0, column=1, padx=10, pady=10)

# Frequency input
ttk.Label(root, text="Frequency (Hz):").grid(row=1, column=0, padx=10, pady=10)
frequency_var = tk.StringVar(value="440")
ttk.Entry(root, textvariable=frequency_var).grid(row=1, column=1, padx=10, pady=10)

# Envelope selection
ttk.Label(root, text="Envelope:").grid(row=2, column=0, padx=10, pady=10)
envelope_var = tk.StringVar(value="Sine")
envelope_menu = ttk.Combobox(root, textvariable=envelope_var)
envelope_menu['values'] = ('Sine', 'Noise', 'Crash')
envelope_menu.grid(row=2, column=1, padx=10, pady=10)

# Generate button
generate_button = ttk.Button(root, text="Generate and Save Sound", command=generate_sound)
generate_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

# Run the main loop
root.mainloop()
