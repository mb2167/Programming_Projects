"""Interface for DAC, PA, oscillator, ADC, and other hardware models."""

from dataclasses import dataclass
from typing import Protocol

import numpy as np


@dataclass(frozen=True)
class SignalContext:
    sample_rate_hz: float
    carrier_frequency_hz: float
    rng: np.random.Generator


class HardwareModel(Protocol):
    def process(self, samples: np.ndarray, context: SignalContext) -> np.ndarray: ...
