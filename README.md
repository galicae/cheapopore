# cheapopore
Reverse-engineering the Brickopore sequencing project with Arduino and non-LEGO bricks.

<details>

<summary>Progress report</summary>

| date       | did      |
| ---------- | ------------- |
| 2024-11-22 | ordered parts off Amazon; cheapest servo I cound find, cheapest color detector I could find, and the cheapest arduino nano knock-off I could find. The goal is to see how low the budget can be. Parts arrived over the span of one week. |
| 2024-11-29 | soldered microcontroller |
| 2024-11-29 | simple servo tutorial from [project hub](https://projecthub.arduino.cc/arduino_uno_guy/the-beginners-guide-to-micro-servos-ae2a30). Implemented in [simple_servo.ino](./tests/simple_servo/simple_servo.ino). |
| 2024-11-29 | button servo tutorial from [arduinogetstarted](https://arduinogetstarted.com/tutorials/arduino-button-servo-motor). Implemented in [button_servo.ino](./tests/button_servo/button_servo.ino). |
| 2024-11-29 | adafruit TCS34725 tutorial from [makersguides](https://www.makerguides.com/tcs34725-rgb-color-sensor-with-arduino/). Implemented in [color_sensor.ino](./tests/color_sensor/color_sensor.ino). |
| 2024-11-30 | Combined [color_sensor.ino](./tests/color_sensor/color_sensor.ino) and [simple_server.py](./tests/simple_server.py) into the simplest possible input reader! |
| 2025-05 | went to local board game store and McGyver'ed a board. |
| 2025-06 | frantically trying to make a workable sequencer, so much that I forgot I wanted to document it. |
| 2025-06-25 | getting servo motor connected to gears is proving harder than I thought. Lots of hot glue are helping. I need to find a better solution for next time. |
| 2025-06-30 | experimenting with servo speed/time. Looks like I can catch single blocks. Might have to manually re-set gears. |
| 2025-07-01 | now reading one last time before reversing sled; this means that I can now read 10 blocks. |
| 2025-07-02 | using playwright to generate PDFs. |

</details>