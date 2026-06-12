import numpy as np
import matplotlib.pyplot as plt

# ------------------------------ PRE-TRANSMISSION SETUP ------------------------------

# Generate the bits to be processed
def gen_bits(seed, size):
    # Random bit generation
    rng = np.random.default_rng(seed)
    return rng.integers(0, 2, size=size)

# Convert the bits into a wave signal
def bit_to_signal(bits):
    return (bits * 2) - 1


# ------------------------------ TRANSMISSION ------------------------------ 

# Add noise to the signal
def add_noise(signal):
    snr_db = 1
    P_signal = np.mean((signal*signal))
    snr_linear = 10 ** (snr_db / 10)
    P_noise = P_signal / snr_linear
    noise_std = np.sqrt(P_noise)
    return signal + np.random.normal(0, noise_std, np.size(signal))


# ------------------------------ POST-TRANSMISSION PROCESSING ------------------------------ 
# Convert the signal to bits
def signal_to_bit(signal):
    return np.where(signal < 0, 0, 1) # If array value < 0, return 0, otherwise 1
    
# Calculate the error between the input bits and output bits
def calc_error(sent_bits, received_bits):
    error = np.not_equal(sent_bits, received_bits)
    return error.sum()/np.size(sent_bits)

# ------------------------------ UTILITIES / DEBUGGING ------------------------------

# Visualise the noisy signal
def plot_signal(signal):
    plt.plot(signal)
    plt.ylim(-3,3)
    plt.xlim(0, np.size(signal))
    plt.axhline(linestyle = "--", color = "red")
    plt.show()

# ------------------------------ MAIN ------------------------------

def main():
    size = 10000
    seed = 1 # Seed for randomness
    
    random_bits = gen_bits(seed, size)
    signal = bit_to_signal(random_bits)
    noisy_signal = add_noise(signal)
    plot_signal(noisy_signal)

    received_bits = signal_to_bit(noisy_signal)

    error = calc_error(random_bits,received_bits)

    print("Error:", error*100,"%")

if __name__ == "__main__":
    main()