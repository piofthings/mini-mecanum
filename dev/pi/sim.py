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

    speedL = 0
    speedR = 0
    ratio = 0.0
    """
    Number of frames that must be marked as "fork" to be counted as a fork. 
    Increase value if too many false positives
    """
    fork_id_frames_threshold = 3 

    fork_number = 0
    continuous_fork_frames_for = 0
    looking_at_fork = False
    
    def __init__(self, challenge):
        self.__challenge = challenge
        atexit.register(self.cleanup)
        if ("_sim" in challenge):
            self.__is_simulation = True
        else:
            self.__miniMecanum = Smokey()

    def worker(self, item):
        try:
            self.last_index = item.index
            if item.is_fork :
                self.continuous_fork_frames_for = self.continuous_fork_frames_for + 1
            else:
                self.continuous_fork_frames_for = 0
            if self.continuous_fork_frames_for > self.fork_id_frames_threshold:
                item.is_fork = True
                if self.looking_at_fork == False:
                    self.looking_at_fork = True
                    self.fork_number = self.fork_number + 1
                    self.one_time_adjustment = False
            else:
                item.is_fork = False
                self.looking_at_fork = False

            print("{:d},{:f},{:d},{:d},{:d},{},{},{:d},{:d},{}".format(
                item.index,
                item.ratio,
                item.thickness,
                item.speedL, 
                item.speedR, 
                item.is_fork, 
                item.is_straight, 
                self.continuous_fork_frames_for,
                self.fork_number,
                item.average_row))

            # if self.fork_number == 1:
            #     self.__miniMecanum.set_speed_LR(item.speedL, item.speedR)
            #     pass #no adjustments necessary, just follow the line
            # elif self.fork_number == 2:
            #     if self.one_time_adjustment == False and self.continuous_fork_frames_for > 5:
            #         self.__miniMecanum.set_speed_LR(200, 100)        
            #         self.one_time_adjustment = True
            # elif self.fork_number == 3:
            #     if self.one_time_adjustment == False and self.continuous_fork_frames_for > 5:
            #         self.__miniMecanum.set_speed_LR(70, 200)        
            #         self.one_time_adjustment = True
            # else:
            #     self.__miniMecanum.set_speed_LR(item.speedL, item.speedR)

            
            # self.__command_queue.task_done()
        except Exception as e:
            print(e)
            traceback.print_exc()
            exit(0)
            

    def start(self):
        thresholdEnable = True
        stretchEnable = False
        if (self.__challenge == "garden_path_sim"):
            thisdir = os.getcwd() + "/samples/captures/2020-12-29-02-22-32"

            self.__captureThresholder = PgmThreshold(self.__command_queue, thisdir, self.worker)
            self.__captureThresholder.start_capture(32,32, thresholdEnable, stretchEnable, True)
        # while True:
        #     pass
            

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