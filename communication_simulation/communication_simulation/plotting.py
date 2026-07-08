# plotting.py
import numpy as np
import matplotlib.pyplot as plt
from scipy.special import erfc

# ------------------------------ UTILITIES / DEBUGGING ------------------------------

# Visualise the noisy signal
def plot_signal(signal: np.ndarray):
    plt.figure(figsize=(10, 4))
    plt.plot(signal)
    plt.xlim(0, np.size(signal))
    plt.axhline(linestyle="--", color="red")
    plt.title("Signal Waveform (Time Domain)")
    plt.xlabel("Sample Index")
    plt.ylabel("Amplitude")
    plt.show()


# Plot SNR against BER and overlay theoretical performance
def plot_snr_v_ber(snr_list: np.ndarray, ber_list: np.ndarray):
    snr_array = np.array(snr_list)

    # Calculate Theoretical BER: 0.5 * erfc(sqrt(Eb/N0))
    snr_linear = 10 ** (snr_array / 10)
    theoretical_ber = 0.5 * erfc(np.sqrt(snr_linear))

    plt.figure(figsize=(8, 5))

    # Plot simulated results
    plt.semilogy(snr_array, ber_list, 'o-', label='Simulated BPSK')

    # Plot theoretical curve
    plt.semilogy(snr_array, theoretical_ber, 'r--', label='Theoretical BPSK')

    plt.xlabel("SNR ($E_b/N_0$) (dB)")
    plt.ylabel("Bit Error Rate (BER)")
    plt.title("BER Performance of BPSK over AWGN Channel")
    plt.grid(True, which="both", linestyle=":", alpha=0.5)
    plt.legend()
    plt.show()