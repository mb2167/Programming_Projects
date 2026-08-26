# modulation/qpsk.py
import numpy as np
from .base import DemodulationContext, ModulationContext
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
    # Map each bit pair onto the in-phase and quadrature components.
    i_symbols = 1 - 2 * symbol_pairs[:, 0]
    q_symbols = 1 - 2 * symbol_pairs[:, 1]
    # Normalise so that every complex QPSK symbol has unit energy.
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
    # Remove the combined RRC delay and retain one sample per symbol.
    symbols = signal_downsample(filtered_signal, symbol_count, sps, span)
    bits = np.empty(symbols.size * 2, dtype=int)
    # Decide the I and Q components independently to recover both bit streams.
    bits[0::2] = (symbols.real < 0).astype(int)
    bits[1::2] = (symbols.imag < 0).astype(int)

    return bits


class QPSKModulator:
    """Adapts the QPSK transmitter to a modulation-chain stage."""

    def process(self, bits: np.ndarray, context: ModulationContext) -> np.ndarray:
        """Create an RRC-shaped QPSK waveform from the input bits."""
        return modulate(bits, context.alpha, context.sps, context.span)


class QPSKDemodulator:
    """Adapts the QPSK receiver to a demodulation-chain stage."""

    def process(self, samples: np.ndarray, context: DemodulationContext) -> np.ndarray:
        """Recover QPSK bits from the input waveform."""
        return demodulate(
            samples,
            context.symbol_count,
            context.alpha,
            context.sps,
            context.span,
        )
