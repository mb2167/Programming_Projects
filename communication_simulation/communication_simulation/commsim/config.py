# config.py
from dataclasses import dataclass
from pathlib import Path
import numpy as np


@dataclass(frozen=True)
class SimConfig:
    # Simulation Parameters
    MODULATION: str = "bpsk"
    SIZE: int = 1000000
    SEED: int = 2

    # SNR Sweep Parameters
    SNR_MIN_DB: int = -5
    SNR_MAX_DB: int = 15

    @property
    def snr_range(self) -> np.ndarray:
        # Generates the array of SNR points to test
        return np.arange(self.SNR_MIN_DB, self.SNR_MAX_DB + 1)

    # Modulation / Symbol Rate Parameters
    SYMBOL_RATE: float = 10.0e6  # 10 Msymbol/s
    SAMPLES_PER_SYMBOL: int = 8
    ALPHA: float = 0.35  # RRC roll-off factor (0 <-> 1)
    FILTER_LENGTH: int = 8  # Length of the RRC filter

    # Sampling Parameters
    SAMPLING_FREQUENCY: float = SYMBOL_RATE * SAMPLES_PER_SYMBOL

    # Carrier Wave Parameters
    CARRIER_FREQUENCY: float = 500.0e6  # 500 MHz

    # Output Parameters
    OUTPUT_DIR: Path = Path("data")
    SHOW_PLOT: bool = True

    # Phase & Frequency Offset Parameters
    TX_PHASE_OFFSET: float = 0.0  # Transmitter phase offset in radians
    RX_PHASE_OFFSET: float = 0.0  # Receiver phase offset in radians
    TX_FREQUENCY_OFFSET: float = 0.0  # Transmitter frequency offset in Hz
    RX_FREQUENCY_OFFSET: float = 0.0  # Receiver frequency offset in Hz

    TX_FREQUENCY = TX_FREQUENCY_OFFSET + CARRIER_FREQUENCY
    RX_FREQUENCY = RX_FREQUENCY_OFFSET + CARRIER_FREQUENCY

    # Costas Loop Parameters
    COSTAS_BANDWIDTH: float = 0.01 * SYMBOL_RATE  # Loop bandwidth as a fraction of the symbol rate
    COSTAS_DAMPING: float = 1 / np.sqrt(2)
    COSTAS_INITIAL_FREQUENCY: float = 0.0
    COSTAS_INITIAL_PHASE: float = 0.0
