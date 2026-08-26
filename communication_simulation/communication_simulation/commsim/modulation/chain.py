"""Composition of modulation and demodulation stages."""

from dataclasses import dataclass, field

import numpy as np

from .base import (
    DemodulationContext,
    DemodulationModel,
    ModulationContext,
    ModulationModel,
)


@dataclass(frozen=True)
class ModulationChain:
    """Runs stages that transform bits into a transmit waveform."""

    stages: tuple[ModulationModel, ...] = field(default_factory=tuple)

    def process(self, bits: np.ndarray, context: ModulationContext) -> np.ndarray:
        """Pass bits through every configured modulation stage."""
        # The output of one stage becomes the input to the next stage.
        samples = bits
        for stage in self.stages:
            samples = stage.process(samples, context)
        return samples


@dataclass(frozen=True)
class DemodulationChain:
    """Runs stages that transform received samples back into bits."""

    stages: tuple[DemodulationModel, ...] = field(default_factory=tuple)

    def process(self, samples: np.ndarray, context: DemodulationContext) -> np.ndarray:
        """Pass samples through every configured demodulation stage."""
        # The output of one stage becomes the input to the next stage.
        bits = samples
        for stage in self.stages:
            bits = stage.process(bits, context)
        return bits
