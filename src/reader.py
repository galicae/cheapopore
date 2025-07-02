#!/usr/bin/env python

# reading simple input from the Arduino serial

import time
import math
import pandas as pd

import serial

import asyncio
from playwright.async_api import async_playwright

def create_report(seq):
    # Ensure we have exactly 10 characters
    cells = list(seq[:10].ljust(10))

    # Create two rows from the characters
    row1 = cells[:10]

    # HTML table rows with inserted letters
    table_rows = f'''
    <tr>{''.join(f'<td>{char}</td>' for char in row1)}</tr>
    '''

    html_content = f'''
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            @page {{
                size: A4;
                margin: 2cm;
            }}

            body {{
                font-family: sans-serif;
                text-align: center;
            }}

            .header-row {{
                display: flex;
                justify-content: center;
                align-items: center;
                width: 20cm;
                margin: auto;
                margin-bottom: 0.1cm;
            }}

            .header-box {{
                width: 2cm;
                height: 1cm;
                border: 1px solid black;
                margin: 0 0.1cm;
            }}

            .header-title {{
                flex-grow: 1;
                font-size: 24px;
                font-weight: bold;
            }}

            .big-rectangle {{
                width: 20cm;
                height: 3cm;
                border: 1px solid black;
                margin: 0.1cm auto;
            }}

            table {{
                width: 20cm;
                border-collapse: collapse;
                margin: 0.2cm auto;
            }}

            th, td {{
                border: 1px solid black;
                width: 2cm;
                height: 1.5cm;
                text-align: center;
            }}

            .square {{
                width: 20cm;
                height: 18cm;
                border: 1px solid black;
                margin: 0.2cm auto;
            }}

            .small-table th, .small-table td {{
                width: 6.66cm;
                height: 1cm;
            }}
        </style>
    </head>
    <body>

        <div class="header-row">
            <div class="header-box"></div>
            <div class="header-title">Monstergenom</div>
            <div class="header-box"></div>
        </div>

        <div class="big-rectangle"></div>

        <table>
            <tr>
                <th>OCU1</th>
                <th>OCU2</th>
                <th>MEM1</th>
                <th>MEM2</th>
                <th>FRM1</th>
                <th>FRM2</th>
                <th>MAG1</th>
                <th>PAT10</th>
                <th>DWF7</th>
                <th>SPEC</th>
            </tr>
            {table_rows}
        </table>

        <div class="square"></div>

        <table class="small-table">
            <tr>
                <th>Forscher/in</th>
                <th>Schule</th>
                <th>Datum</th>
            </tr>
            <tr>
                <td></td><td></td><td></td>
            </tr>
        </table>

    </body>
    </html>
    '''
    return html_content

async def create_pdf(html_content):
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.set_content(html_content)
        await page.pdf(path="monstergenom.pdf", format="A4", print_background=True)
        await browser.close()


def read_write(arduino, val):
    # time.sleep(0.05)
    arduino.write(str(val).encode('UTF-8'))
    data = arduino.readline().decode('UTF-8')
    return data.split('\t')

def format(data, out):
    res = []
    past_leading_zeros = False
    # print("\tRED\tGREEN\tBLUE\tCLEAR")
    # print("\t-----------------------------------")
    for i, d in enumerate(data):
        if d == [''] and not past_leading_zeros:
            # print(f"{i}\t-\t-\t-\t-")
            continue
        elif d == [''] and past_leading_zeros:
            # print(f"{i}\t-\t-\t-\t-")
            res.append([0, 0, 0, 0])
        else:
            past_leading_zeros = True
            print(f"{i}\t{d[0]}\t{d[1]}\t{d[2]}\t{d[3].strip()}")
            res.append([int(num.strip()) for num in d])
    df = pd.DataFrame(res)
    df.columns = ['r', 'g', 'b', 'c']
    return df
    # df.to_csv(out, sep='\t')
    
def assign_base(row):
    # clear value > 1000 means yellow or green
    if row['c'] > 1000:
        if abs(row['g'] - row['r']) > 100: # green
        # if row['g'] > row['r']: # green
            return 'A'
        else: # yellow
            return 'G'
    else:
        if row['b'] > row['r']: # blue
            return 'C'
        else: # red
            return 'T'

def main():
    port = 'COM4'
    tmp = "C:\\Users\\nikol\\OneDrive\\Documents\\repos\\cheapopore\\tmp\\out.tsv"

    arduino = serial.Serial(port=port, baudrate=9600, timeout=.1)
    # frames = 10
    # cols = [read() for f in tqdm(range(frames))]

    # G: yellow, C: blue, A: green, T: red

    print("sequencing...")
    data = []
    for i in range(12):
        response = read_write(arduino, 1)
        data.append(response)
        time.sleep(0.5)

    # # stop reading
    response = read_write(arduino, 0)
    data.append(response)
    # # reset servo
    # time.sleep(1)
    read_write(arduino, 2)
    # print(data)
    
    clean = format(data, tmp)
    clean['base'] = clean.apply(assign_base, axis=1)
    sequence = ''.join(clean['base'].values)
    print(sequence)

    html_content = create_report(sequence)
    asyncio.run(create_pdf(html_content))
    
    

if __name__ == "__main__":
    main()

