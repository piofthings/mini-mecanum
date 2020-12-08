import os
import sys
import picamera
import numpy as np
from picamera.array import PiYUVAnalysis
from picamera.color import Color
import numpy as np
sys.path.append(os.path.abspath(os.path.join(
    os.path.dirname(__file__), "../libs")))

from diycv.effects.thresholding import Thresholding

class MyColorAnalyzer(PiYUVAnalysis):
	def __init__(self, camera):
		super(MyColorAnalyzer, self).__init__(camera)
		self.last_color = ''
		self.threshold = Thresholding(32,32)

	def analyze(self, a):
		# Convert the average color of the pixels in the middle box
		np.set_printoptions(threshold=sys.maxsize, linewidth=1000)
		#print(a)
		Y = np.dsplit(a, 1).reshape(32,32)
		y_thresholded = self.threshold.with_np_array(Y, True)
		print(y_thresholded)

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
				camera.wait_recordin	(1)
				i = i + 	
			camera.stop_recording()
		finally:
			camera.stop_recording()	