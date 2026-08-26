"""Hardware-stage composition."""

from dataclasses import dataclass, field

import numpy as np

from .base import HardwareModel, SignalContext


@dataclass(frozen=True)
class IdentityHardware:
    """Default stage; useful when no hardware impairment is modelled."""

    def process(self, samples: np.ndarray, context: SignalContext) -> np.ndarray:
        return samples


@dataclass(frozen=True)
class HardwareChain:
    """Runs hardware stages in order, enabling isolated model additions."""

    stages: tuple[HardwareModel, ...] = field(default_factory=tuple)

    def process(self, samples: np.ndarray, context: SignalContext) -> np.ndarray:
        for stage in self.stages:
            samples = stage.process(samples, context)
        return samples


@dataclass(frozen=True)
class TransmitterHardwareChain(HardwareChain):
    """Runs hardware stages that affect the waveform before the channel."""


@dataclass(frozen=True)
class ReceiverHardwareChain(HardwareChain):
    """Runs hardware stages that affect the waveform after the channel."""
