"""Simulation orchestration."""

import numpy as np

from .channels import add_noise
from .metrics import BerMeasurement, calc_error
from .modulation import bpsk, qpsk

MODULATION_SCHEMES = {"bpsk": bpsk, "qpsk": qpsk}


def communication_simulation(
    rng: np.random.Generator,
    size: int,
    eb_n0_db: float,
    alpha: float,
    sps: int,
    span: int,
    modulation: str,
) -> BerMeasurement:
    random_bits = gen_bits(rng, size)
    match modulation:
        case "bpsk":
            signal = bpsk.modulate(random_bits, alpha, sps, span)
            noisy_signal = add_noise(signal, eb_n0_db, rng, bits_per_symbol=1)
            received_bits = bpsk.demodulate(noisy_signal, size, alpha, sps, span)
        case "qpsk":
            if size % 2:
                raise ValueError("QPSK requires an even number of bits.")
            signal = qpsk.modulate(random_bits, alpha, sps, span)
            noisy_signal = add_noise(signal, eb_n0_db, rng, bits_per_symbol=2)
            received_bits = qpsk.demodulate(noisy_signal, size // 2, alpha, sps, span)
        case _:
            raise ValueError(f"Unsupported modulation scheme: {modulation}")
    return calc_error(random_bits, received_bits)


def gen_bits(rng: np.random.Generator, size: int) -> np.ndarray:
    return rng.integers(0, 2, size=size)
