# config.py
from dataclasses import dataclass
import numpy as np

@dataclass(frozen=True)
class SimConfig:
    # Simulation Parameters
    SIZE: int = 100000
    SEED: int = 2
    
    # SNR Sweep Parameters
    SNR_MIN_DB: int = -10
    SNR_MAX_DB: int = 20
    
    @property
    def snr_range(self) -> np.ndarray:
        # Generates the array of SNR points to test
        return np.arange(self.SNR_MIN_DB, self.SNR_MAX_DB + 1)
    
    # Modulation Parameters
    SPS: int = 8 # Samples per symbol
    ALPHA: float = 0.35 # RRC roll-off factor (0 <-> 1)
    FILTER_LENGTH: int = 8 # Length of the RRC filter