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

from diycv.camera.capture_threshold import CaptureThreshold
from diycv.filestream.pgm_threshold import PgmThreshold
from smokey.smokey import Smokey

class Main():
    __challenge = ""
    __miniMecanum = Smokey()

    __command_queue = queue.Queue()
    __captureThresholder = None

    __is_simulation = False

    def __init__(self, challenge):
        self.__challenge = challenge
        atexit.register(self.cleanup)
        if (challenge.contains("_sim")):
            this.__is_simulation = True

    def worker(self):
        speedL = 0
        speedR = 0
        ratio = 0.0
        """
        Number of frames that must be marked as "fork" before we start considering the frame 
        as a fork. Increase value if too many false positives
        """
        fork_id_frames_threshold = 3 

        fork_number = 0
        continuous_fork_frames_for = 0
        looking_at_fork = False

        while True:
            try:
                item = self.__command_queue.get()
                if item.index == 174:
                    print(item.rows)
                if item.is_fork :
                    continuous_fork_frames_for = continuous_fork_frames_for + 1
                else:
                    continuous_fork_frames_for = 0
                if continuous_fork_frames_for > fork_id_frames_threshold:
                    item.is_fork = True
                    if looking_at_fork == False:
                        looking_at_fork = True
                        fork_number = fork_number + 1
                else:
                    item.is_fork = False
                    looking_at_fork = False

                print("{:d},{:f},{:d},{:d},{:d},{},{},{:d},{:d},{}".format(
                    item.index,
                    item.ratio,
                    item.thickness,
                    item.speedL, 
                    item.speedR, 
                    item.is_fork, 
                    item.is_straight, 
                    continuous_fork_frames_for,
                    fork_number,
                    item.average_row))

                #self.__miniMecanum.set_speed_LR(item.speedL, item.speedR)
                self.__command_queue.task_done()
            except Exception as e:
                print(e)
                traceback.print_exc()



    def start(self):
        threading.Thread(target=self.worker, daemon=True).start()
        thresholdEnable = True
        stretchEnable = False
        self.__miniMecanum.get_power_stats()
        if self.__challenge == 'garden_path':
            self.__captureThresholder = CaptureThreshold(self.__command_queue, 32, 32, 30)
            self.__captureThresholder.start_capture(32,32, thresholdEnable, stretchEnable, True)        
        elif (self.__challenge == "garden_path_sim"):
            thisdir = os.getcwd() + "/samples/captures/2020-12-13-20-28-36"
            self.__captureThresholder = PgmThreshold(self.__command_queue, thisdir)
            self.__captureThresholder.start_capture(32,32, thresholdEnable, stretchEnable, True)
        while True:
            pass
            

    def cleanup(self):
        try:
            #self.__command_queue.join()
            if self.__challenge == 'garden_path':
                self.__captureThresholder.stop_capture()
            time.sleep(1)
            self.__miniMecanum.set_speed(0)
            self.__miniMecanum.get_power_stats()
            self.__miniMecanum.set_speed(0)
        except:
            print("Save failed")

if __name__ == '__main__':
    main = Main("garden_path_sim")
    try:
        main.start()
    except:
        exit(0)