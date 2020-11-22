#ifndef CYTRON_SOFT_PWM_MD_H
#define CYTRON_SOFT_PWM_MD_H

#include <Arduino.h>
#include <stdint.h>



enum MODE {
  PWM_DIR,
  PWM_SWPM,
};



class SoftPwmMotorDriver
{
  public:
    SoftPwmMotorDriver(MODE mode, uint8_t pin1, uint8_t pin2, float maxMotorVoltage, float currentM);
    void setSpeed(int16_t speed);
    void setSpeed(int16_t speed, float currentInputVoltage);
    void setMaxMotorVoltage(float maxMotorVoltage);
    void setcurrentInputVoltage(float currentInputVoltage);

  protected:
    MODE _mode;
  	uint8_t _pin1;
    uint8_t _pin2;
    float _maxMotorVoltage;
    float _currentInputVoltage;
};

#endif