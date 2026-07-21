# modulation/bpsk.py
import numpy as np
from .pulse_shapes import low_pass_filter

# ------------------------------ PRE-TRANSMISSION SETUP ------------------------------

# Convert the bits into a BPSK signal
def modulate(
    bit_array: np.ndarray,
    samples_per_carrier: int,
    carrier_frequency: float,
    sampling_frequency: float,
) -> np.ndarray:

    # Convert bits into BPSK phase shifts

    phases = np.where(bit_array == 0, np.pi, 0.0)

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
    samples_per_carrier: int,
) -> np.ndarray:

    # Recreate the carrier used by the transmitter
    time = np.arange(signal.size) / sampling_frequency
    carrier = np.cos(2 * np.pi * carrier_frequency * time)

    mixed_signal = signal * carrier

    filtered_signal = low_pass_filter(mixed_signal, samples_per_carrier)

    # Take one decision sample from the centre of every bit period
    symbol_indices = np.arange(
        samples_per_carrier // 2,
        signal.size,
        samples_per_carrier,
    )
    symbols = filtered_signal[symbol_indices]

    # Negative corresponds to bit 0; positive corresponds to bit 1
    return np.where(symbols < 0, 0, 1)
