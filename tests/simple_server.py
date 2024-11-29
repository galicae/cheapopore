#!/usr/bin/env python

# reading simple input from the Arduino serial

import serial
import time
from tqdm import tqdm

arduino = serial.Serial(port='COM6', baudrate=9600, timeout=.1)

def read():
    # time.sleep(0.05)
    data = arduino.readline().decode('UTF-8')
    return data.split('\t')

# frames = 10
# cols = [read() for f in tqdm(range(frames))]

# G: yellow, C: blue, A: green, T: red

while True:
    print(read())