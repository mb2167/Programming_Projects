# metrics.py
import numpy as np
from dataclasses import dataclass


@dataclass(frozen=True)
class BerMeasurement:
    """BER outcome for one simulation point."""

    bit_errors: int
    total_bits: int

    @property
    def ber(
        self,
    ) -> float:
        return self.bit_errors / self.total_bits

    @property
    def zero_error_upper_bound_95(
        self,
    ) -> float | None:
        """Approximate 95% upper bound when no bit errors were observed."""
        if self.bit_errors == 0:
            return 3.0 / self.total_bits
        return None

# ------------------------------ POST-TRANSMISSION PROCESSING ------------------------------

# Calculate the error between the input bits and output bits
def calc_error(
    sent_bits: np.ndarray,
    received_bits: np.ndarray,
) -> BerMeasurement:
    
    if sent_bits.shape != received_bits.shape:
        raise ValueError("Sent and received bit arrays must have the same shape.")

    bit_errors = int(np.count_nonzero(sent_bits != received_bits))
    return BerMeasurement(bit_errors=bit_errors, total_bits=sent_bits.size)

