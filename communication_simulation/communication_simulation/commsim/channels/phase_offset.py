# phase_offset.py
import numpy as np
from dataclasses import dataclass
from commsim.config import SimConfig as cfg
from .base import ChannelContext

@dataclass(frozen=True)
class PHASE_OFFSET:
    """Phase offset channel."""

    phase_offset: float = cfg.TX_PHASE_OFFSET - cfg.RX_PHASE_OFFSET
    frequency_offset: float = cfg.TX_FREQUENCY_OFFSET - cfg.RX_FREQUENCY_OFFSET
    phase_noise: float = 0.0

    def process(
        self,
        signal: np.ndarray,
        context: ChannelContext,
    ) -> np.ndarray:
        # Apply phase offset
        time = np.arange(signal.size) / context.sample_rate_hz
        phase_shift = (self.phase_offset + 2 * np.pi * self.frequency_offset * time + context.rng.normal(0.0, self.phase_noise, size=signal.shape))
        return signal * np.exp(1j * phase_shift)
