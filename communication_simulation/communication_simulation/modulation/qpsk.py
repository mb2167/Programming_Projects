# modulation/qpsk.py
import numpy as np

# ------------------------------ PRE-TRANSMISSION SETUP ------------------------------

# Convert the bits into a BPSK signal
def modulate(
    bit_array: np.ndarray,
) -> np.ndarray:
    
    symbols = (bit_array * 2) - 1
    paired_symbols = np.reshape(symbols, (-1, 2))




# ------------------------------ POST-TRANSMISSION PROCESSING ------------------------------

# Convert the signal back to bits
def demodulate(
    signal: np.ndarray,
) -> np.ndarray:
    pass
