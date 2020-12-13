#include <Arduino.h>
#include <Adafruit_INA260.h>
#include "SoftPWMMotorDriver.h"
#include "main.h"

#define DIR_FORWARD 1;
#define DIR_REVERSE -1;

int currentSpeed = 0;
int currentDirection = DIR_FORWARD;
float max_voltage_mv = 6000.00;
float ina_input_voltage = 0;
float ina_input_current = 0;
float ina_input_power = 0;

// Configure the motor driver.
SoftPwmMotorDriver motor1Rf(PWM_SWPM, 16, 10, max_voltage_mv, 8400.0);   // PWM 1A = Pin 10, PWM 1B = Pin 16.
SoftPwmMotorDriver motor2Rr(PWM_SWPM, 9, 8, max_voltage_mv, 8400.0);     // PWM 2A = Pin 9, PWM 2B = Pin 8.
SoftPwmMotorDriver motor3Lf(PWM_SWPM, 4, 5, max_voltage_mv, 8400.0);     // PWM 1A = Pin 5, PWM 1B = Pin 4.
SoftPwmMotorDriver motor4Lr(PWM_SWPM, 6, 7, max_voltage_mv, 8400.0);     // PWM 2A = Pin 6, PWM 2B = Pin 7.


Adafruit_INA260 ina260 = Adafruit_INA260();

void testMotors() {
  // delay(5000);
  currentSpeed = -255;
  motor1Rf.setSpeed(currentSpeed, ina_input_voltage);   // Motor 1 runs forward at full speed.
  motor3Lf.setSpeed(currentSpeed, ina_input_voltage);   // Motor 1 runs forward at full speed.
  motor2Rr.setSpeed(currentSpeed, ina_input_voltage);   // Motor 2 runs backward at full speed.
  motor4Lr.setSpeed(currentSpeed, ina_input_voltage);   // Motor 2 runs backnward at full speed.
  readPower();
  writeSerialLog();
  delay(5000);

  currentSpeed = 0;
  motor1Rf.setSpeed(currentSpeed, ina_input_voltage);     // Motor 1 stops.
  motor3Lf.setSpeed(currentSpeed, ina_input_voltage);     // Motor 1 runs forward at full speed.
  motor2Rr.setSpeed(currentSpeed, ina_input_voltage);     // Motor 2 stops.
  motor4Lr.setSpeed(currentSpeed, ina_input_voltage);     // Motor 2 runs backward at full speed.
  readPower();
  writeSerialLog();
  delay(5000);

  currentSpeed = 255;
  motor1Rf.setSpeed(currentSpeed, ina_input_voltage);    // Motor 1 runs backward at full speed.
  motor3Lf.setSpeed(currentSpeed, ina_input_voltage);    // Motor 1 runs forward at full speed.
  motor2Rr.setSpeed(currentSpeed, ina_input_voltage);    // Motor 2 runs forward at full speed.
  motor4Lr.setSpeed(currentSpeed, ina_input_voltage);    // Motor 2 runs backward at full speed.
  readPower();
  writeSerialLog();
  delay(5000);

  currentSpeed = 0;
  motor1Rf.setSpeed(currentSpeed, ina_input_voltage);     // Motor 1 stops.
  motor3Lf.setSpeed(currentSpeed, ina_input_voltage);     // Motor 1 runs forward at full speed.
  motor2Rr.setSpeed(currentSpeed, ina_input_voltage);     // Motor 2 stops.
  motor4Lr.setSpeed(currentSpeed, ina_input_voltage);     // Motor 2 runs backward at full speed.
  readPower();
  writeSerialLog();
  delay(5000);
}


void setSpeed(int speed){
  currentSpeed = speed;
  motor1Rf.setSpeed(currentSpeed * currentDirection, ina_input_voltage);
  motor3Lf.setSpeed(currentSpeed * currentDirection, ina_input_voltage);
  motor2Rr.setSpeed(currentSpeed * currentDirection, ina_input_voltage);
  motor4Lr.setSpeed(currentSpeed * currentDirection, ina_input_voltage);
}

void setLRSpeed(int speedLeft, int speedRight){
  motor1Rf.setSpeed(speedRight, ina_input_voltage);
  motor2Rr.setSpeed(speedRight, ina_input_voltage);
  motor3Lf.setSpeed(speedLeft, ina_input_voltage);
  motor4Lr.setSpeed(speedLeft, ina_input_voltage);
}

