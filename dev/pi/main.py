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

class Main():
    __challenge = ""

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
            self.__command_queue.task_done()

    def start(self):
        threading.Thread(target=self.worker, daemon=True).start()
        self.__captureThresholder.start_capture(32,32,True, True, False)
        
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