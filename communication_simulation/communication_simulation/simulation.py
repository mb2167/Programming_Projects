# simulation.py
from channels import add_noise
from metrics import BerMeasurement, calc_error
import numpy as np
import modulation.pulse_shapes as pulse_shapes
import modulation.bpsk as bpsk
import modulation.qpsk as qpsk

MODULATION_SCHEMES = {
    "bpsk": bpsk,
    "qpsk": qpsk,
}

def communication_simulation(
    rng: np.random.Generator,
    size: int,
    eb_n0_db: float,
    alpha: float,
    sps: int,
    span: int,
    modulation: str,
    samples_per_carrier: int = 16,
    carrier_frequency: float = 1_000.0,
    sampling_frequency: float = 16_000.0,
) -> BerMeasurement:
    
    random_bits = gen_bits(rng, size)

    match modulation:
        case "bpsk":
            symbols = bpsk.modulate(random_bits)
            signal = pulse_shapes.apply_tx_pulse_shaping(symbols, alpha, sps, span)
            noisy_signal = add_noise(signal, eb_n0_db, rng)
            received_signal = pulse_shapes.apply_rx_pulse_shaping(noisy_signal, alpha, sps, span)
            received_bits = bpsk.demodulate(received_signal)

        case "qpsk":
            signal = qpsk.modulate(random_bits, samples_per_carrier, carrier_frequency, sampling_frequency)
            noisy_signal = add_noise(signal, eb_n0_db, rng)
            received_bits = qpsk.demodulate(noisy_signal, carrier_frequency, sampling_frequency, samples_per_carrier)

        case _:
            raise ValueError(f"Unsupported modulation scheme: {modulation}")

    return calc_error(random_bits, received_bits)


# Generate the bits to be processed using a shared RNG instance
def gen_bits(
    rng: np.random.Generator,
    size: int
    ) -> np.ndarray:

    return rng.integers(0, 2, size=size)