void setLfLrRfRrSpeed(int speedLeftFront, int speedLeftRear, int speedRightFront, int speedRightRear){
  motor1Rf.setSpeed(speedRightFront, ina_input_voltage);
  motor2Rr.setSpeed(speedRightRear, ina_input_voltage);
  motor3Lf.setSpeed(speedLeftFront, ina_input_voltage);
  motor4Lr.setSpeed(speedLeftRear, ina_input_voltage);
}

void setDirection(int direction){
  currentDirection = direction;
  setSpeed(currentSpeed);
}

String getValue(String data, char separator, int index)
{
  int found = 0;
  int strIndex[] = {0, -1};
  int maxIndex = data.length()-1;

  for(int i=0; i<=maxIndex && found<=index; i++){
    if(data.charAt(i)==separator || i==maxIndex){
        found++;
        strIndex[0] = strIndex[1]+1;
        strIndex[1] = (i == maxIndex) ? i+1 : i;
    }
  }

  return found>index ? data.substring(strIndex[0], strIndex[1]) : "";
}

void receiveEvent() {
  if (Serial1.available() > 0) {
    digitalWrite(LED_BUILTIN, HIGH);   // turn the LED on (HIGH is the voltage level)

    String cInput = Serial1.readStringUntil('\n');
    Serial.println(cInput);
    String c = getValue(cInput, ':', 0);
    String speeds = getValue(cInput, ':', 1);
    int command = c.toInt();
 
    Serial.print("\nCommand: ");
    Serial.println(command);
    Serial.println(speeds);

    switch (command)
    {
      case 1: // Set Speed
      {
        String s = Serial1.readStringUntil('\n');
        int speed = s.toInt();
        setSpeed(speed);
        Serial.print("\nSpeed: ");
        Serial.println(speed);
        break;
      }
      case 2: // Set Direction
      {
        String d = Serial.readStringUntil('\n');
        int direction = d.toInt();
        Serial.print("\nDirection: ");
        Serial.println(d);
        setDirection(direction);
        break;
      }
      case 3: // Set L-R Speed
      {
        Serial.println("Case 3");
        String sl = getValue(speeds, ',', 0);
        int speedLeft = sl.toInt();
        String sr = getValue(speeds, ',', 1);
        int speedRight = sr.toInt();
        setLRSpeed(speedLeft, speedRight);
        Serial.print("\nSpeed Set: ");
        Serial.print(speedLeft);
        Serial.print(", ");
        Serial.println(speedRight);
        break;
      }
      case 4: // Set Lf-Lr-Rf-Rr Speed
      {
        String slf = getValue(speeds, ',', 0);
        int speedLeftFront = slf.toInt();
        String slr = SgetValue(speeds, ',', 1);
        int speedLeftRight = slr.toInt();
        String srf = getValue(speeds, ',', 2);
        int speedRightFront = srf.toInt();
        String srr = getValue(speeds, ',', 4);;
        int speedRightRear = srr.toInt();
        setLfLrRfRrSpeed(slf,slr,srf,srr);
        break;
      }
      case 5: // Get Last Power readings
      {
          Serial1.print(ina_input_current);  
          Serial1.print(", ");  
          Serial1.print(ina_input_voltage);  
          Serial1.print(", ");  
          Serial1.print(ina_input_power);  
          Serial1.print(", ");
          Serial1.println(currentSpeed);  
        break;
      }
    }
  }
  digitalWrite(LED_BUILTIN, LOW);

}

// The setup routine runs once when you press reset.
void setup() {
  pinMode(LED_BUILTIN, OUTPUT);
  Serial1.begin(115200);
  Serial1.println("Starting...");
  if (!ina260.begin()) 
  {    
    Serial.println("Couldn't find INA260 chip");    
    //while (1);  
  }
  Serial.print("Current (mA), ");  
  Serial.print("Bus Voltage (mV), ");  
  Serial.print("Power (mW), ");  
  Serial.print("Current Speed (PWM), ");  
  Serial.println("");
    //testMotors();
}



// The loop routine runs over and over again forever.
void loop() {
  readPower();
  //testMotors();
  //writeSerialLog();
  receiveEvent();
}

void readPower() {
  ina_input_voltage = ina260.readBusVoltage();
  ina_input_current = ina260.readCurrent();
  ina_input_power = ina260.readPower();
}

void writeSerialLog() {
  Serial.print(ina_input_current);  
  Serial.print(", ");  
  Serial.print(ina_input_voltage);  
  Serial.print(", ");  
  Serial.print(ina_input_power);  
  Serial.print(", ");
  Serial.println(currentSpeed);  
}