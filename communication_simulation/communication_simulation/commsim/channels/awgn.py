# channel/awgn.py

from dataclasses import dataclass

import numpy as np

from .base import ChannelContext


@dataclass(frozen=True)
class AWGN:
    """Additive white Gaussian noise channel."""

    eb_n0_db: float
    bits_per_symbol: int = 1

    def process(
        self,
        signal: np.ndarray,
        context: ChannelContext,
    ) -> np.ndarray:
        if self.bits_per_symbol <= 0:
            raise ValueError("bits_per_symbol must be positive.")

        eb_n0_linear = 10 ** (self.eb_n0_db / 10)

        noise_std = np.sqrt(1 / (2 * self.bits_per_symbol * eb_n0_linear))

        noise = context.rng.normal(0.0, noise_std, size=signal.shape)

        if np.iscomplexobj(signal):
            noise = noise + 1j * context.rng.normal(0.0, noise_std, size=signal.shape)

        return signal + noise