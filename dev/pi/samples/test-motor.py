# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""Simple test for using adafruit_motorkit with a DC motor"""
import time
import board
from adafruit_motorkit import MotorKit
import threading


def stop_arm():
    kit.motor1.throttle = 0
    print("stopped via timer")


kit = MotorKit(i2c=board.I2C())
kit.motor1.throttle = 0
time.sleep(1)

kit.motor1.throttle = -1
timeout = 9
timer = threading.Timer(timeout, stop_arm)
timer.start()  

count = 0
while True:
    print("Waiting...")
    time.sleep(0.2)
    count = count + 1
    if count > (timeout/0.2):
        break

kit.motor1.throttle = 0

