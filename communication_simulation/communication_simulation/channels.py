# channels.py
import numpy as np

# ------------------------------ TRANSMISSION ------------------------------

def add_noise(signal: np.ndarray, snr_db: int, rng: int):
    return add_AWGN_noise(signal, snr_db, rng)

# Add AWGN noise to the signal
def add_AWGN_noise(signal: np.ndarray, snr_db: int, rng: int):
    P_signal = np.mean(signal * signal)
    snr_linear = 10 ** (snr_db / 10)
    P_noise = P_signal / snr_linear
    noise_std = np.sqrt(P_noise)
    noise = rng.normal(0, noise_std, np.size(signal))
    return signal + noise