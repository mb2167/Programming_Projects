# modulation/qpsk.py
import numpy as np
from .pulse_shapes import low_pass_filter

# ------------------------------ PRE-TRANSMISSION SETUP ------------------------------

# Convert the bits into a QPSK signal
def modulate(
    bit_array: np.ndarray,
    samples_per_carrier: int,
    carrier_frequency: float,
    sampling_frequency: float,
) -> np.ndarray:

    # Convert bits into QPSK phase shifts
    symbol_pairs = bit_array.reshape(-1, 2)
    indices = symbol_pairs[:, 0] * 2 + symbol_pairs[:, 1]

    pi_4 = np.pi / 4
    phase_lookup = np.array([
        pi_4,       # 00
        3 * pi_4,   # 01
        7 * pi_4,   # 10
        5 * pi_4,   # 11
    ])

    phases = phase_lookup[indices]

    # Generate a sine wave with phase shifts
    upsampled_phases = np.repeat(phases, samples_per_carrier)
    time = np.arange(upsampled_phases.size) / sampling_frequency

    return np.cos(2 * np.pi * carrier_frequency * time + upsampled_phases)


# ------------------------------ POST-TRANSMISSION PROCESSING ------------------------------

# Convert the signal back to bits
def demodulate(
    signal: np.ndarray,
    carrier_frequency: float,
    sampling_frequency: float,
    samples_per_carrier: int
) -> np.ndarray:
    # Mix the received signal with coherent in-phase and quadrature carriers
    time = np.arange(signal.size) / sampling_frequency
    carrier_phase = 2 * np.pi * carrier_frequency * time

    i_signal = signal * np.cos(carrier_phase)
    q_signal = -signal * np.sin(carrier_phase)

    filtered_i_signal = low_pass_filter(i_signal, samples_per_carrier)
    filtered_q_signal = low_pass_filter(q_signal, samples_per_carrier)

    # Take one I/Q decision sample from the centre of each symbol period
    symbol_indices = np.arange(samples_per_carrier // 2, signal.size, samples_per_carrier)

    i_symbols = filtered_i_signal[symbol_indices]
    q_symbols = filtered_q_signal[symbol_indices]

    bits = np.empty(i_symbols.size * 2, dtype=int)
    bits[0::2] = q_symbols < 0
    bits[1::2] = i_symbols < 0

    return bits
