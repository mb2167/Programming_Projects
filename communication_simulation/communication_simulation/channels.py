# channels.py
import numpy as np

# ------------------------------ TRANSMISSION ------------------------------

def add_noise(
    signal: np.ndarray, eb_n0_db: float, rng: np.random.Generator
) -> np.ndarray:
    
    return add_AWGN_noise(signal, eb_n0_db, rng)

# Add AWGN noise to the signal
def add_AWGN_noise(
    signal: np.ndarray, eb_n0_db: float, rng: np.random.Generator
) -> np.ndarray:
    
    """Add real AWGN for unit-energy BPSK symbols at a given Eb/N0."""
    eb_n0_linear = 10 ** (eb_n0_db / 10)
    noise_std = np.sqrt(1 / (2 * eb_n0_linear))
    noise = rng.normal(0.0, noise_std, size=signal.shape)
    return signal + noise
