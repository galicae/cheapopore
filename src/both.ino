#include <Wire.h>
#include <Servo.h>
#include "Adafruit_TCS34725.h"

// for a common anode LED, connect the common pin to +5V
// for common cathode, connect the common to ground

// set to false if using a common cathode LED
#define commonAnode true

// our RGB -> eye-recognized gamma color
byte gammatable[256];

// constants
Adafruit_TCS34725 tcs = Adafruit_TCS34725(TCS34725_INTEGRATIONTIME_50MS, TCS34725_GAIN_4X);
const int SERVO_PIN = 9;
Servo servo;

// variables
int sequencing = 0;
int angle = 0;

void setup() {
  Serial.begin(9600);
  // initialize servo motor
  servo.attach(SERVO_PIN); // attaches the servo on pin 9 to the servo object

  if (tcs.begin()) {
    // Serial.println("Found sensor");
  } else {
    Serial.println("No TCS34725 found ... check your connections");
    while (1); // halt!
  }

  // thanks PhilB for this gamma table!
  // it helps convert RGB colors to what humans see
  for (int i=0; i<256; i++) {
    float x = i;
    x /= 255;
    x = pow(x, 2.5);
    x *= 255;

    if (commonAnode) {
      gammatable[i] = 255 - x;
    } else {
      gammatable[i] = x;
    }
    //Serial.println(gammatable[i]);
  }
}

// The commented out code in loop is example of getRawData with clear value.
// Processing example colorview.pde can work with this kind of data too, but It requires manual conversion to 
// [0-255] RGB value. You can still uncomments parts of colorview.pde and play with clear value.
void loop() {
  float red, green, blue;
  if (Serial.available() > 0) {
    int val = char(Serial.read())-'0';
    if (val == 1) {
        tcs.setInterrupt(false);  // turn on LED

        delay(100);// takes 50ms to read

        tcs.getRGB(&red, &green, &blue);

        Serial.print(int(red)); 
        Serial.print("\t");
        Serial.print(int(green)); 
        Serial.print("\t");
        Serial.print(int(blue));

        // control servo motor arccoding to the angle
        servo.writeMicroseconds(1000);
        delay(310);
        servo.writeMicroseconds(1500);
    }

    if (val == 0) {
        Serial.write('OFF\n');
        tcs.setInterrupt(true);
    }

    if (val == 2) {
        Serial.write('OFF\n');
        tcs.setInterrupt(true);
        delay(1000);
        servo.writeMicroseconds(2000);
        delay(2700);
        servo.writeMicroseconds(1500);
    }
  }
}
