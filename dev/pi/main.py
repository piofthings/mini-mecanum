#!/usr/bin/env python3
import sys
import os
import warnings
import time
import atexit
from timeit import default_timer as timer
from datetime import datetime
import threading, queue
import traceback

sys.path.append(os.path.abspath(os.path.join(
    os.path.dirname(__file__), "./libs")))

from diycv.camera.capture_threshold import CaptureThreshold
from diycv.filestream.pgm_threshold import PgmThreshold
from smokey.smokey_gpio import SmokeyGpio

class Main():
    __challenge = ""
    __miniMecanum = SmokeyGpio([17,27,23,24,5,6,26,16])

    __command_queue = queue.Queue()
    __captureThresholder = None

    __is_simulation = False

    """
    Number of frames that must be marked as "fork" before we star t considering the frame 
    as a fork. Increase value if too many false positives
    """
    fork_id_frames_threshold = 1 
    last_index = 0
    fork_number = 0
    continuous_fork_frames_for = 0
    looking_at_fork = False
    capture_started = None

    def __init__(self, challenge):
        self.__challenge = challenge
        atexit.register(self.cleanup)
        if ("_sim" in challenge):
            self.__is_simulation = True


    def worker(self, item):
        # while True:
        try:
            # item = self.__command_queue.get()
            # if item.index == 174:
            #     print(item.rows)
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

            if self.fork_number == 1:
                self.__miniMecanum.set_speed_LR(item.speedL, item.speedR)
                pass #no adjustments necessary, just follow the line
            elif self.fork_number == 2:
                if self.one_time_adjustment == False and self.continuous_fork_frames_for > 5:
                    self.__miniMecanum.set_speed_LR(200, 100)        
                    self.one_time_adjustment = True
            elif self.fork_number == 3:
                if self.one_time_adjustment == False and self.continuous_fork_frames_for > 5:
                    self.__miniMecanum.set_speed_LR(70, 200)        
                    self.one_time_adjustment = True
            else:
                self.__miniMecanum.set_speed_LR(item.speedL, item.speedR)
            # self.__command_queue.task_done()
        except Exception as e:
            print(e)
            traceback.print_exc()
            exit(0)



    def start(self):
        try:
            # threading.Thread(target=self.worker, daemon=True).start()
            thresholdEnable = True
            stretchEnable = False
            self.__miniMecanum.get_power_stats()
            if self.__challenge == 'garden_path':
                self.__captureThresholder = CaptureThreshold(self.__command_queue, 32, 32, 30, self.worker)
                self.capture_started = timer()
                self.__captureThresholder.start_capture(thresholdEnable, stretchEnable, True)        
            elif (self.__challenge == "garden_path_sim"):
                thisdir = os.getcwd() + "/samples/captures/2020-12-13-20-28-36"
                self.__captureThresholder = PgmThreshold(self.__command_queue, thisdir)
                self.__captureThresholder.start_capture(32,32, thresholdEnable, stretchEnable, True)
            # while True:
            #     timer.sleep(0.001)
            #     pass
        except Exception as e:
            print(e)
            traceback.print_exc()
            exit(0)
            

    def cleanup(self):
        try:
            now = timer()
            print(str(self.last_index/(now - self.capture_started)) + " Frames per second")
            # self.__command_queue.join()
            if self.__challenge == 'garden_path':
                self.__captureThresholder.stop_capture()
            self.__miniMecanum.set_speed(0)
            self.__miniMecanum.get_power_stats()
            self.__miniMecanum.set_speed(0)
        except:
            print("Save failed")

if __name__ == '__main__':
    main = Main("garden_path")
    try:
        main.start()
    except:
        exit(0)