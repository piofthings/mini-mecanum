#!/usr/bin/env python3
import picamera
import sys
import os
import warnings
import time
from timeit import default_timer as timer
from datetime import datetime

class CaptureThreshold():
    __frame_processor_queue = None
    __camera = None

    def __init__(self, queue):
        self.__frame_processor_queue = queue

    def write_pgm(self, filename, w, h, data):
        with open(filename, 'wb') as f:
            f.write("P5\n{:d} {:d}\n255\n".format(w, h).encode('utf8'))
            f.write(data)

    def process_bytearray(self, data, w, h, stretch=True, thresh=True):
        if stretch:
            y = 0
            out = []
            while y < h:
                row = memoryview(data)[y*w:(y+1)*w]
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
                    val = int((val - minval) * factor)
                    if thresh:
                        if val > 128:
                            val = 255
                        else:
                            val = 0
                        row[x] = val
                    else:
                        row[x] = val
                    x = x + 1
                y = y + 1
                out.append(row.tolist())
            if self.__frame_processor_queue  != None:
                self.__frame_processor_queue.put(out, block=False, timeout=0.5)


    def start_capture(self, width, height, threshold, stretch, save):
        self.__camera = picamera.PiCamera(resolution='{:d}x{:d}'.format(width, height), framerate=30)
        data = bytearray(b'\0' * (width * (height*2)))

        self.__camera.start_preview()
        # Wait for 3s to settle
        time.sleep(3)
        start = timer()
        prev = start
        i = 0
        folderName = "captures/" + datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
        if not os.path.exists(folderName):
            os.makedirs(folderName)

        for foo in self.__camera.capture_continuous(data, 'yuv', use_video_port=True):
            i = i + 1

            if save:
                # Save original
                self.write_pgm("{:s}/out_{:d}.pgm".format(folderName, i), width, height, data)

            proc_start = timer()
            self.process_bytearray(data, width, height, stretch=stretch, thresh=threshold)
            proc_time = timer() - proc_start

            if save:
                # Save result
                self.write_pgm("{:s}/out_proc_{:d}.pgm".format(folderName, i), width, height, data)

            now = timer()
            t = now - prev
            #print("Frame time: {}, processing took: {}".format(t, proc_time))
            prev = now

            if now - start > 1:
                print("{:d} frames in {}, {} fps".format(i, now - start, i / (now - start)))
                i =0
                start = timer()
                prev = start

    def stop_capture(self):
        self.__camera.stop_preview()
        # exit(0)


if __name__ == '__main__':
    lineDetector = CaptureThreshold()
    lineDetector.start_capture(32,32, True, True, True)
    timer.suspend(3)
    lineDetector.stop_capture()