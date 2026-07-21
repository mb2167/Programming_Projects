# modulation/pulse_shapes.py

import numpy as np

def symbol_upsample(
    symbols: np.ndarray,
    sps: int,
) -> np.ndarray:
    upsampled = np.zeros(len(symbols) * sps)
    upsampled[::sps] = symbols
    return upsampled

def signal_downsample(
    signal: np.ndarray,
    size: int,
    sps: int,
    span: int,
) -> np.ndarray:
    group_delay_samples = span * sps
    downsampled_signal = signal[group_delay_samples : group_delay_samples + (size * sps) : sps]
    
    return downsampled_signal

def raised_cosine_receiver_filter(
    alpha: float,
    sps: int,
    span: int,
) -> np.ndarray:
    # Generates a Root-Raised Cosine (RRC) filter impulse response.

    num_taps = span * sps + 1 # Number of taps (samples) in filter
    time_index_array = np.linspace(-span/2, span/2, num_taps)
    impulse_response = np.zeros(num_taps)

    # Case C constants calculations
    term1 = (1.0 + 2.0 / np.pi) * np.sin(np.pi / (4.0 * alpha))
    term2 = (1.0 - 2.0 / np.pi) * np.cos(np.pi / (4.0 * alpha))
    case_c_constant = (alpha / np.sqrt(2.0)) * (term1 + term2)
    
    for i, t in enumerate(time_index_array):
        if t == 0.0:
            # --- CASE B: The Center Peak ---
            impulse_response[i] = 1.0 - alpha + (4 * alpha / np.pi)
        
        elif alpha != 0 and np.isclose(np.abs(t), 1.0 / (4.0 * alpha)):
            # --- CASE C: The Intercept Points ---
            impulse_response[i] = case_c_constant

        else:
            # --- CASE A: The Standard Case ---
            numerator = np.sin(np.pi * t * (1.0 - alpha)) + 4.0 * alpha * t * np.cos(np.pi * t * (1.0 + alpha))
            denominator = np.pi * t * (1.0 - (4.0 * alpha * t) ** 2)
            impulse_response[i] = numerator / denominator
    
    impulse_response /= np.sqrt(np.sum(impulse_response**2))

    return impulse_response

def apply_tx_pulse_shaping(
    symbols: np.ndarray,
    alpha: float,
    sps: int,
    span: int,
) -> np.ndarray:
    
    upsampled_signals = symbol_upsample(symbols, sps)
    rrc_taps = raised_cosine_receiver_filter(alpha, sps, span)
    tx_signal = np.convolve(upsampled_signals, rrc_taps, mode='full')

    return tx_signal

def apply_rx_matched_filter(
    noisy_signal: np.ndarray,
    alpha: float,
    sps: int,
    span: int,
) -> np.ndarray:
    
    rrc_taps = raised_cosine_receiver_filter(alpha, sps, span)
    rx_filtered_signal = np.convolve(noisy_signal, rrc_taps, mode='full')

    return rx_filtered_signal


def low_pass_filter(
        unfiltered_signal: np.ndarray,
        samples_per_carrier: int
) -> np.ndarray:
    
    # Define the averaging window size
    window_size = samples_per_carrier // 2
    kernel = np.ones(window_size) / window_size

    filtered_signal = np.convolve(unfiltered_signal, kernel, mode='same')

    return filtered_signal