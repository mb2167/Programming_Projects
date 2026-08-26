# config.py
from dataclasses import dataclass
from pathlib import Path
import numpy as np

@dataclass(frozen=True)
class SimConfig:
    # Simulation Parameters
    MODULATION: str = "qpsk"
    SIZE: int = 1000000
    SEED: int = 2
    
    # SNR Sweep Parameters
    SNR_MIN_DB: int = -5
    SNR_MAX_DB: int = 15
    
    @property
    def snr_range(
        self,
    ) -> np.ndarray:
        
        # Generates the array of SNR points to test
        return np.arange(self.SNR_MIN_DB, self.SNR_MAX_DB + 1)
    
    # Modulation Parameters
    SPS: int = 8 # Samples per symbol
    ALPHA: float = 0.35 # RRC roll-off factor (0 <-> 1)
    FILTER_LENGTH: int = 8 # Length of the RRC filter

    # Output Parameters
    OUTPUT_DIR: Path = Path("data")
    SHOW_PLOT: bool = True

    # Carrier Wave Parameters
    CARRIER_FREQUENCY: float = 500.0e6  # 500 MHz
    SAMPLES_PER_CARRIER: int = 8
    SAMPLING_FREQUENCY: int = CARRIER_FREQUENCY * SAMPLES_PER_CARRIER

