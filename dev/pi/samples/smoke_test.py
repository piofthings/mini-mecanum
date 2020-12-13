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

from smokey import Smokey


class SmokeyTest:
    __frame = 0
    __mem_buffer = np.empty((32, 32, 3), dtype=np.uint8)
    __miniMecanum = None

    def __init__(self):
        #Constructor
        self.__miniMecanum = Smokey()
        atexit.register(self.cleanup)

    def garden_path(self):
        self.__miniMecanum.set_speed_LR(128,128)
     
    def cleanup(self):
        try:
            self.__miniMecanum.set_speed(0)
            print(self.__frame)
            print(date.strftime('%H-%M-%S-%f')[:-3])

            folderName = 'captures/' + date.strftime('%Y-%m-%d-%H-%M-%S')
            if not os.path.exists(folderName):
                os.makedirs(folderName)
            np.save(folderName + "/" + date.strftime('%H-%M-%S-%f')[:-3], self.__mem_buffer)
        except:
            print("Save failed")


if __name__ == '__main__':
    smokey = SmokeyTest()
    smokey.garden_path()
    while True:
        pass
