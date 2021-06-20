#!/usr/bin/env python3

from gpiozero import AngularServo
from time import sleep

# servo = Servo(22)
servo = AngularServo(22, min_angle=-90, max_angle=90)
i = 0
while i < 1:
    servo.angle = -90
    sleep(5)
    # servo.angle = -45
    # sleep(5)
    servo.angle = 90
    sleep(2)
    # servo.angle = 45
    # sleep(2)
    # servo.angle = 90
    # sleep(2)
    i = 1
