#!/usr/bin/env/python3
from diycv.effects.thresholding import Thresholding
from picamera.color import Color
from picamera.array import PiYUVAnalysis
import numpy as np
import picamera
import sys
import os
from picamera.array import PiAnalysisOutput

sys.path.append(os.path.abspath(os.path.join(
    os.path.dirname(__file__), "../libs")))


class MyPiYUVAnalysis(PiAnalysisOutput):
    """
    Provides a basis for per-frame YUV analysis classes.
    This custom output class is intended to be used with the
    :meth:`~picamera.PiCamera.start_recording` method when it is called with
    *format* set to ``'yuv'``. While recording is in progress, the
    :meth:`~PiAnalysisOutput.write` method converts incoming frame data into a
    numpy array and calls the stub :meth:`~PiAnalysisOutput.analyze` method
    with the resulting array (this deliberately raises
    :exc:`NotImplementedError` in this class; you must override it in your
    descendent class).
    .. note::
        If your overridden :meth:`~PiAnalysisOutput.analyze` method runs slower
        than the required framerate (e.g. 33.333ms when framerate is 30fps)
        then the camera's effective framerate will be reduced. Furthermore,
        this doesn't take into account the overhead of picamera itself so in
        practice your method needs to be a bit faster still.
class MyColorAnalyzer(PiYUVAnalysis):
    The array passed to :meth:`~PiAnalysisOutput.analyze` is organized as
    (rows, columns, channel) where the channel 0 is Y (luminance), while 1 and
    2 are U and V (chrominance) respectively. The chrominance values normally
    have quarter resolution of the luminance values but this class makes all
    channels equal resolution for ease of use.
    """

    def write(self, b):
        super(MyPiYUVAnalysis, self).write(b)
        return self.analyze(self.bytes_to_yuv_raw(b, self.size or self.camera.resolution))
        return result

    def raw_resolution(self, resolution, splitter=False):
        """
        Round a (width, height) tuple up to the nearest multiple of 32 horizontally
        and 16 vertically (as this is what the Pi's camera module does for
        unencoded output).
        """
        width, height = resolution
        if splitter:
            fwidth = (width + 15) & ~15
        else:
            fwidth = (width + 31) & ~31
        fheight = (height + 15) & ~15
        return fwidth, fheight

    def bytes_to_yuv_raw(self, data, resolution):
        """
        Converts a bytes object containing YUV data to a `numpy`_ array.
        """
        width, height = resolution
        fwidth, fheight = self.raw_resolution(resolution)
        y_len = fwidth * fheight
        uv_len = (fwidth // 2) * (fheight // 2)
        if len(data) != (y_len + 2 * uv_len):
            raise PiCameraValueError(
                'Incorrect buffer length for resolution %dx%d' % (width, height))
    # Separate out the Y, U, and V values from the array
        a = np.frombuffer(data, dtype=np.uint8)
        Y = a[:y_len].reshape((fheight, fwidth))
        Uq = a[y_len:-uv_len].reshape((fheight // 2, fwidth // 2))
        Vq = a[-uv_len:].reshape((fheight // 2, fwidth // 2))
    # Reshape the values into two dimensions, and double the size of the
    # U and V values (which only have quarter resolution in YUV4:2:0)
        U = np.empty_like(Y)
        V = np.empty_like(Y)
        U[0::2, 0::2] = Uq
        U[0::2, 1::2] = Uq
        U[1::2, 0::2] = Uq
        U[1::2, 1::2] = Uq
        V[0::2, 0::2] = Vq
        V[0::2, 1::2] = Vq
        V[1::2, 0::2] = Vq
        V[1::2, 1::2] = Vq
        return (Y, U, V)


class MyColorAnalyzer(MyPiYUVAnalysis):
    def __init__(self, camera):
        super(MyColorAnalyzer, self).__init__(camera)
        self.last_color = ''
        self.threshold = Thresholding(32, 32)
        self.count = 0

    def analyze(self, (Y, U, V)):
        # Convert the average color of the pixels in the middle box
        np.set_printoptions(threshold=sys.maxsize, linewidth=1000)
        print(self.count)
        self.count = self.count + 1
#		print(Y.size)
        y_thresholded = self.threshold.with_np_array(Y, True)
#		print(y_thresholded)


with picamera.PiCamera(resolution='32x32', framerate=24) as camera:
    # Fix the camera's white-balance gains
    camera.awb_mode = 'off'
    camera.awb_gains = (1.4, 1.5)
    # # Draw a box over the area we're going to watch
    # camera.start_preview(alpha=128)
    # box = np.zeros((96, 160, 3), dtype=np.uint8)
    # box[30:60, 60:120, :] = 0x80
    # camera.add_overlay(memoryview(box), size=(160, 90), layer=3, alpha=64)
    # # Construct the analysis output and start recording data to it
    with MyColorAnalyzer(camera) as analyzer:
        camera.start_recording(analyzer, 'yuv')
        try:
            i = 0
            while i < 1:
                camera.wait_recording(1)
                i = i + 1
            camera.stop_recording()
        finally:
            pass
#			camera.stop_recording()


# 	def analyze(self, a):
# 		# Convert the average color of the pixels in the middle box
# 		np.set_printoptions(threshold=sys.maxsize, linewidth=1000)
# 		Y = np.dsplit(a, 3)
# 		Y = np.array(Y[0], dtype=np.uint8).reshape(32,32)
# 		print(self.count)
# 		self.count = self.count + 1
# #		print(Y.size)
# 		y_thresholded = self.threshold.with_np_array(Y, True)
# #		print(y_thresholded)
