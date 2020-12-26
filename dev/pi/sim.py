#!/usr/bin/env python3
import sys
import os
import warnings
import time
import traceback
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
        speedL = 0
        speedR = 0
        ratio = 0.0
        while True:
            try:
                item = self.__command_queue.get()
                if item.index == 174:
                    print(item.rows)
                print("{:d},{:f},{:d},{:d},{:d},{},{},{}".format(
                    item.index,
                    item.ratio,
                    item.thickness,
                    item.speedL, 
                    item.speedR, 
                    item.is_fork, 
                    item.is_straight, 
                    item.average_row))
                self.__command_queue.task_done()
            except Exception as e:
                print(e)
                traceback.print_exc()
            

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