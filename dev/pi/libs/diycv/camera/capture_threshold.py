#!/usr/bin/env python3
import picamera
import sys
import os
import warnings
import time
from timeit import default_timer as timer
from datetime import datetime

sys.path.append(os.path.abspath(os.path.join(
    os.path.dirname(__file__), "../models")))

from frame_data import FrameData
from row_data import RowData

sys.path.append(os.path.abspath(os.path.join(
    os.path.dirname(__file__), "../detection")))

from line import Line

class CaptureThreshold():
    __frame_processor_queue = None
    __camera = None
    __line_processor = None
    __width = 32
    __height = 32
    __framerate = 30

    def __init__(self, queue, width, height, framerate):
        self.__framerate = framerate
        self.__frame_processor_queue = queue
        self.__width = width
        self.__height = height
        self.__line_processor = Line(queue)
        self.__camera = picamera.PiCamera(resolution='{:d}x{:d}'.format(width, height), framerate=framerate)
        self.__camera.start_preview()
        # Wait for 3s to settle
        time.sleep(3)

    def write_pgm(self, filename, w, h, data):
        with open(filename, 'wb') as f:
            f.write("P5\n{:d} {:d}\n255\n".format(w, h).encode('utf8'))
            f.write(data)

    
    def start_capture(self, threshold, stretch, save):
        data = bytearray(b'\0' * (width * (height*2)))
        start = timer()
        prev = start
        i = 0
        total = 0
        folderName = "captures/" + datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
        if not os.path.exists(folderName):
            os.makedirs(folderName)

        try:
            for foo in self.__camera.capture_continuous(data, 'yuv', use_video_port=True):
                i = i + 1
                if save:
                    # Save original
                    self.write_pgm("{:s}/grayscale_{:d}.pgm".format(folderName, total), width, height, data)

                self.__line_processor.process_bytearray(data, width, height, threshold, stretch)

                if save:
                    # Save result
                    self.write_pgm("{:s}/processed_{:d}.pgm".format(folderName, total), width, height, data)

                now = timer()
                t = now - prev
                #print("Frame time: {}, processing took: {}".format(t, proc_time))
                prev = now

            print("{:d} frames in {}, {} fps".format(i, now - start, i / (now - start)))
        except Exception as e:
            print(e)


    def stop_capture(self):
        if self.__camera:
            self.__camera.stop_preview()
        # exit(0)


if __name__ == '__main__':
    lineDetector = CaptureThreshold()
    lineDetector.start_capture(32,32, True, True, True)
    timer.suspend(3)
    lineDetector.stop_capture()