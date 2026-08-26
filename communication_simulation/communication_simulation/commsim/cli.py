# main.py
import numpy as np

# Support both ``python -m commsim`` and VS Code's "Run Python File" action.
if __package__ in (None, ""):
    import sys
    from pathlib import Path

    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from commsim.config import SimConfig
    from commsim.plotting import plot_snr_v_ber
    from commsim.reporting import save_ber_results
    from commsim.simulation import communication_simulation
else:
    from .config import SimConfig
    from .plotting import plot_snr_v_ber
    from .reporting import save_ber_results
    from .simulation import communication_simulation

# ------------------------------ MAIN ------------------------------

def main():
    # Load configuration
    cfg = SimConfig()

    # Instantiate the RNG once here using the config seed
    rng = np.random.default_rng(cfg.SEED)
    
    measurements = []

    # Iterate through the SNR range defined in config
    for eb_n0_db in cfg.snr_range:
        measurement = communication_simulation(
            rng,
            cfg.SIZE,
            eb_n0_db,
            cfg.ALPHA,
            cfg.SPS,
            cfg.FILTER_LENGTH,
            cfg.MODULATION,
            sample_rate_hz=cfg.SAMPLING_FREQUENCY,
            carrier_frequency_hz=cfg.CARRIER_FREQUENCY,
        )
        measurements.append(measurement)
        print(
            f"Eb/N0 = {eb_n0_db:>3} dB: "
            f"{measurement.bit_errors} errors / {measurement.total_bits} bits "
            f"(BER = {measurement.ber:.3e})"
        )

    csv_path = cfg.OUTPUT_DIR / "bpsk_ber_results.csv"
    figure_path = cfg.OUTPUT_DIR / "bpsk_ber.png"
    save_ber_results(csv_path, cfg.snr_range, measurements)
    plot_snr_v_ber(cfg.snr_range, measurements, figure_path, cfg.SHOW_PLOT)
    print(f"Saved results to {csv_path}")
    print(f"Saved figure to {figure_path}")

if __name__ == "__main__":
    main()
