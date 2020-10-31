#ifndef CYTRON_SOFT_PWM_MD_H
#define CYTRON_SOFT_PWM_MD_H

#include <Arduino.h>
#include <stdint.h>



enum MODE {
  PWM_DIR,
  PWM_SWPM,
};



class CytronSoftPwmMD
{
  public:
    CytronSoftPwmMD(MODE mode, uint8_t pin1, uint8_t pin2);
    void setSpeed(int16_t speed);
    
  protected:
    MODE _mode;
  	uint8_t _pin1;
    uint8_t _pin2;
};

#endif