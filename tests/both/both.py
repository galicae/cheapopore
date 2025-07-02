#!/usr/bin/env python

# reading simple input from the Arduino serial

import time
import math

import serial
from tqdm import tqdm

import matplotlib.pyplot as plt
import numpy as np

def read_write(arduino, val):
    # time.sleep(0.05)
    arduino.write(str(val).encode('UTF-8'))
    data = arduino.readline().decode('UTF-8')
    print(data)
    return data.split('\t')

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
        int_datum = np.array([int(d.strip()) for d in datum])
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
        # print(i)
        response = read_write(arduino, 1)
        data.append(response)
        time.sleep(0.5)

    # print(data)

    # # stop reading
    response = read_write(arduino, 0)
    data.append(response)
    time.sleep(0.5)
    # reset servo
    # time.sleep(1)
    read_write(arduino, 2)

    # T = np.array([140, 55, 50]) # red
    # A = np.array([69, 113, 47]) # green
    # C = np.array([40, 75, 119]) # blue
    # G = np.array([103, 92, 34]) # yellow

if __name__ == "__main__":
    main()

