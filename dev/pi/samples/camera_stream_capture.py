#!/usr/bin/env python3
from picamera.array import PiAnalysisOutput
from picamera.color import Color
from picamera.array import PiYUVAnalysis
import numpy as np
import picamera
import sys
import os
import warnings
from timeit import default_timer as timer

sys.path.append(os.path.abspath(os.path.join(
    os.path.dirname(__file__), "../libs")))

from diycv.effects.thresholding import Thresholding

class GreyScaleYUVAnalysis(PiAnalysisOutput):
    def write(self, b):
        super(GreyScaleYUVAnalysis, self).write(b)
        return self.analyze(self.bytes_to_yuv_raw(b, self.size or self.camera.resolution))
        return result

    def raw_resolution(self, resolution, splitter=False):
        width, height = resolution
        if splitter:
            fwidth = (width + 15) & ~15
        else:
            fwidth = (width + 31) & ~31
        fheight = (height + 15) & ~15
        return fwidth, fheight

    def bytes_to_yuv_raw(self, data, resolution):
        width, height = resolution
        fwidth, fheight = self.raw_resolution(resolution)
        y_len = fwidth * fheight
        # Separate out the Y only we discard the UV for greyscale analysis
        a = np.frombuffer(data, dtype=np.uint8)
        Y = a[:y_len].reshape((fheight, fwidth))
        return Y


class LineAnalyser(GreyScaleYUVAnalysis):
    def __init__(self, camera):
        super(LineAnalyser, self).__init__(camera)
        self.last_color = ''
        self.threshold = Thresholding(32, 32)
        self.count = 0

    def analyze(self, a):
        Y = a
        print(self.count)
        self.count = self.count + 1
#		print(Y.size)
        y_thresholded = self.threshold.with_np_array(Y, True)
#        print(y_thresholded)


np.set_printoptions(threshold=sys.maxsize, linewidth=1000)
warnings.filterwarnings('error', category=DeprecationWarning)

with picamera.PiCamera(resolution='32x32', framerate=30) as camera:
    # Fix the camera's white-balance gains
    camera.awb_mode = 'off'
    camera.awb_gains = (1.4, 1.5)
    with LineAnalyser(camera) as analyzer:
        camera.start_recording(analyzer, 'yuv')
        try:
            i = 0            
            start = timer()
            camera.wait_recording(1)

            while i < 1:
                end = timer()
                if(end - start > 1) :
                    i = 1
            camera.stop_recording()
        finally:
            pass
#			camera.stop_recording()


