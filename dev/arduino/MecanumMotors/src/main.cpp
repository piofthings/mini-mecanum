#include <Arduino.h>
#include <Wire.h>
#include "CytronMotorDriver.h"


// Configure the motor driver.
CytronMD motor1(PWM_DIR, 9, 8);   // PWM 1A = Pin 9, PWM 1B = Pin 8.
CytronMD motor2(PWM_DIR, 11, 12); // PWM 2A = Pin 10, PWM 2B = Pin 11.
CytronMD motor3(PWM_DIR, 5, 4);   // PWM 1A = Pin 5, PWM 1B = Pin 4.
CytronMD motor4(PWM_DIR, 3, 2); // PWM 2A = Pin 3, PWM 2B = Pin 2.

#define DIR_FORWARD 1;
#define DIR_REVERSE -1;

int currentSpeed = 0;
int currentDirection = DIR_FORWARD;
int currentTurnfactor = 

void testMotors() {
  motor1.setSpeed(64);    // Motor 1 runs forward at 50% speed.
  motor2.setSpeed(64);    // Motor 2 runs backward at 50% speed.
  motor3.setSpeed(64);    // Motor 1 runs forward at 50% speed.
  motor4.setSpeed(64);    // Motor 2 runs backward at 50% speed.
  delay(1000);

  motor1.setSpeed(128);   // Motor 1 runs forward at full speed.
  motor2.setSpeed(128);   // Motor 2 runs backward at full speed.
  motor3.setSpeed(128);   // Motor 1 runs forward at full speed.
  motor4.setSpeed(128);   // Motor 2 runs backward at full speed.
  delay(1000);

  motor1.setSpeed(0);     // Motor 1 stops.
  motor2.setSpeed(0);     // Motor 2 stops.
  motor3.setSpeed(0);     // Motor 1 runs forward at full speed.
  motor4.setSpeed(0);     // Motor 2 runs backward at full speed.
  delay(1000);

  motor1.setSpeed(-64);   // Motor 1 runs backward at 50% speed.
  motor2.setSpeed(-64);   // Motor 2 runs forward at 50% speed.
  motor3.setSpeed(-64);   // Motor 1 runs forward at full speed.
  motor4.setSpeed(-64);   // Motor 2 runs backward at full speed.
  delay(1000);

  motor1.setSpeed(-128);    // Motor 1 runs backward at full speed.
  motor2.setSpeed(-128);    // Motor 2 runs forward at full speed.
  motor3.setSpeed(-128);    // Motor 1 runs forward at full speed.
  motor4.setSpeed(-128);    // Motor 2 runs backward at full speed.
  delay(1000);

  motor1.setSpeed(0);     // Motor 1 stops.
  motor2.setSpeed(0);     // Motor 2 stops.
  motor3.setSpeed(0);     // Motor 1 runs forward at full speed.
  motor4.setSpeed(0);     // Motor 2 runs backward at full speed.
  delay(1000);
}

void setSpeed(int speed){
  motor1.setSpeed(speed*currentDirection);
  motor2.setSpeed(speed*currentDirection);
  motor3.setSpeed(speed*currentDirection);
  motor4.setSpeed(speed*currentDirection);
}

void setDirection(int direction){
  motor1.setSpeed(currentSpeed*direction);
  motor2.setSpeed(currentSpeed*direction);
  motor3.setSpeed(currentSpeed*direction);
  motor4.setSpeed(currentSpeed*direction);
  currentSpeed = direction;
}


void receiveEvent(int howMany) {
  if(howMany == 3){
    int offset = Wire.read(); // receive byte as a character
    int c = Wire.read();
    Serial.print("Command: ");
    Serial.println(c);
    switch (c)
    {
      case 1: // Set Speed
        int speed = Wire.read();
        setSpeed(speed);
        Serial.print("Speed: ");
        Serial.println(speed);
        break;
      case 2: // Set Direction
        int direction = Wire.read();
        Serial.print("Direction: ");
        Serial.println(direction);
        setDirection(direction);
        break;
      case 3: // Set Turnfactor
        break;
    }
  }
}

// The setup routine runs once when you press reset.
void setup() {
  Serial.begin(115200);
  Serial.println("Starting...");

  Wire.begin(0x8);
  Wire.onReceive(receiveEvent);
  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, LOW);
}



// The loop routine runs over and over again forever.
void loop() {
  //motorTest();
  delay(100);
}