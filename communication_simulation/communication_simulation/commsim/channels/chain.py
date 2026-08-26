"""Composition of propagation-channel stages."""

from dataclasses import dataclass, field

import numpy as np

from .base import ChannelContext, ChannelModel


@dataclass(frozen=True)
class IdentityChannel:
    """Passes samples through unchanged when no channel effect is required."""

    def process(self, samples: np.ndarray, context: ChannelContext) -> np.ndarray:
        """Return the input samples without applying an impairment."""
        return samples


@dataclass(frozen=True)
class ChannelChain:
    """Applies configured propagation-channel stages in sequence."""

    stages: tuple[ChannelModel, ...] = field(default_factory=tuple)

    def process(self, samples: np.ndarray, context: ChannelContext) -> np.ndarray:
        """Pass samples through every configured channel stage."""
        for stage in self.stages:
            samples = stage.process(samples, context)
        return samples
