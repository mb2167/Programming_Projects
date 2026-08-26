# modulation/bpsk.py
import numpy as np
from .base import DemodulationContext, ModulationContext
from .pulse_shapes import apply_rx_matched_filter, apply_tx_pulse_shaping, signal_downsample

# ------------------------------ PRE-TRANSMISSION SETUP ------------------------------

# Convert the bits into a BPSK signal
def modulate(
    bit_array: np.ndarray,
    alpha: float,
    sps: int,
    span: int,
) -> np.ndarray:

    """Create a pulse-shaped, real-baseband BPSK waveform."""
    # Map binary values to antipodal BPSK symbols: 0 -> -1 and 1 -> +1.
    symbols = 2 * bit_array - 1
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

    # Match the transmit RRC filter before taking one sample per symbol.
    filtered_signal = apply_rx_matched_filter(signal, alpha, sps, span)
    symbols = signal_downsample(filtered_signal, symbol_count, sps, span)
    # Reverse the transmitter mapping by deciding from each symbol's sign.
    bits = (symbols >= 0).astype(int)
    return bits


class BPSKModulator:
    """Adapts the BPSK transmitter to a modulation-chain stage."""

    def process(self, bits: np.ndarray, context: ModulationContext) -> np.ndarray:
        """Create an RRC-shaped BPSK waveform from the input bits."""
        return modulate(bits, context.alpha, context.sps, context.span)


class BPSKDemodulator:
    """Adapts the BPSK receiver to a demodulation-chain stage."""

    def process(self, samples: np.ndarray, context: DemodulationContext) -> np.ndarray:
        """Recover BPSK bits from the input waveform."""
        return demodulate(
            samples,
            context.symbol_count,
            context.alpha,
            context.sps,
            context.span,
        )
