# simulation.py
from channels import add_noise
from metrics import BerMeasurement, calc_error
import numpy as np
import modulation.bpsk as bpsk
import modulation.pulse_shapes as pulse_shapes

def communication_simulation(
    rng: np.random.Generator,
    size: int,
    eb_n0_db: float,
    alpha: float,
    sps: int,
    span: int,
) -> BerMeasurement:
    
    random_bits = gen_bits(rng, size)
    signal = bpsk.modulate(random_bits)
    shaped_signal = pulse_shapes.apply_tx_pulse_shaping(signal, alpha, sps, span)
    noisy_signal = add_noise(shaped_signal, eb_n0_db, rng)
    filtered_signal = pulse_shapes.apply_rx_matched_filter(noisy_signal, alpha, sps, span)
    downsampled_signal = pulse_shapes.signal_downsample(filtered_signal, size, sps, span)
    received_bits = bpsk.demodulate(downsampled_signal)

    return calc_error(random_bits, received_bits)


# Generate the bits to be processed using a shared RNG instance
def gen_bits(
    rng: np.random.Generator,
    size: int
    ) -> np.ndarray:

    return rng.integers(0, 2, size=size)

def gen_carrier_wave(
    carrier_frequency: float,
    sampling_frequency: float,
    sampling_period: float
    ) -> np.ndarray:

    total_samples = int(sampling_period * sampling_frequency)
    time_period = np.arange(total_samples) / sampling_frequency
    sine_wave = np.sin(2 * np.pi * carrier_frequency * time_period)

    return sine_wave

