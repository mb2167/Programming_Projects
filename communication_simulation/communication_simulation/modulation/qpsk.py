# modulation/qpsk.py
import numpy as np

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

    return np.sin(2 * np.pi * carrier_frequency * time + upsampled_phases)


# ------------------------------ POST-TRANSMISSION PROCESSING ------------------------------

# Convert the signal back to bits
def demodulate(
    signal: np.ndarray,
) -> np.ndarray:
    pass
