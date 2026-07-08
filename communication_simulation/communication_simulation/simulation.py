# simulation.py
from channels import add_noise
from metrics import calc_error
import numpy as np
import modulation.bpsk as bpsk
import modulation.pulse_shapes as pulse_shapes
from plotting import plot_signal



def communication_simulation(rng: int, size: int, snr_db: int,
                             alpha: float, sps: int, span: int):
    random_bits = gen_bits(rng, size)
    signal = bpsk.modulate(random_bits)
    shaped_signal = pulse_shapes.apply_tx_pulse_shaping(signal, alpha, sps, span)
    noisy_signal = add_noise(shaped_signal, snr_db, rng)
    filtered_signal = pulse_shapes.apply_rx_matched_filter(noisy_signal, alpha, sps, span)
    downsampled_signal = pulse_shapes.signal_downsample(filtered_signal, size, sps, span)
    received_bits = bpsk.demodulate(downsampled_signal)
    error = calc_error(random_bits, received_bits)
    return error


# Generate the bits to be processed using a shared RNG instance
def gen_bits(rng: int, size: int):
    return rng.integers(0, 2, size=size)

