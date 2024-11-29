#include <Servo.h>

// from https://arduinogetstarted.com/tutorials/arduino-button-servo-motor

Servo servo;

void setup() {
  servo.attach(9);
}

void loop() {
  servo.write(0);
  delay(500);
  servo.write(90);
  delay(500);
  servo.write(180);
  delay(500);
  servo.write(90);
  delay(500);
  servo.write(0);
  delay(500);
}