#!/usr/bin/env python3
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

from diycv.filestream.pgm_threshold import PgmThreshold
#from smokey.smokey import Smokey

class Main():
    __challenge = ""
    __miniMecanum = None

    __command_queue = queue.Queue()
    __captureThresholder = None

    __is_simulation = False

    def __init__(self, challenge):
        self.__challenge = challenge
        atexit.register(self.cleanup)
        if ("_sim" in challenge):
            self.__is_simulation = True
        else:
            self.__miniMecanum = Smokey()

    def worker(self):
        while True:
            item = self.__command_queue.get()
            #print(f'Working on {item}')
            #print(item[15])
            first_white_pos = 0
            last_white_pos = 0
            current_pos_white = False
            prev_post_white = False
            speed = 0
            for pos in range(0,31):
                if item[15][pos] == 255:
                    if first_white_pos == 0:
                        first_white_pos = pos
                    else:
                        last_white_pos = pos
                    current_pos_white = True
                else:
                    prev_post_white = current_pos_white
                    current_pos_white = False
            thickness = last_white_pos - first_white_pos + 1
            if  thickness > 1 and thickness < 6:
                speed = 200
                #good thickness
                ideal_center = 8 - (thickness/2)
                ratio = ideal_center/first_white_pos
                # 0 0 0 0 0 0 1 1 1 1 0 0 0 0 0 0 | ideal, ratio = 1
                # 0 0 1 1 1 1 0 0 0 0 0 0 0 0 0 0 | move right wheels faster, ratio > 1
                # 0 0 0 0 0 0 0 0 0 0 1 1 1 1 0 0 | move left wheels faster, ratio < 1
                if ratio > 1:
                    speedL = int(speed/ratio)
                    speedR = speed
                    if self.__is_simulation == False:
                        self.__miniMecanum.set_speed_LR(speedL, speedR)
                    
                if ratio < 1:
                    speedL = speed
                    speedR = int(speed * ratio)
                    if self.__is_simulation == False:
                        self.__miniMecanum.set_speed_LR(speed, int(speed * ratio))
                #print("{:d}-{:d}-{:d}".format(thickness, first_white_pos, last_white_pos))
            else:
                speed = 0
                #self.__miniMecanum.set_speed_LR(speed, speed)
            print("{:d},{:d},{:d},{:d},".format(thickness, first_white_pos, last_white_pos, speed) + str(item[15]))

            self.__command_queue.task_done()

    def start(self):
        threading.Thread(target=self.worker, daemon=True).start()
        thresholdEnable = True
        stretchEnable = False
        if (self.__challenge == "garden_path_sim"):
            thisdir = os.getcwd() + "/samples/captures/2020-12-13-20-28-36"

            self.__captureThresholder = PgmThreshold(self.__command_queue, thisdir)
            self.__captureThresholder.start_capture(32,32, thresholdEnable, stretchEnable, True)
        while True:
            pass
            

    def cleanup(self):
        try:
            time.sleep(1)

        except Exception as e:
            print(e)

if __name__ == '__main__':
    main = Main("garden_path_sim")
    try:
        main.start()
    except Exception as e:
        print(e)
        exit(0)