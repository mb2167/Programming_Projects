# channel/base.py

from dataclasses import dataclass

from typing import Protocol

import numpy as np


@dataclass(frozen=True)
class ChannelContext:
    """Context shared by channel/noise models."""

    sample_rate_hz: float
    carrier_frequency_hz: float
    rng: np.random.Generator

class ChannelModel(Protocol):
    """Interface implemented by all channel models."""

    def process(
        self,
        signal: np.ndarray,
        context: ChannelContext,
    ) -> np.ndarray:
        ...