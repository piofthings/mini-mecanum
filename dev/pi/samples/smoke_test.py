#!/usr/bin/env python3

import os
import sys
import time
import serial
import picamera
from datetime import datetime
import atexit

sys.path.append(os.path.abspath(os.path.join(
    os.path.dirname(__file__), "../libs/smokey")))

from smokey import Smokey


miniMecanum = Smokey()
frame = 0
date = datetime.now()
folderName = 'captures/' + date.strftime('%Y-%m-%d-%H-%M-%S')
if not os.path.exists(folderName):
    os.makedirs(folderName)

def cleanup():
    miniMecanum.set_speed(0)

atexit.register(cleanup)

with picamera.PiCamera() as camera:
    camera.resolution = (128, 128)
    camera.start_preview()
    time.sleep(2)
    miniMecanum.set_speed(-128)
    while True:
        date = datetime.now()
        timestamp = date.strftime('%H-%M-%S')
        name = folderName + '/' + 'image' + timestamp + '-' + str(frame) + '.data'
        frame = frame + 1
        camera.capture(name, 'yuv')
