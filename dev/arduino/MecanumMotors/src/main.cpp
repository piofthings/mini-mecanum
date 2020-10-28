#include <Arduino.h>
#include "CytronMotorDriver.h"
#include "main.h"

// Configure the motor driver.
CytronMD motor1(PWM_DIR, 10, 16);   // PWM 1A = Pin 10, PWM 1B = Pin 16.
CytronMD motor2(PWM_DIR, 9, 8);     // PWM 2A = Pin 9, PWM 2B = Pin 8.
CytronMD motor3(PWM_DIR, 5, 4);     // PWM 1A = Pin 5, PWM 1B = Pin 4.
CytronMD motor4(PWM_DIR, 6, 7);     // PWM 2A = Pin 6, PWM 2B = Pin 7.

#define DIR_FORWARD 1;
#define DIR_REVERSE -1;

int currentSpeed = 0;
int currentDirection = DIR_FORWARD;


void testMotors() {
  motor1.setSpeed(64);    // Motor 1 runs forward at 50% speed.
  motor2.setSpeed(64);    // Motor 2 runs backward at 50% speed.
  motor3.setSpeed(64);    // Motor 1 runs forward at 50% speed.
  motor4.setSpeed(64);    // Motor 2 runs backward at 50% speed.
  delay(1000);

  motor1.setSpeed(128);   // Motor 1 runs forward at full speed.
  motor2.setSpeed(128);   // Motor 2 runs backward at full speed.
  motor3.setSpeed(128);   // Motor 1 runs forward at full speed.
  motor4.setSpeed(128);   // Motor 2 runs backnward at full speed.
  delay(1000);

  motor1.setSpeed(0);     // Motor 1 stops.
  motor2.setSpeed(0);     // Motor 2 stops.
  motor3.setSpeed(0);     // Motor 1 runs forward at full speed.
he  motor4.setSpeed(0);     // Motor 2 runs backward at full speed.
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
  currentSpeed = speed;
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
  currentDirection = direction;
}


void receiveEvent() {
  if (Serial1.available() > 0) {
    digitalWrite(LED_BUILTIN, HIGH);   // turn the LED on (HIGH is the voltage level)

    String c = Serial1.readStringUntil(':');
    int command = c.toInt();
 
    Serial1.print("Command: ");
    Serial1.println(c);

    switch (command)
    {
      case 1: // Set Speed
        String s = Serial1.readStringUntil('\n');
        int speed = s.toInt();
        setSpeed(speed);
        Serial1.print("Speed: ");
        Serial1.println(speed);
        break;
      case 2: // Set Direction
        String d = Serial1.readStringUntil('\n');
        int direction = d.toInt();
        Serial1.print("Direction: ");
        Serial1.println(d);
        setDirection(direction);
        break;
      case 3: // Set Turnfactor
        break;
    }
  }
  digitalWrite(LED_BUILTIN, LOW);

}

// The setup routine runs once when you press reset.
void setup() {
  pinMode(LED_BUILTIN, OUTPUT);
  Serial1.begin(115200);
  Serial1.println("Starting...");

  //testMotors()
}



// The loop routine runs over and over again forever.
void loop() {
  //testMotors();
  receiveEvent();
}