"""Persistent output for reproducible simulation experiments."""

import csv
from pathlib import Path

import numpy as np

from .metrics import BerMeasurement


def save_ber_results(
    output_path: Path,
    eb_n0_db_values: np.ndarray,
    measurements: list[BerMeasurement],
) -> None:
    
    """Write raw BER results, retaining zero-error outcomes exactly."""
    if len(eb_n0_db_values) != len(measurements):
        raise ValueError("Each Eb/N0 value must have one BER measurement.")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(
            csv_file,
            fieldnames=(
                "eb_n0_db",
                "bit_errors",
                "total_bits",
                "ber",
                "zero_error_upper_bound_95",
            ),
        )
        writer.writeheader()
        for eb_n0_db, measurement in zip(eb_n0_db_values, measurements):
            writer.writerow(
                {
                    "eb_n0_db": eb_n0_db,
                    "bit_errors": measurement.bit_errors,
                    "total_bits": measurement.total_bits,
                    "ber": measurement.ber,
                    "zero_error_upper_bound_95": (
                        measurement.zero_error_upper_bound_95 or ""
                    ),
                }
            )

