#!/usr/bin/env python

# reading simple input from the Arduino serial

import time
import math

import serial
from tqdm import tqdm

import matplotlib.pyplot as plt
import numpy as np

from colormath.color_objects import sRGBColor, LabColor
from colormath.color_conversions import convert_color
from colormath.color_diff import delta_e_cie2000

def rgb_to_lab(r, g, b):
    """
    Converts an sRGB triplet (0-255) to CIELAB.

    Args:
        r (int): Red component (0-255).
        g (int): Green component (0-255).
        b (int): Blue component (0-255).

    Returns:
        LabColor: A colormath LabColor object.
    """
    # Create an sRGBColor object (colormath expects values 0-1 for sRGBColor)
    # The library handles the internal conversion from 0-255 to 0-1 if you pass them directly.
    srgb = sRGBColor(r, g, b, is_upscaled=True)
    
    # Convert sRGB to CIELAB
    lab = convert_color(srgb, LabColor)
    return lab

def calculate_color_probability(target_rgb, observed_rgb, sigma=5.0):
    """
    Calculates a likelihood score for how probable an observed RGB triplet
    represents a target RGB triplet, based on Delta E 2000 in CIELAB space.
    Higher score indicates higher probability/similarity.

    Args:
        target_rgb (tuple): A tuple (R, G, B) for the target color (0-255).
        observed_rgb (tuple): A tuple (R, G, B) for the observed color (0-255).
        sigma (float): The standard deviation for the Gaussian function.
                       Smaller sigma means only very close colors have high likelihood.
                       A good starting point is often 1 to 10.

    Returns:
        float: A likelihood score between 0 and 1 (approximately),
               where 1 indicates identical colors and 0 indicates very different.
    """
    # print(target_rgb, observed_rgb)
    target_lab = rgb_to_lab(target_rgb[0], target_rgb[1], target_rgb[2])
    observed_lab = rgb_to_lab(observed_rgb[0], observed_rgb[1], observed_rgb[2])
    # print(target_lab, observed_lab)

    # Calculate Delta E 2000
    # The result is a float representing the color difference.
    # A value < 1.0 is generally imperceptible to the human eye.
    # Values around 2.0-3.0 are just noticeable differences.
    delta_e = delta_e_cie2000(target_lab, observed_lab)

    # Convert Delta E to a likelihood score using a Gaussian-like function.
    # This maps smaller delta_e values to higher likelihoods.
    # The 'sigma' parameter controls the spread/sensitivity.
    # We use - (delta_e**2) / (2 * sigma**2) in the exponent.
    # When delta_e is 0, exp(0) = 1 (max likelihood).
    # As delta_e increases, the exponent becomes more negative, and exp() approaches 0.
    likelihood = float(f"{math.exp(-(delta_e**2) / (2 * sigma**2)):.6f}") # Format to 6 decimal places for cleaner output

    return likelihood, delta_e

def read_write(arduino, val):
    # time.sleep(0.05)
    arduino.write(str(val).encode('UTF-8'))
    data = arduino.readline().decode('UTF-8')
    print(data)
    return data.split('\t')


def calc_base_probability(data, sigma=5.0):
    # define normal distributions:
    T = np.array([140, 55, 50]) # red
    A = np.array([69, 113, 47]) # green
    C = np.array([40, 75, 119]) # blue
    G = np.array([103, 92, 34]) # yellow
    probs = np.zeros((4, len(data)))
    for i, _ in enumerate(data):
        likelihood, _ = calculate_color_probability(T, data[i], sigma=sigma)
        probs[0, i] = likelihood
        likelihood, _ = calculate_color_probability(A, data[i], sigma=sigma)
        probs[1, i] = likelihood
        likelihood, _ = calculate_color_probability(C, data[i], sigma=sigma)
        probs[2, i] = likelihood
        likelihood, _ = calculate_color_probability(G, data[i], sigma=sigma)
        probs[3, i] = likelihood
    return probs

# given an iterable of pairs return the key corresponding to the greatest value
def argmax(pairs):
    return max(pairs, key=lambda x: x[1])[0]

# given an iterable of values return the index of the greatest value
def argmax_index(values):
    return argmax(enumerate(values))

def consensus(probs):
    bases = np.array(['T', 'A', 'C', 'G'])
    indices = np.argmax(probs, axis=1)
    consensus = [bases[i] for i in indices]
    return ''.join(consensus)


def plot_sequencing(data):
    probs = calc_base_probability(data)
    # consensus_sequence = consensus(probs)
    fig, ax = plt.subplots()
    ax.plot(probs[0, :], c='red')
    ax.plot(probs[1, :], c='green')
    ax.plot(probs[2, :], c='blue')
    ax.plot(probs[3, :], c='gold')

    dna = {'T': 'red', 'A': 'green', 'C': 'blue', 'G': 'yellow'}

    # for i, s in enumerate(consensus_sequence):
    #     ax.text(i, 1.1, s, c=dna[s], size='large')
    ax.set_ylim(0.5, 1.2)
    plt.show(block=True)
    
def clean_data(data):
    clean = []
    started = False
    for datum in data:
        if datum == [''] and not started:
            continue
        elif datum == [''] and started:
            datum = [0, 0, 0]
        else:
            started = True
        int_datum = np.array([int(d) for d in datum])
        clean.append(int_datum)
    return np.array(clean)

def main():
    port = 'COM4'
    arduino = serial.Serial(port=port, baudrate=9600, timeout=.1)
    # frames = 10
    # cols = [read() for f in tqdm(range(frames))]

    # G: yellow, C: blue, A: green, T: red

    print("sequencing...")
    data = []
    for i in range(12):
        print(i)
        response = read_write(arduino, 1)
        data.append(response)
        time.sleep(0.5)

    print(data)

    # # stop reading
    read_write(arduino, 0)
    # # reset servo
    # time.sleep(1)
    read_write(arduino, 2)

    print(data)

    

if __name__ == "__main__":
    main()

