from modulation import gen_bits, bit_to_signal, signal_to_bit
from channels import add_noise
from metrics import calc_error


def communication_simulation(rng, size, snr_db):
    random_bits = gen_bits(rng, size)
    signal = bit_to_signal(random_bits)
    noisy_signal = add_noise(signal, snr_db, rng)
    received_bits = signal_to_bit(noisy_signal)
    error = calc_error(random_bits, received_bits)
    return error