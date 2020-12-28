# mini-mecanum

Mini Mecanum bot goes to [PiWars at Home 2021](https://piwars.org)

Yes, we couldn't resist and put our names in for [PiWars at Home 2021](https://piwars.org) and now we are in deep trouble.

# Motor Driver using GPIOZero
We are using 2xMDD3A Cytron motor drivers to drive 4 motors independently so we can strafe when we use Mecanum motors. The drivers use PWM signal for forward and backward directions instead of using a PWM and Direction pin.

Looks like the `GPIO Zero` libraries' `Motor` abstraction will work with this driver. So we are using the following Pins on the Pi

 --------------------------------------------------------
| GPIO 17 (Physical 11) | Left Front | Forward  | Yellow | 
| GPIO 27 (Physical 13) | Left Front | Backward | Blue   | 
|------------------------------------|----------|---------
| GPIO 23 (Phyiscal 16) | Left Rear  | Forward  | Yellow | 
| GPIO 24 (Physical 18) | Left Rear  | Backward | Blue   |
|------------------------------------|----------|---------
| GPIO 5 (Phyiscal 29) | Right Front | Forward  | Yellow |
| GPIO 6 (Physical 31) | Right Front | Backward | Blue   |
|------------------------------------|----------|---------
| GPIO 26 (Phyiscal 37) | Right Rear | Forward  | Yellow |
| GPIO 16 (Phyiscal 36) | Right Rear | Backward | Blue   |
 --------------------------------------------------------
