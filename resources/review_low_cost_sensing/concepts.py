"""This code will explore some of the main concepts in the low-cost sensing field."""

#%% Photoacoustic signal (synthetic data)
import numpy as np
import matplotlib.pyplot as plt


def photoacoustic_signal(t, A, f, tau):
    """Simulate a photoacoustic signal."""
    return A * np.exp(-t/tau) * np.sin(2*np.pi*f*t)

t = np.linspace(0, 10e-6, 1000) # time vector
A = 1 # amplitude
f = 5e6 # frequency
tau = 1e-6 # time constant

signal = photoacoustic_signal(t, A, f, tau)

plt.plot(t*1e6, signal)
plt.xlabel('Time (us)')
plt.ylabel('Amplitude')
plt.title('Photoacoustic signal')
plt.show()

#%% Signal Average and SNR improvement


def noisy_photoacoustic_signal(t, A, f, tau, noise_level):
    """Add noise to a photoacoustic signal."""
    clean_signal = photoacoustic_signal(t, A, f, tau)
    noise = np.random.normal(0, noise_level, len(t))
    return clean_signal + noise

noise_level = 0.2
averages = [1, 10, 100, 1000]

plt.figure(figsize=(12, 4))

for i, average in enumerate(averages):
    average_signal = np.zeros_like(t)
    for _ in range(average):
        average_signal += noisy_photoacoustic_signal(t, A, f, tau, noise_level)
    average_signal /= average

    plt.subplot(1, 4, i+1)
    plt.plot(t*1e6, average_signal)
    plt.xlabel('Time (us)')
    plt.ylabel('Amplitude')
    plt.title(f'Average {average} times')

#%%

import numpy as np
import matplotlib.pyplot as plt

def golay_pair(n):
    if n == 1:
        return [1], [1]
    else:
        a, b = golay_pair(n//2)
        return a + b, a + [-x for x in b]

def apply_code(signal, code):
    return np.convolve(signal, code, mode='same')

t = np.linspace(0, 100e-6, 1000)
signal = np.zeros_like(t)
signal[500] = 1  # Impulso único

code_a, code_b = golay_pair(8)

encoded_a = apply_code(signal, code_a)
encoded_b = apply_code(signal, code_b)

plt.figure(figsize=(12, 4))
plt.subplot(131)
plt.plot(t*1e6, signal)
plt.title('Señal Original')
plt.subplot(132)
plt.plot(t*1e6, encoded_a)
plt.title('Codificada con A')
plt.subplot(133)
plt.plot(t*1e6, encoded_b)
plt.title('Codificada con B')
plt.tight_layout()
plt.show()
