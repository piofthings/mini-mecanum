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


def class Smokey():
    __frame = 0
    __mem_buffer = np.empty((32, 32, 3), dtype=np.uint8)

    def __init__(self):
        #Constructor
        atexit.register(self.cleanup)

    def garden_path(self):
        miniMecanum = Smokey()
        date = datetime.now()


        with picamera.PiCamera() as camera:
            camera.resolution = (32, 32)
            camera.start_preview()
            time.sleep(2)
            miniMecanum.set_speed(128)
            date = datetime.now()
            
            print(date.strftime('%H-%M-%S-%f')[:-3])
            while True:
                frame = frame + 1
                output = np.empty((32, 32, 3), dtype=np.uint8)
                camera.capture(output, 'yuv')
                np.vstack((self.__mem_buffer,output))


    def cleanup(self):
        miniMecanum.set_speed(0)
        print(self.__frame)
        print(date.strftime('%H-%M-%S-%f')[:-3])
        try:
            fileName = 'captures/' + date.strftime('%Y-%m-%d-%H-%M-%S')
            if not os.path.exists(folderName):
                os.makedirs(folderName)
            np.save(folderName + "/" + date.strftime('%H-%M-%S-%f')[:-3], self.__mem_buffer)
        except:
            print("Save failed")


if __name__ == '__main__':
    smokey = Smokey()
