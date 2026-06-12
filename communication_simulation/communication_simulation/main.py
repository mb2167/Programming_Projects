import numpy as np
import matplotlib.pyplot as plt

# ------------------------------ PRE-TRANSMISSION SETUP ------------------------------

# Generate the bits to be processed
def gen_bits(seed, size):
    # Random bit generation
    rng = np.random.default_rng(seed)
    return rng.integers(0, 2, size=size)

# Convert the bits into a wave signal
def bit_to_signal(array):
    return (array * 2) - 1


# ------------------------------ TRANSMISSION ------------------------------ 

# Add noise to the signal
def add_noise(array):
    mean = 0
    std = 0.5
    return (array + np.random.normal(mean, std, np.size(array)))


# ------------------------------ POST-TRANSMISSION PROCESSING ------------------------------ 
# Convert the signal to bits
def signal_to_bit(array):
    return np.where(array < 0, 0, 1) # If array value < 0, return 0, otherwise 1
    
# Calculate the error between the input bits and output bits
def calc_error(array1, array2):
    error = np.not_equal(array1, array2)
    return error.sum()/np.size(array1)

# ------------------------------ UTILITIES / DEBUGGING ------------------------------

# Visualise the noisy signal
def plot_signal(array):
    plt.plot(array)
    plt.ylim(-3,3)
    plt.xlim(0, np.size(array))
    plt.axhline(linestyle = "--", color = "red")
    plt.show()

# ------------------------------ MAIN ------------------------------

def main():
    size = 1000
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