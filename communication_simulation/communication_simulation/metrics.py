import numpy as np

# ------------------------------ POST-TRANSMISSION PROCESSING ------------------------------

# Calculate the error between the input bits and output bits
def calc_error(sent_bits, received_bits):
    error = np.not_equal(sent_bits, received_bits)
    return error.sum() / np.size(sent_bits)