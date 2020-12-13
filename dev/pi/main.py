#!/usr/bin/env python3
import picamera
import sys
import os
import warnings
import time
import atexit
from timeit import default_timer as timer
from datetime import datetime
import threading, queue

sys.path.append(os.path.abspath(os.path.join(
    os.path.dirname(__file__), "./libs")))
    
from diycv.camera.capture_threshold import CaptureThreshold
from smokey.smokey import Smokey

class Main():
    __challenge = ""
    __miniMecanum = Smokey()

    __command_queue = queue.Queue()
    __captureThresholder = None

    def __init__(self, challenge):
        self.__challenge = challenge
        self.__captureThresholder = CaptureThreshold(self.__command_queue)

    def worker(self):
        while True:
            item = self.__command_queue.get()
            #print(f'Working on {item}')
            #print(item[15])
            first_white_pos = 0
            last_white_pos = 0
            current_pos_white = False
            prev_post_white = False
            for pos in range(0, 15):

                if item[15][pos] == 255:
                    if first_white_pos == 0:
                        first_white_pos = pos
                    else:
                        last_white_pos = pos
                    current_pos_white = True
                else:
                    prev_post_white = current_pos_white
                    current_pos_white = False
            thickness = last_white_pos - first_white_pos
            if  thickness > 2 and thickness < 6:
                speed = 255
                #good thickness
                ideal_center = 8 - (thickness/2)
                ratio = ideal_center/first_white_pos
                # 0 0 0 0 0 0 1 1 1 1 0 0 0 0 0 0 | ideal, ratio = 1
                # 0 0 1 1 1 1 0 0 0 0 0 0 0 0 0 0 | move right wheels faster, ratio > 1
                # 0 0 0 0 0 0 0 0 0 0 1 1 1 1 0 0 | move left wheels faster, ratio < 1
                if ratio > 1:
                    # 
                    self.__miniMecanum.set_speed_LR(int(speed/ratio), speed)
                if ratio < 1:
                    self.__miniMecanum.set_speed_LR(speed, int(speed * ratio))
                #print("{:d}-{:d}-{:d}".format(thickness, first_white_pos, last_white_pos))
            else:
                speed = 128
                self.__miniMecanum.set_speed_LR(speed, speed)
            self.__command_queue.task_done()

    def start(self):
        threading.Thread(target=self.worker, daemon=True).start()
        self.__captureThresholder.start_capture(32,32,True, True, True)
        
        while True:
            pass
            

    def cleanup(self):
        try:
            self.__miniMecanum.set_speed(0)
            self.__captureThresholder.stop_capture()
        except:
            print("Save failed")

if __name__ == '__main__':
    main = Main("garden_path")
    main.start()