#!/usr/bin/env python3

import os
import sys
import time
import serial
import picamera

sys.path.append(os.path.abspath(os.path.join(
    os.path.dirname(__file__), "../libs/smokey")))

from smokey import Smokey

miniMecanum = Smokey()
frame = 0

while True:
    miniMecanum.set_speed(128)
    with picamera.PiCamera() as camera:
        camera.resolution = (100, 100)
        camera.start_preview()
        time.sleep(2)
        name = 'image' + str(frame) + '.data'
        camera.capture(name, 'yuv')
