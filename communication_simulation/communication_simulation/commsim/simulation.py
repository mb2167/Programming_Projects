"""Simulation orchestration."""

import numpy as np

from .channels import AWGN, ChannelChain, ChannelContext
from .hardware import ReceiverHardwareChain, SignalContext, TransmitterHardwareChain
from .metrics import BerMeasurement, calc_error
from .modulation import (
    BPSKDemodulator,
    BPSKModulator,
    DemodulationChain,
    DemodulationContext,
    ModulationChain,
    ModulationContext,
    QPSKDemodulator,
    QPSKModulator,
)


MODULATION_SCHEMES = {
    "bpsk": (
        ModulationChain((BPSKModulator(),)),
        DemodulationChain((BPSKDemodulator(),)),
        1,
    ),
    "qpsk": (
        ModulationChain((QPSKModulator(),)),
        DemodulationChain((QPSKDemodulator(),)),
        2,
    ),
}
DEFAULT_TRANSMITTER_HARDWARE = TransmitterHardwareChain()
DEFAULT_RECEIVER_HARDWARE = ReceiverHardwareChain()



# Run a configured modem through transmit hardware, a channel, and receive hardware.
def communication_simulation(
    rng: np.random.Generator,
    size: int,
    eb_n0_db: float,
    alpha: float,
    sps: int,
    span: int,
    modulation: str,
    transmitter_hardware: TransmitterHardwareChain | None = None,
    receiver_hardware: ReceiverHardwareChain | None = None,
    sample_rate_hz: float = 1.0,
    carrier_frequency_hz: float = 0.0,
) -> BerMeasurement:

    random_bits = gen_bits(rng, size)

    try:
        modulation_chain, demodulation_chain, bits_per_symbol = MODULATION_SCHEMES[modulation]

    except KeyError as error:
        raise ValueError(f"Unsupported modulation scheme: {modulation}") from error

    if size % bits_per_symbol:
        raise ValueError(f"{modulation.upper()} requires a bit count divisible by {bits_per_symbol}.")

    hardware_context = SignalContext(sample_rate_hz, carrier_frequency_hz, rng)
    channel_context = ChannelContext(sample_rate_hz, carrier_frequency_hz, rng)
    modulation_context = ModulationContext(alpha, sps, span)
    demodulation_context = DemodulationContext(size // bits_per_symbol, alpha, sps, span)

    transmitter_hardware = transmitter_hardware or DEFAULT_TRANSMITTER_HARDWARE
    receiver_hardware = receiver_hardware or DEFAULT_RECEIVER_HARDWARE
    channel_chain = ChannelChain((AWGN(eb_n0_db, bits_per_symbol),))

    signal = modulation_chain.process(random_bits, modulation_context)
    transmitted_signal = transmitter_hardware.process(signal, hardware_context)
    channel_output = channel_chain.process(transmitted_signal, channel_context)
    received_signal = receiver_hardware.process(channel_output, hardware_context)
    received_bits = demodulation_chain.process(received_signal, demodulation_context)

    return calc_error(random_bits, received_bits)


# Generate binary data using the supplied random-number generator.
def gen_bits(rng: np.random.Generator, size: int) -> np.ndarray:
    return rng.integers(0, 2, size=size)
