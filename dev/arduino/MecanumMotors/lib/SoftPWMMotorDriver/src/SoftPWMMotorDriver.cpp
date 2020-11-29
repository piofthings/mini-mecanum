#include "SoftPWMMotorDriver.h"
#include "SoftwarePWM.h"

SoftPwmMotorDriver::SoftPwmMotorDriver(MODE mode, uint8_t pin1, uint8_t pin2, float maxMotorVoltage, float currentInputVoltage)
{
    _mode = mode;
    _pin1 = pin1;
    _pin2 = pin2;
    _maxMotorVoltage = maxMotorVoltage;
    _currentInputVoltage = currentInputVoltage;

    SoftwarePWMBegin();

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
        SoftwarePWMSet(_pin1, LOW);
        SoftwarePWMSet(_pin2, LOW);
        break;
    default:
        break;
    }
}

void SoftPwmMotorDriver::setMaxMotorVoltage(float maxMotorVoltage)
{
    _maxMotorVoltage = maxMotorVoltage;
}

void SoftPwmMotorDriver::setcurrentInputVoltage(float currentInputVoltage)
{
    _currentInputVoltage = currentInputVoltage;
}

void SoftPwmMotorDriver::setSpeed(int16_t speed, float currentInputVoltage)
{
    setcurrentInputVoltage(currentInputVoltage);
    setSpeed(speed);
}

void SoftPwmMotorDriver::setSpeed(int16_t speed)
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

    float adj_speed = speed * (_maxMotorVoltage/_currentInputVoltage);
    // Serial.print("Adjusted Speed: ");
    // Serial.println(adj_speed);
    // Serial.println(speed);
    // Serial.println(_maxMotorVoltage);
    // Serial.println(_currentInputVoltage);
    // Set the speed and direction.
    switch (_mode)
    {
        case PWM_DIR:
            //Serial.print("PWM");
            if (speed >= 0)
            {
                analogWrite(_pin1, (int)adj_speed);
                digitalWrite(_pin2, LOW);
            }
            else
            {
                analogWrite(_pin1, (int)-adj_speed);
                digitalWrite(_pin2, HIGH);
            }
            break;

        case PWM_SWPM:
            //Serial.print("SWPWM");
            if (speed >= 0)
            {
                SoftwarePWMSet(_pin1, (int)(abs(adj_speed)));
                SoftwarePWMSet(_pin2, 0);
            }
            else
            {
                SoftwarePWMSet(_pin1, 0);
                SoftwarePWMSet(_pin2, (int)(abs(adj_speed)));
            }
            break;
    }
}