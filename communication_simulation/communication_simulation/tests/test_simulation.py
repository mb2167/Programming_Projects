import unittest
from pathlib import Path
import sys

import matplotlib.pyplot as plt
import numpy as np

# Add the project root so this file can be run directly from the tests folder
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import modulation.bpsk as bpsk
import modulation.pulse_shapes as pulse_shapes
import modulation.qpsk as qpsk
from metrics import BerMeasurement, calc_error
from simulation import communication_simulation


# ------------------------------ TESTS ------------------------------

class TestCommunicationSimulation(unittest.TestCase):
    # Test that BPSK modulation and demodulation returns the original bits
    def test_bpsk_round_trip_without_channel(
        self,
    ) -> None:
        bits = np.array([0, 1, 1, 0, 1])
        samples_per_carrier = 16
        carrier_frequency = 1_000.0
        sampling_frequency = carrier_frequency * samples_per_carrier

        signal = bpsk.modulate(
            bits,
            samples_per_carrier,
            carrier_frequency,
            sampling_frequency,
        )
        received_bits = bpsk.demodulate(
            signal,
            carrier_frequency,
            sampling_frequency,
            samples_per_carrier,
        )

        np.testing.assert_array_equal(received_bits, bits)

    # Test that each bit pair uses the documented QPSK phase mapping
    def test_qpsk_modulation_uses_expected_phase_mapping(
        self,
    ) -> None:
        
        bits = np.array([0, 0, 0, 1, 1, 0, 1, 1])

        signal = qpsk.modulate(
            bits,
            samples_per_carrier=2,
            carrier_frequency=0.0,
            sampling_frequency=1.0,
        )

        expected = np.repeat(np.cos(np.pi / 4 * np.array([1, 3, 7, 5])), 2)
        np.testing.assert_allclose(signal, expected)

    # Test QPSK demodulation and display the passband and mixed waveforms
    def test_qpsk_demodulation_round_trip_with_waveforms(
        self,
    ) -> None:
        bits = np.array([0, 0, 0, 1, 1, 0, 1, 1])
        samples_per_carrier = 16
        carrier_frequency = 1_000.0
        sampling_frequency = carrier_frequency * samples_per_carrier

        signal = qpsk.modulate(
            bits,
            samples_per_carrier,
            carrier_frequency,
            sampling_frequency,
        )
        received_bits = qpsk.demodulate(
        signal,
        carrier_frequency=carrier_frequency,
        sampling_frequency=sampling_frequency,
        samples_per_carrier=samples_per_carrier,
        )

        np.testing.assert_array_equal(received_bits, bits)

        time = np.arange(signal.size) / sampling_frequency
        carrier_phase = 2 * np.pi * carrier_frequency * time
        i_signal = signal * np.cos(carrier_phase)
        q_signal = -signal * np.sin(carrier_phase)

        fig, axes = plt.subplots(3, 1, sharex=True, figsize=(10, 7))
        axes[0].plot(time, signal)
        axes[0].set_title("QPSK signal")
        axes[0].set_ylabel("Amplitude")

        axes[1].plot(time, i_signal)
        axes[1].set_title("In-phase mixed signal")
        axes[1].set_ylabel("Amplitude")

        axes[2].plot(time, q_signal)
        axes[2].set_title("Quadrature mixed signal")
        axes[2].set_xlabel("Time (s)")
        axes[2].set_ylabel("Amplitude")

        fig.tight_layout()
        plt.show()
        plt.close(fig)

    # Test that the RRC filter is symmetrical and normalised to unit energy
    def test_rrc_taps_are_symmetric_and_unit_energy(
        self,
    ) -> None:
        
        taps = pulse_shapes.raised_cosine_receiver_filter(alpha=0.35, sps=8, span=8)
        np.testing.assert_allclose(taps, taps[::-1])
        self.assertAlmostEqual(float(np.sum(taps**2)), 1.0)

    # Test that a nearly noiseless channel produces no bit errors
    def test_noiseless_high_eb_n0_round_trip_has_no_errors(
        self,
    ) -> None:
        
        result = communication_simulation(
            np.random.default_rng(12), 1_000, 100.0, 0.35, 8, 8, "bpsk"
        )
        self.assertEqual(result.bit_errors, 0)
        self.assertEqual(result.ber, 0.0)

    # Test that simulated BER at 0 dB is close to the theoretical BPSK value
    def test_ber_near_theory_at_zero_db(
        self,
    ) -> None:
        
        result = communication_simulation(
            np.random.default_rng(3), 100_000, 0.0, 0.35, 8, 8, "bpsk"
        )
        self.assertAlmostEqual(result.ber, 0.07865, delta=0.01)

    # Test that a zero-error result has an upper bound for logarithmic plotting
    def test_zero_error_measurement_has_upper_bound(
        self,
    ) -> None:
        
        measurement = BerMeasurement(bit_errors=0, total_bits=100_000)
        self.assertEqual(measurement.zero_error_upper_bound_95, 3e-5)

    # Test that BER cannot be calculated from bit arrays of different lengths
    def test_metrics_reject_mismatched_array_shapes(
        self,
    ) -> None:
        
        with self.assertRaises(ValueError):
            calc_error(np.array([0, 1]), np.array([0]))


if __name__ == "__main__":
    unittest.main()
