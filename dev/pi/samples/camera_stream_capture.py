import picamera
import numpy as np
from picamera.array import PiYUVAnalysis
from picamera.color import Color

class MyColorAnalyzer(PiYUVAnalysis):
	def __init__(self, camera):
		super(MyColorAnalyzer, self).__init__(camera)
		self.last_color = ''

	def analyze(self, a):
		# Convert the average color of the pixels in the middle box
		print(a)
		print(a.shape)


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
			while True:
		    	camera.wait_recording(1)
		finally:
			camera.stop_recording()