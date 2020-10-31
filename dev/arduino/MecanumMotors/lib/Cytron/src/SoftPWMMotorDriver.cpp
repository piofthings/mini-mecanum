#include "SoftPWMMotorDriver.h"
#include "SoftPWM.h"

CytronSoftPwmMD::CytronSoftPwmMD(MODE mode, uint8_t pin1, uint8_t pin2)
{
    _mode = mode;
    _pin1 = pin1;
    _pin2 = pin2;

    SoftPWMBegin();

    switch (_mode)
    {
    case PWM_DIR:
        pinMode(_pin1, OUTPUT);
        pinMode(_pin2, OUTPUT);
        digitalWrite(_pin1, LOW);
        digitalWrite(_pin2, LOW);
        break;
    case PWM_SWPM:
        pinMode(_pin1, OUTPUT);
        pinMode(_pin2, OUTPUT);
        SoftPWMSet(_pin1, LOW);
        SoftPWMSet(_pin2, LOW);
        break;
    default:
        break;
    }
}

void CytronSoftPwmMD::setSpeed(int16_t speed)
{
    // Make sure the speed is within the limit.
    if (speed > 255)
    {
        speed = 255;
    }
    else if (speed < -255)
    {
        speed = -255;
    }

    // Set the speed and direction.
    switch (_mode)
    {
    case PWM_DIR:
        if (speed >= 0)
        {
            analogWrite(_pin1, speed);
            digitalWrite(_pin2, LOW);
        }
        else
        {
            analogWrite(_pin1, -speed);
            digitalWrite(_pin2, HIGH);
        }
        break;

    case PWM_SWPM:
        if (speed >= 0)
        {
            SoftPWMSet(_pin1, speed);
            SoftPWMSet(_pin2, 0);
        }
        else
        {
            SoftPWMSet(_pin1, 0);
            SoftPWMSet(_pin2, -speed);
        }
        break;
    }
}