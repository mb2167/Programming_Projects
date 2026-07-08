# main.py
import numpy as np

from config import SimConfig
from simulation import communication_simulation
from plotting import plot_snr_v_ber, plot_signal


# ------------------------------ MAIN ------------------------------

def main():
    # Load configuration
    cfg = SimConfig()

    # Instantiate the RNG once here using the config seed
    rng = np.random.default_rng(cfg.SEED)
    
    snr_list = []
    ber_list = []

    # Iterate through the SNR range defined in config
    for snr_dB in cfg.snr_range:
        snr_list.append(snr_dB)
        ber_list.append(communication_simulation(rng, cfg.SIZE, snr_dB, cfg.ALPHA, cfg.SPS, cfg.FILTER_LENGTH))

    plot_snr_v_ber(snr_list, ber_list)


if __name__ == "__main__":
    main()