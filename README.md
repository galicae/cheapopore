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

</details>