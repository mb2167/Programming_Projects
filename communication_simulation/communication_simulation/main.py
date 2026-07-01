import numpy as np

from simulation import communication_simulation
from plotting import plot_snr_v_ber


# ------------------------------ MAIN ------------------------------

def main():
    size = 1000000
    seed = 2

    # Instantiate the RNG once here to avoid repeating bit sequences
    rng = np.random.default_rng(seed)

    snr_list = []
    ber_list = []

    for snr_dB in range(-10, 13):
        snr_list.append(snr_dB)
        ber_list.append(communication_simulation(rng, size, snr_dB))

    plot_snr_v_ber(snr_list, ber_list)


if __name__ == "__main__":
    main()