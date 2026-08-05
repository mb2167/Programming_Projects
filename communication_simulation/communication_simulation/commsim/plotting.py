# plotting.py
import numpy as np
import matplotlib.pyplot as plt
from scipy.special import erfc
from .metrics import BerMeasurement
from pathlib import Path

# ------------------------------ UTILITIES / DEBUGGING ------------------------------

# Visualise the noisy signal
def plot_signal(
    signal: np.ndarray,
) -> None:
    
    plt.figure(figsize=(10, 4))
    plt.plot(signal)
    plt.xlim(0, np.size(signal))
    plt.axhline(linestyle="--", color="red")
    plt.title("Signal Waveform (Time Domain)")
    plt.xlabel("Sample Index")
    plt.ylabel("Amplitude")
    plt.show()


# Plot SNR against BER and overlay theoretical performance
def plot_snr_v_ber(
    eb_n0_db_values: np.ndarray,
    measurements: list[BerMeasurement],
    output_path: Path | None = None,
    show: bool = True,
) -> None:
    
    snr_array = np.asarray(eb_n0_db_values)
    ber_array = np.array([measurement.ber for measurement in measurements])
    zero_error_mask = ber_array == 0

    # A zero BER cannot be plotted logarithmically.  Use a clearly labelled
    # 95% upper bound for display, while preserving the true zero in the CSV.
    plot_ber = np.array([
        measurement.ber
        if measurement.ber > 0
        else measurement.zero_error_upper_bound_95
        for measurement in measurements
    ])

    # Calculate Theoretical BER: 0.5 * erfc(sqrt(Eb/N0))
    snr_linear = 10 ** (snr_array / 10)
    theoretical_ber = 0.5 * erfc(np.sqrt(snr_linear))

    plt.figure(figsize=(8, 5))

    # Plot simulated results
    plt.semilogy(snr_array, plot_ber, 'o-', label='Simulated BPSK')
    if np.any(zero_error_mask):
        plt.semilogy(
            snr_array[zero_error_mask],
            plot_ber[zero_error_mask],
            'v',
            label='Zero errors observed (95% upper bound)',
        )

    # Plot theoretical curve
    plt.semilogy(snr_array, theoretical_ber, 'r--', label='Theoretical BPSK')

    plt.xlabel("$E_b/N_0$ (dB)")
    plt.ylabel("Bit Error Rate (BER)")
    plt.title("BER Performance of BPSK over AWGN Channel")
    plt.grid(True, which="both", linestyle=":", alpha=0.5)
    plt.legend()
    plt.tight_layout()
    if output_path is not None:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(output_path, dpi=200)
    if show:
        plt.show()
    plt.close()

