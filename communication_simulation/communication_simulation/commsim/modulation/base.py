"""Interfaces shared by modulation and demodulation stages."""

from dataclasses import dataclass
from typing import Protocol

import numpy as np


@dataclass(frozen=True)
class ModulationContext:
    """Provides pulse-shaping parameters to a modulation stage."""

    # RRC roll-off factor, samples per symbol, and filter span in symbols.
    alpha: float
    sps: int
    span: int


@dataclass(frozen=True)
class DemodulationContext:
    """Provides symbol-recovery parameters to a demodulation stage."""

    # Number of output symbols expected after timing recovery.
    symbol_count: int
    alpha: float
    sps: int
    span: int


class ModulationModel(Protocol):
    """Defines a stage that converts bits into a sampled waveform."""

    # Each modulation stage receives bits and returns waveform samples.
    def process(self, bits: np.ndarray, context: ModulationContext) -> np.ndarray:
        """Modulate the input bits using the supplied context."""
        ...


class DemodulationModel(Protocol):
    """Defines a stage that converts a sampled waveform into bits."""

    # Each demodulation stage receives waveform samples and returns bits.
    def process(self, samples: np.ndarray, context: DemodulationContext) -> np.ndarray:
        """Demodulate the input samples using the supplied context."""
        ...
