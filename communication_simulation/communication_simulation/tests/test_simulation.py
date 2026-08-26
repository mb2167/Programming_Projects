import unittest
from pathlib import Path
import sys

import numpy as np

# Add the project root so this file can be run directly from the tests folder
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import commsim.modulation.bpsk as bpsk
import commsim.modulation.pulse_shapes as pulse_shapes
import commsim.modulation.qpsk as qpsk
from commsim.metrics import BerMeasurement, calc_error
from commsim.simulation import communication_simulation
from commsim.hardware import ReceiverHardwareChain, TransmitterHardwareChain
from commsim.modulation import (
    BPSKDemodulator,
    BPSKModulator,
    DemodulationChain,
    DemodulationContext,
    ModulationChain,
    ModulationContext,
)


# ------------------------------ TESTS ------------------------------

class TestCommunicationSimulation(unittest.TestCase):
    # Test that BPSK modulation and demodulation returns the original bits
    def test_bpsk_round_trip_without_channel(
        self,
    ) -> None:
        bits = np.array([0, 1, 1, 0, 1])

        signal = bpsk.modulate(
            bits,
            alpha=0.35,
            sps=16,
            span=8,
        )
        received_bits = bpsk.demodulate(
            signal,
            symbol_count=bits.size,
            alpha=0.35,
            sps=16,
            span=8,
        )

        np.testing.assert_array_equal(received_bits, bits)

    # Test QPSK transmit/receive RRC filtering and hard decisions
    def test_qpsk_rrc_round_trip_without_channel(self) -> None:
        bits = np.array([0, 0, 0, 1, 1, 0, 1, 1])
        samples_per_carrier = 16
        carrier_frequency = 1_000.0
        sampling_frequency = carrier_frequency * samples_per_carrier

        signal = qpsk.modulate(
            bits,
            alpha=0.35,
            sps=samples_per_carrier,
            span=8,
        )
        received_bits = qpsk.demodulate(
            signal,
            symbol_count=bits.size // 2,
            alpha=0.35,
            sps=samples_per_carrier,
            span=8,
        )

        np.testing.assert_array_equal(received_bits, bits)

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

    def test_qpsk_ber_near_theory_at_zero_db(self) -> None:
        result = communication_simulation(
            np.random.default_rng(3), 100_000, 0.0, 0.35, 8, 8, "qpsk"
        )
        self.assertAlmostEqual(result.ber, 0.07865, delta=0.01)

    # Test that modulation and demodulation chains use their configured stages.
    def test_modulation_and_demodulation_chains(self) -> None:
        bits = np.array([0, 1, 1, 0])
        modulation_chain = ModulationChain((BPSKModulator(),))
        signal = modulation_chain.process(bits, ModulationContext(alpha=0.35, sps=8, span=8))
        demodulation_chain = DemodulationChain((BPSKDemodulator(),))
        received_bits = demodulation_chain.process(
            signal,
            DemodulationContext(symbol_count=bits.size, alpha=0.35, sps=8, span=8),
        )
        np.testing.assert_array_equal(received_bits, bits)

    # Test that separate transmit and receive hardware stages run in order.
    def test_transmit_and_receive_hardware_chains_are_separate(self) -> None:
        calls: list[str] = []

        class RecordTransmitter:
            def process(self, samples: np.ndarray, context: object) -> np.ndarray:
                calls.append("transmitter")
                return samples

        class RecordReceiver:
            def process(self, samples: np.ndarray, context: object) -> np.ndarray:
                calls.append("receiver")
                return samples

        communication_simulation(
            np.random.default_rng(12),
            100,
            100.0,
            0.35,
            8,
            8,
            "bpsk",
            transmitter_hardware=TransmitterHardwareChain((RecordTransmitter(),)),
            receiver_hardware=ReceiverHardwareChain((RecordReceiver(),)),
        )
        self.assertEqual(calls, ["transmitter", "receiver"])

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
