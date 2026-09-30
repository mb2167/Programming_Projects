# receiver.py
"""Receiver-side synchronization components."""

from dataclasses import dataclass

import numpy as np

from commsim.config import SimConfig as cfg


@dataclass
class CostasLoop:
    """Complex-baseband Costas carrier-recovery loop."""

    loop_bandwidth: float = cfg.COSTAS_BANDWIDTH
    damping_factor: float = cfg.COSTAS_DAMPING
    sampling_frequency: float = cfg.SAMPLING_FREQUENCY
    initial_frequency: float = cfg.COSTAS_INITIAL_FREQUENCY
    initial_phase: float = cfg.COSTAS_INITIAL_PHASE
    modulation: str = cfg.MODULATION

    def __post_init__(self) -> None:
        self.modulation = self.modulation.lower()

        if self.modulation not in {"bpsk", "qpsk"}:
            raise ValueError(
                f"Unsupported modulation: {self.modulation}. "
                "Expected 'bpsk' or 'qpsk'."
            )

        if self.sampling_frequency <= 0:
            raise ValueError("sampling_frequency must be positive.")

        if self.loop_bandwidth <= 0:
            raise ValueError("loop_bandwidth must be positive.")

        if self.damping_factor <= 0:
            raise ValueError("damping_factor must be positive.")

        # Runtime loop state.
        self.phase = float(self.initial_phase)
        self.frequency = float(self.initial_frequency)

        # Integral state of the second-order loop filter.
        self.integrator = 0.0

        # Most recent phase error.
        self.error = 0.0

        # Estimate of whether the loop is currently locked.
        self.locked = False

        # Calculate discrete-time loop-filter gains.
        self._calculate_loop_gains()

    def _calculate_loop_gains(self) -> None:
        """Calculate proportional and integral gains for the loop filter."""

        # Normalised loop bandwidth.
        #
        # The loop bandwidth is specified in Hz while the loop operates
        # at the sample rate.
        normalized_bandwidth = (self.loop_bandwidth / self.sampling_frequency)

        theta = normalized_bandwidth / (self.damping_factor + 0.25 / self.damping_factor)

        denominator = 1.0 + 2.0 * self.damping_factor * theta + theta**2

        self.proportional_gain = (4.0 * self.damping_factor * theta / denominator)

        self.integral_gain = (4.0 * theta**2 / denominator)

    def _phase_detector(self, samples: np.ndarray) -> np.ndarray:
        """Calculate the Costas-loop phase error."""

        i = samples.real
        q = samples.imag

        if self.modulation == "bpsk":
            # BPSK Costas phase detector.
            #
            # The sign of I removes the data modulation while Q
            # represents the residual quadrature component.
            return np.sign(i) * q

        # QPSK Costas phase detector.
        #
        # Both I and Q are used to remove the data modulation.
        return np.sign(i) * q - np.sign(q) * i

    def _update_loop(self, error: float) -> None:
        """Update the loop filter, frequency estimate and phase."""

        self.error = float(error)

        # Integral portion of the second-order loop filter.
        self.integrator += self.integral_gain * self.error

        # Frequency correction.
        correction = (self.proportional_gain * self.error + self.integrator)

        self.frequency += correction * self.sampling_frequency

        # Advance NCO phase by the estimated frequency.
        self.phase += (2.0 * np.pi * self.frequency / self.sampling_frequency)

        # Keep phase numerically bounded.
        self.phase = np.angle(np.exp(1j * self.phase))

    def process(self, samples: np.ndarray) -> np.ndarray:
        """
        Correct carrier phase and frequency offsets.

        Parameters
        ----------
        samples:
            Complex baseband receiver samples.

        Returns
        -------
        np.ndarray
            Carrier-corrected complex baseband samples.
        """

        samples = np.asarray(samples)

        if not np.iscomplexobj(samples):
            raise ValueError("CostasLoop expects complex baseband samples.")

        corrected = np.empty_like(samples, dtype=np.complex128)

        for n, sample in enumerate(samples):
            # Generate the current NCO correction.
            nco = np.exp(-1j * self.phase)

            # Remove the estimated carrier phase.
            mixed = sample * nco

            # Store the corrected sample.
            corrected[n] = mixed

            # Determine the residual carrier phase error.
            error = self._phase_detector(np.asarray([mixed]))[0]

            # Update the loop state ready for the next sample.
            self._update_loop(error)

        return corrected

    def reset(self) -> None:
        """Reset the loop to its configured initial state."""

        self.phase = float(self.initial_phase)
        self.frequency = float(self.initial_frequency)

        self.integrator = 0.0
        self.error = 0.0
        self.locked = False

    @property
    def phase_estimate(self) -> float:
        """Current carrier phase estimate in radians."""

        return self.phase

    @property
    def frequency_estimate(self) -> float:
        """Current carrier frequency estimate in Hz."""

        return self.frequency