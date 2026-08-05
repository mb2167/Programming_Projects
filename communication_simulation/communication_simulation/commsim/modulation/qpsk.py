# modulation/qpsk.py
import numpy as np
from .pulse_shapes import (
    apply_rx_matched_filter,
    apply_tx_pulse_shaping,
    signal_downsample,
)

# ------------------------------ PRE-TRANSMISSION SETUP ------------------------------

# Convert the bits into a QPSK signal
def modulate(
    bit_array: np.ndarray,
    alpha: float,
    sps: int,
    span: int,
) -> np.ndarray:
    """Create a pulse-shaped, complex-baseband QPSK waveform."""
    if bit_array.size % 2:
        raise ValueError("QPSK requires an even number of bits.")

    symbol_pairs = bit_array.reshape(-1, 2)
    i_symbols = 1 - 2 * symbol_pairs[:, 0]
    q_symbols = 1 - 2 * symbol_pairs[:, 1]
    symbols = (i_symbols + 1j * q_symbols) / np.sqrt(2)
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
    """Matched-filter and make hard decisions on a QPSK baseband waveform."""
    filtered_signal = apply_rx_matched_filter(signal, alpha, sps, span)
    symbols = signal_downsample(filtered_signal, symbol_count, sps, span)
    bits = np.empty(symbols.size * 2, dtype=int)
    bits[0::2] = (symbols.real < 0).astype(int)
    bits[1::2] = (symbols.imag < 0).astype(int)

    return bits
