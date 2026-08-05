# channels.py
import numpy as np

# ------------------------------ TRANSMISSION ------------------------------

def add_noise(
    signal: np.ndarray,
    eb_n0_db: float,
    rng: np.random.Generator,
    bits_per_symbol: int = 1,
) -> np.ndarray:
    return add_AWGN_noise(signal, eb_n0_db, rng, bits_per_symbol)

# Add AWGN noise to the signal
def add_AWGN_noise(
    signal: np.ndarray,
    eb_n0_db: float,
    rng: np.random.Generator,
    bits_per_symbol: int = 1,
) -> np.ndarray:
    """Add AWGN to unit-energy real or complex symbols at a given Eb/N0."""
    if bits_per_symbol <= 0:
        raise ValueError("bits_per_symbol must be positive.")
    eb_n0_linear = 10 ** (eb_n0_db / 10)
    noise_std = np.sqrt(1 / (2 * bits_per_symbol * eb_n0_linear))
    noise = rng.normal(0.0, noise_std, size=signal.shape)
    if np.iscomplexobj(signal):
        noise = noise + 1j * rng.normal(0.0, noise_std, size=signal.shape)
    return signal + noise
