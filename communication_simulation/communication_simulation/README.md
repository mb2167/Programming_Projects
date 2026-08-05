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

## Modular API (additive)

The original modules remain available unchanged for existing scripts. New work
can use the `commsim/` package, whose components are separated into modems,
channels, hardware stages, simulation orchestration, reporting, and plotting.
It provides an additive route for hardware models without changing the legacy
interfaces:

`bits -> modem -> TX hardware -> channel -> RX hardware -> decision -> BER`

Implement `HardwareModel.process(samples, context)` and attach it using
`HardwareChain` to model components such as DACs, ADCs, amplifiers, phase
noise, quantisation, or frequency offsets. Run its default experiment with
`py -3.13 -m commsim`.


## TODO

### High Priority

- [ ] Fix AWGN scaling so noise power is based on the transmitted bit energy (Eb) rather than assuming unit-energy symbols.
- [ ] Add validation that the QPSK input contains an even number of bits (or pad automatically).
- [ ] Rename `raised_cosine_receiver_filter()` to `root_raised_cosine_filter()` or `rrc_filter()`.

### Replace the Current Receiver

- [ ] Replace the moving-average `low_pass_filter()` with a proper receiver implementation.
- [ ] Decide whether to use:
  - [ ] Integrate-and-dump receiver (simpler).
  - [ ] Root Raised Cosine (RRC) matched filter (recommended).

### Integrate Pulse Shaping

- [ ] Remove the current rectangular pulse generation (`np.repeat(...)`) from the modulators.
- [ ] Map bits to BPSK/QPSK symbols before pulse shaping.
- [ ] Upsample the symbols.
- [ ] Apply the transmit RRC filter.
- [ ] Perform carrier modulation after pulse shaping.
- [ ] At the receiver:
  - [ ] Coherently mix down to baseband.
  - [ ] Apply the matched RRC filter.
  - [ ] Compensate for TX/RX filter group delay.
  - [ ] Downsample at the correct symbol instants.
  - [ ] Make symbol decisions.

### Improve the Simulation Model

- [ ] Separate the symbol rate from the carrier frequency so they are independent parameters.
- [ ] Compute `samples_per_symbol` from the symbol rate and sampling frequency instead of tying it to one carrier cycle.
- [ ] Verify that BER remains unchanged when changing the oversampling factor.

### Clean Up the Code

- [ ] Remove unused parameters (`alpha`, `sps`, `span`) until they are integrated into the pulse-shaping pipeline.
- [ ] Remove unused imports.
- [ ] Consider replacing the `match` statement with the `MODULATION_SCHEMES` dictionary to reduce duplicated code.

### Validation

- [ ] Compare the simulated BPSK BER against the theoretical BER curve.
- [ ] Compare the simulated Gray-coded QPSK BER against the theoretical BER curve.
- [ ] Verify that changing the carrier frequency, sampling frequency, samples per symbol, or RRC roll-off factor does not unexpectedly shift the BER curve.

### Optional Extensions

- [ ] Add carrier phase offset.
- [ ] Add carrier frequency offset.
- [ ] Add symbol timing offset.
- [ ] Add Rayleigh and Rician fading channels.
- [ ] Add higher-order modulation schemes (e.g. 16-QAM, 64-QAM).
- [ ] Add eye diagram and constellation plotting.
- [ ] Add unit tests for modulation, demodulation, and BER performance.
