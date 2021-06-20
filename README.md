# mini-mecanum

Mini Mecanum bot goes to [PiWars at Home 2021](https://piwars.org)

Yes, we couldn't resist and put our names in for [PiWars at Home 2021](https://piwars.org) and now we are in deep trouble.

# Motor Driver using GPIOZero
We are using 2xMDD3A Cytron motor drivers to drive 4 motors independently so we can strafe when we use Mecanum motors. The drivers use PWM signal for forward and backward directions instead of using a PWM and Direction pin.

Looks like the `GPIO Zero` libraries' `Motor` abstraction will work with this driver. So we are using the following Pins on the Pi


| #    | Pin                   | Used                      |          | Wire colour |
| :--- | --------------------- | :------------------------ | :------- | :---------- |
| 1.   | GPIO 17 (Physical 11) | Left Front                | Forward  | Yellow      |
| 2.   | GPIO 27 (Physical 13) | Left Front                | Backward | Blue        |
| 3.   | GPIO 23 (Phyiscal 16) | Left Rear                 | Forward  | Yellow      |
| 4.   | GPIO 24 (Physical 18) | Left Rear                 | Backward | Blue        |
| 5.   | GPIO 5 (Phyiscal 29)  | Right Front               | Forward  | Yellow      |
| 6.   | GPIO 6 (Physical 31)  | Right Front               | Backward | Blue        |
| 7.   | GPIO 26 (Phyiscal 37) | Right Rear                | Forward  | Yellow      |
| 8.   | GPIO 16 (Phyiscal 36) | Right Rear                | Backward | Blue        |
| 9.   | GPIO 2 (Physical 3)   | I2C SDA                   |          |             |
| 10.  | GPIO 3 (Physical 5)   | I2C SCL                   |          |             |
| 11.  | GPIO 22 (Physical 15) | S (Fish feeder Servo)     |          |             |
| 13.  | Ground (Physical 06)  | UART                      |          |             |
| 14.  | GPIO 14 (Physical 08) | UART TX                   |          |             |
| 15.  | GPIO 16 (Physical 10) | UART RX                   |          |             |
| 16.  | 3v3 (Physical 1)      | I2C/UART                  |          |             |
| 17.  | 5v (Physical 2)       |                           |          |             |
| 18.  | GPIO 21 (Physical 40) | Blue Gripper Stop switch  |          |             |
| 19.  | GPIO 20 (Physical 39) | Red Gripper Stop switch   |          |             |
| 20.  | GPIO 12 (Physical 32) | Green Gripper Stop switch |          |             |
  
## Used [*] / Unsed [_] (GPIO pins)

|                     |        |        |                      |
| :------------------ | ------ | ------ | -------------------- |
| 3v3 Power           | 01 [*] | [*] 02 | 5v Power /1          |
| GPIO 2(I2C SDA)     | 03 [*] | [_] 04 | 5v Power             |
| GPIO 2(I2C SDA)     | 05 [*] | [*] 06 | Ground               |
| GPIO 4(GPCLK0)      | 07 [_] | [*] 08 | GPIO 14 (UART TX)    |
| Ground              | 09 [_] | [*] 10 | GPIO 15 (UART RX)    |
| GPIO 17             | 11 [*] | [_] 12 | GPIO 18 (PCM CLK)    |
| GPIO 27             | 13 [*] | [*] 14 | Ground               |
| GPIO 22             | 15 [_] | [*] 16 | GPIO 23              |
| 3v3 Power           | 17 [_] | [*] 18 | GPIO 24              |
| GPIO 10 (SPI MOSI)  | 19 [_] | [_] 20 | Ground               |
| GPIO 9 (SPIO MISO)  | 21 [_] | [_] 22 | GPIO 25              |
| GPIO 11 (SPIO SCLK) | 23 [_] | [*] 24 | GPIO 8 (SPI0 CE0)    |
| Ground              | 25 [_] | [*] 26 | GPIO 7 (SPI0 CE1)    |
| GPIO 0 (EEPROM SDA) | 27 [_] | [*] 28 | GPIO 1 (EEPROM SCL)) |
| GPIO 5              | 29 [*] | [_] 30 | Ground               |
| GPIO 6              | 31 [*] | [*] 32 | GPIO 12 (PWM0)       |
| GPIO 13 (PWM 1)     | 33 [_] | [_] 34 | Ground               |
| GPIO 19 (PCM FS)    | 35 [_] | [*] 36 | GPIO 16              |
| GPIO 26             | 37 [*] | [*] 38 | GPIO 20 (PCM DIN)    |
| Ground 39           | 39 [*] | [*] 40 | GPIO 21 (PCM DOUT)   |
              
