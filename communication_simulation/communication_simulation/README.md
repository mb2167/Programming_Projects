# Communication Simulation

A real-valued baseband BPSK simulation over an additive white Gaussian noise
(AWGN) channel.  It uses root-raised-cosine (RRC) transmit and matched receive
filters.

## Model assumptions

- Bits are mapped to BPSK symbols: `0 -> -1`, `1 -> +1`.
- Symbols and RRC taps are normalised to unit energy.
- Noise is calibrated using `Eb/N0`, not average sample power.
- The theoretical reference is `0.5 * erfc(sqrt(Eb/N0))`.
- This is a real baseband model; it does not currently include fading, carrier
  offset, timing error, coding, or multipath.

## Run

Install the dependencies and run:

```powershell
py -3.13 -m pip install -r requirements.txt
py -3.13 main.py
```

The configuration is in `config.py`.  Each run writes:

- `data/bpsk_ber_results.csv`: raw BER, bit-error count, and the number of bits.
- `data/bpsk_ber.png`: BER figure with the theoretical BPSK curve.

When a point has zero observed errors, its raw BER remains `0` in the CSV.  The
plot shows `3 / total_bits`, an approximate one-sided 95% upper bound, with a
downward-triangle marker.  This avoids treating zero as a measurable BER on a
logarithmic axis.

## Tests

Run the built-in test suite with:

```powershell
py -3.13 -m unittest discover -s tests -v
```


## TODO

- Fix AWGN scaling to use the actual transmitted bit energy (Eb).
- Validate that QPSK receives an even number of bits.
- Rename raised_cosine_receiver_filter() to rrc_filter().
- Replace the moving-average low-pass filter with a proper matched filter.
- Integrate the RRC pulse-shaping pipeline into the transmitter and receiver.
- Compensate for filter group delay before symbol decisions.
- Decouple the symbol rate from the carrier frequency.
- Remove or implement the currently unused parameters (alpha, sps, span).
- Refactor to reduce duplicated modulation/demodulation logic.
- Validate simulated BER against theoretical BPSK/QPSK BER curves.
- Test that BER is independent of oversampling and carrier settings.
