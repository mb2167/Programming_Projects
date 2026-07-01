import numpy as np

# ------------------------------ PRE-TRANSMISSION SETUP ------------------------------

# Generate the bits to be processed using a shared RNG instance
def gen_bits(rng, size):
    return rng.integers(0, 2, size=size)


# Convert the bits into a BPSK signal
def bit_to_signal(bits):
    return (bits * 2) - 1


# ------------------------------ POST-TRANSMISSION PROCESSING ------------------------------

# Convert the signal back to bits
def signal_to_bit(signal):
    return np.where(signal < 0, 0, 1)