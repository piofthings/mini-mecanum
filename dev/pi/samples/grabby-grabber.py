# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

# This example moves a servo its full range (180 degrees by default) and then back.

from board import SCL, SDA
import busio
import time

# This example also relies on the Adafruit motor library available here:
# https://github.com/adafruit/Adafruit_CircuitPython_Motor
from adafruit_motor import servo

# Import the PCA9685 module.
from adafruit_pca9685 import PCA9685

from gpiozero import Button



i2c = busio.I2C(SCL, SDA)

# Create a simple PCA9685 class instance.
pca = PCA9685(i2c)
pca.frequency = 50

# To get the full range of the servo you will likely need to adjust the min_pulse and max_pulse to
# match the stall points of the servo.
# This is an example for the Sub-micro servo: https://www.adafruit.com/product/2201
# servo7 = servo.Servo(pca.channels[7], min_pulse=580, max_pulse=2480)
# This is an example for the Micro Servo - High Powered, High Torque Metal Gear:
#   https://www.adafruit.com/product/2307
# servo7 = servo.Servo(pca.channels[7], min_pulse=600, max_pulse=2400)
# This is an example for the Standard servo - TowerPro SG-5010 - 5010:
#   https://www.adafruit.com/product/155
# servo7 = servo.Servo(pca.channels[7], min_pulse=600, max_pulse=2500)
# This is an example for the Analog Feedback Servo: https://www.adafruit.com/product/1404
# servo7 = servo.Servo(pca.channels[7], min_pulse=600, max_pulse=2600)

# The pulse range is 1000 - 2000 by default.
clampLeft = servo.Servo(pca.channels[0])
swingArmLeft = servo.Servo(pca.channels[5])
button12 = Button(12)
button8 = Button(22)
button21 = Button(21)

while True:
    if button12.is_pressed:
        print("Button 12 is pressed")
    if button8.is_pressed:
        print("Button 8 is pressed")
    if button21.is_pressed:
        print("Button 21 is pressed")
    time.sleep(0.5)

# clampLeft.angle = 0
# time.sleep(0.5)
# clampLeft.angle = -30
# time.sleep(0.5)
# max = 40
# for i in range(max):
#      clampLeft.angle = i
#      time.sleep(0.05)
# for i in range(max):
#      if button.is_pressed:
#          print("Button is pressed")
#          clampLeft.angle = clampLeft.angle + 3
#          time.sleep(0.05)
#          break
    
#      else:
#         clampLeft.angle = max - i
#         time.sleep(0.05)
#         #print("Button is not pressed")

pca.deinit()
