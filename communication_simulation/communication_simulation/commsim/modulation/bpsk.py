# modulation/bpsk.py
import numpy as np
from .pulse_shapes import apply_rx_matched_filter, apply_tx_pulse_shaping, signal_downsample

# ------------------------------ PRE-TRANSMISSION SETUP ------------------------------

# Convert the bits into a BPSK signal
def modulate(
    bit_array: np.ndarray,
    alpha: float,
    sps: int,
    span: int,
) -> np.ndarray:

    """Create a pulse-shaped, real-baseband BPSK waveform."""
    symbols = 2 * bit_array - 1
    return apply_tx_pulse_shaping(symbols, alpha, sps, span)
   

# ------------------------------ POST-TRANSMISSION PROCESSING ------------------------------

# Convert the signal back to bits
def demodulate(
    signal: np.ndarray,
    symbol_count: int,
    alpha: float,
    sps: int,
    span: int,
) -> np.ndarray:

    # Recreate the carrier used by the transmitter
    filtered_signal = apply_rx_matched_filter(signal, alpha, sps, span)
    symbols = signal_downsample(filtered_signal, symbol_count, sps, span)
    bits = (symbols >= 0).astype(int)
    return bits