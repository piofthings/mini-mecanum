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

class PgmThreshold():
    __frame_processor_queue = None
    __camera = None
    __source_folder = ""
    __is_simulation = True

    def __init__(self, queue, source_folder):
        self.__frame_processor_queue = queue
        self.__source_folder = source_folder

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

            



    def process_bytearray(self, data, w, h, thresh=True, stretch=True, index = -1):
        y = 0
        out = []
        frame_data = FrameData()
        frame_data.index = index
        average_out=[]
        average_out = [0 for i in range(w)]         

        try:
            while y < h:

                row = memoryview(data)[y*w:(y+1)*w]
                if stretch:
                    minval = 255
                    maxval = 0
                    for val in row:
                        if val < minval:
                            minval = val
                        if val > maxval:
                            maxval = val

                    diff = maxval - minval

                    factor = 1
                    if diff != 0:
                        factor = 255/diff

                x = 0
                for val in row:
                    if stretch:
                        val = int((val - minval) * factor)
                    if thresh:
                        if val > 128:
                            val = 255
                        else:
                            val = 0
                        row[x] = val
                    else:
                        row[x] = val

                    if x == 0:
                        average_out[x] = val
                    else:
                        average_out[x] = (average_out[x] + val)
                    if( y == h - 1):
                        average_out[x] = int(average_out[x] / h)
                    x = x + 1
                y = y + 1
                out.append(row.tolist())
            if self.__frame_processor_queue  != None:
                frame_data.rows = out
                self.nomalize_avg(average_out, w)
                frame_data.average_row = average_out
                self.set_speed(frame_data)
                self.__frame_processor_queue.put(frame_data, block=True, timeout=0.5)
        except Exception as e:
                print(e)
                traceback.print_exc()

    def nomalize_avg(self, average_row, width):
        for col in range(0, width - 1):
            if(average_row[col] < 100 and average_row[col] > 9):
                average_row[col] = 128
            elif (average_row[col] < 10):
                average_row[col] = 0
            elif (average_row[col] > 99):
                average_row[col] = 255

    def set_speed(self, frame_data):
        try:        
            first_white_pos = 0
            last_white_pos = 0
            current_pos_white = False
            prev_post_white = False
            speed = 0
            for pos in range(0,32):
                if frame_data.average_row[pos] == 255:
                    if first_white_pos == 0:
                        first_white_pos = pos
                    else:
                        last_white_pos = pos
                    current_pos_white = True
                else:
                    prev_post_white = current_pos_white
                    current_pos_white = False
            thickness = last_white_pos - first_white_pos + 1
            if  thickness > 1:
                speed = 200
                #good thickness
                ideal_center = (32 - thickness)/2
                ratio = ideal_center/first_white_pos
                frame_data.ratio = ratio
                # 0 0 0 0 0 0 1 1 1 1 0 0 0 0 0 0 | ideal, ratio = 1
                # 0 0 1 1 1 1 0 0 0 0 0 0 0 0 0 0 | move left wheels faster, ratio > 1
                # 0 0 0 0 0 0 0 0 0 0 1 1 1 1 0 0 | move right wheels faster, ratio < 1
                if ratio > 1:
                    frame_data.speedR = int(speed/ratio)
                    frame_data.speedL = speed
                    if self.__is_simulation == False:
                        self.__miniMecanum.set_speed_LR(speedL, speedR)
                    
                elif ratio < 1:
                    frame_data.speedR = speed
                    frame_data.speedL = int(speed * ratio)
                    if self.__is_simulation == False:
                        self.__miniMecanum.set_speed_LR(speed, int(speed * ratio))
                else :
                    frame_data.speedL = speed
                    frame_data.speedR = speed
                #print("{:d}-{:d}-{:d}".format(thickness, first_white_pos, last_white_pos))
            else:
                frame_data.speedL = 0
                frame_data.speedR = 0
            frame_data.first_white_pos = first_white_pos
            frame_data.last_white_pos = last_white_pos
            frame_data.thickness = thickness
        except Exception as e:
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

                proc_start = timer()
                data = bytearray(b'\0' * (width * (height*2)))
                
                self.read_pgm(fullpath, width, height, data)
                self.process_bytearray(data, width, height, threshold, stretch, index)
                proc_time = timer() - proc_start
                if save:
                    # Save result
                    self.write_pgm("{:s}/processed_{:d}.pgm".format(self.__source_folder, index), width, height, data)

                now = timer()
                t = now - prev
                #print("Frame {} time: {}, processing took: {}".format(i, t, proc_time))
                prev = now

            print("{:d} frames in {}, {} fps".format(i, now - start, i / (now - start)))
            start = timer()

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