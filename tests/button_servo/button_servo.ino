#include <Servo.h>

// from https://arduinogetstarted.com/tutorials/arduino-button-servo-motor

// constants
const int BUTTON_PIN = 7;
const int SERVO_PIN = 9;
Servo servo;

// variables
int angle = 0;
int lastButtonState;
int currentButtonState;

void setup() {
  Serial.begin(9600);                // initialize serial
  pinMode(BUTTON_PIN, INPUT_PULLUP); // set arduino pin to input pull-up mode
  servo.attach(SERVO_PIN);           // attaches the servo on pin 9 to the servo object

  servo.write(angle);
  currentButtonState = digitalRead(BUTTON_PIN);
}

void loop() {
  lastButtonState    = currentButtonState;      // save the last state
  currentButtonState = digitalRead(BUTTON_PIN); // read new state

  if(lastButtonState == HIGH && currentButtonState == LOW) {
    Serial.println("The button is pressed");

    // change angle of servo motor
    if(angle == 0)
      angle = 170;
    else
    if(angle == 170)
      angle = 0;

    // control servo motor arccoding to the angle
    servo.write(angle);
  }
}
