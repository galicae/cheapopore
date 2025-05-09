#!/usr/bin/env python

# reading simple input from the Arduino serial

import time

import serial
from tqdm import tqdm

import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm

def read_write(arduino, val):
    # time.sleep(0.05)
    arduino.write(str(val).encode('UTF-8'))
    data = arduino.readline().decode('UTF-8')
    print(data)
    return data.split('\t')

def convert_to_numbers(data, col):
    numbers = [0] * len(data)
    for i, s in enumerate(data):
        if len(s) == 1:
            numbers[i] = 0
        else:
            numbers[i] = int(s[col])
    return numbers

def read_rgb(data):
    red = convert_to_numbers(data, 0)
    green = convert_to_numbers(data, 1)
    blue = convert_to_numbers(data, 2)
    return np.array([red, green, blue])

def probability(col1, col2, norm=150**2 * 3):
    rd = (col1[0] - col2[0])**2
    bd = (col1[1] - col2[1])**2
    gd = (col1[2] - col2[2])**2
    return 1 - (rd + bd + gd) / norm


def calc_base_probability(raw,):
    # define normal distributions:
    T=[170, 40, 40], # red
    A=[70, 120, 35], # green
    C=[30, 90, 110], # blue
    G=[100, 90, 30] # yellow
    data = read_rgb(raw)
    probs = np.zeros((4, len(raw)))
    for i, _ in enumerate(data):
        probs[0, i] = probability(data[:, i], T)
        probs[1, i] = probability(data[:, i], A)
        probs[2, i] = probability(data[:, i], C)
        probs[3, i] = probability(data[:, i], G)
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
    print(probs)
    print(indices)
    return res


def plot_sequencing(data):
    probs = calc_base_probability(data)
    consensus_sequence = consensus(probs)
    fig, ax = plt.subplots()
    ax.plot(t_prob, c='red')
    ax.plot(a_prob, c='green')
    ax.plot(c_prob, c='blue')
    ax.plot(g_prob, c='gold')

    dna = {'T': 'red', 'A': 'green', 'C': 'blue', 'G': 'yellow'}

    for i, s in enumerate(consensus_sequence):
        ax.text(i, 1.1, s, c=dna[s], size='large')
    ax.set_ylim(0.5, 1.2)
    plt.show(block=True)
    

def main():
    port = 'COM3'
    arduino = serial.Serial(port=port, baudrate=9600, timeout=.1)
    # frames = 10
    # cols = [read() for f in tqdm(range(frames))]

    # G: yellow, C: blue, A: green, T: red

    t_end = time.time() + 10
    print("sequencing...")
    data = []
    # while time.time() < t_end:
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

    plot_sequencing(data)

    

if __name__ == "__main__":
    main()

