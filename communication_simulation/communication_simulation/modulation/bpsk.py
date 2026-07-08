# modulation/bpsk.py
import numpy as np

# ------------------------------ PRE-TRANSMISSION SETUP ------------------------------

# Convert the bits into a BPSK signal
def modulate(bit_array: np.ndarray):
    symbols = (bit_array * 2) - 1
    return symbols


# ------------------------------ POST-TRANSMISSION PROCESSING ------------------------------

# Convert the signal back to bits
def demodulate(signal: np.ndarray):
    return np.where(signal < 0, 0, 1)