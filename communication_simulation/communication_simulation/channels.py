import numpy as np

# ------------------------------ TRANSMISSION ------------------------------

# Add AWGN noise to the signal
def add_noise(signal, snr_db, rng):
    P_signal = np.mean(signal * signal)
    snr_linear = 10 ** (snr_db / 10)
    P_noise = P_signal / snr_linear
    noise_std = np.sqrt(P_noise / 2)
    noise = rng.normal(0, noise_std, np.size(signal))
    return signal + noise