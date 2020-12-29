#!/usr/bin/env python3
import sys
import os
import traceback
from os.path import isfile, join
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

class PgmThreshold():
    __frame_processor_queue = None
    __camera = None
    __source_folder = ""
    __is_simulation = True
    __line_processor = None

    def __init__(self, queue, source_folder, set_speed):
        self.__frame_processor_queue = queue
        self.__source_folder = source_folder
        self.__line_processor = Line(queue, set_speed)

    def write_pgm(self, filename, w, h, data):
        with open(filename, 'wb') as f:
            f.write("P5\n{:d} {:d}\n255\n".format(w, h).encode('utf8'))
            f.write(data)

    def read_pgm(self, filename, w, h, data):
        try:
            with open(filename, 'rb') as pgmf:
                """Return a raster of integers from a PGM as a list of lists."""
                p5 = pgmf.readline()
                # print(p5)
                shape = pgmf.readline()
                # print(shape)
                depth = pgmf.readline()
                # print(depth)
                #assert depth <= 255
                i = 0
                bites = pgmf.read()
                data[0:bites.count(0)] = bites


                #return bytearray(pgmf.read(w * (h*2)))


        except Exception as e:
            print("read_pgm: Error @ " + filename)

            print(e)
            traceback.print_exc()
            
    def start_capture(self, width, height, threshold, stretch, save):
        start = timer()
        prev = start
        i = 0
        total = 0
        folderName = "captures/" + datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
        if not os.path.exists(folderName):
            os.makedirs(folderName)

        print(self.__source_folder)
        allFiles = os.listdir(self.__source_folder)
        #print (allFiles)

        count = 0
        for filename in allFiles:
            if ("gray" in filename):
                count = count + 1

        i = 0
        try:
            for index in range(1, count):
                i=i+1
                fullpath = os.path.join(self.__source_folder, "grayscale_" + str(index) + ".pgm") 
                #print(fullpath)

                data = bytearray(b'\0' * (width * (height*2)))
                
                self.read_pgm(fullpath, width, height, data)
                self.__line_processor.process_bytearray(data, width, height, threshold, stretch, index)
                if save:
                    # Save result
                    self.write_pgm("{:s}/processed_{:d}.pgm".format(self.__source_folder, index), width, height, data)

                now = timer()
                t = now - prev
                #print("Frame {} time: {}, processing took: {}".format(i, t, proc_time))
                prev = now

            print("{:d} frames in {}, {} fps".format(i, now - start, i / (now - start)))

        except Exception as e:
            print(e)


    def stop_capture(self):
        pass
        # exit(0)


if __name__ == '__main__':
    lineDetector = CaptureThreshold()
    lineDetector.start_capture(32,32, True, True, True)
    timer.suspend(3)
    lineDetector.stop_capture()