#!/usr/bin/env python3

import os
import sys
import time
import serial
import picamera
import picamera.array
from datetime import datetime
import atexit
import numpy as np
sys.path.append(os.path.abspath(os.path.join(
    os.path.dirname(__file__), "../libs/smokey")))

from smokey_gpio import SmokeyGpio


class SmokeyTest:
    __frame = 0
    __mem_buffer = np.empty((32, 32, 3), dtype=np.uint8)
    __miniMecanum = None

    def __init__(self):
        #Constructor
        self.__miniMecanum = SmokeyGpio([17,27,23,24,5,6,26,16])
        atexit.register(self.cleanup)

    def garden_path(self):
        self.__miniMecanum.set_speed_LR(128,128)
     
    def cleanup(self):
        try:
            self.__miniMecanum.set_speed(0)
            self.__miniMecanum.get_power_stats()
        except:
            print("Save failed")


if __name__ == '__main__':
    smokey = SmokeyTest()
    smokey.garden_path()
    
    while True:
        pass
