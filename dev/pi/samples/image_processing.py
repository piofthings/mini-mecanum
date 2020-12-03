from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import sys
from struct import *
import array
import numpy as np

 
image_name = "captures/2020-11-30/image0.data"
width = 128
height = 128

print ("width=" + str(width) + "height=" + str(height))

stream = open(image_name, 'rb')
# Capture the image in YUV format
# with picamera.PiCamera() as camera:
#     camera.resolution = (width, height)
#     camera.start_preview()
#     time.sleep(2)
#     camera.capture(stream, 'yuv')
# Rewind the stream for reading
stream.seek(0)
# Calculate the actual image size in the stream (accounting for rounding
# of the resolution)
fwidth = 128 #(width + 31) // 32 * 32
fheight = 128 #(height + 15) // 16 * 16
# Load the Y (luminance) data from the stream
Y = np.fromfile(stream, dtype=np.uint8, count=fwidth*fheight).\
        reshape((fheight, fwidth))
# Use dummy UV (chrominance) data for grayscale image
U = np.ones((fheight, fwidth))
V = np.ones((fheight, fwidth))
# Stack the YUV channels together, crop the actual resolution, convert to
# floating point for later calculations, and apply the standard biases

YUV = np.dstack((Y, U, V))[:height, :width, :].astype(np.float)

# YUV conversion matrix from ITU-R BT.601 version (SDTV)
#              Y       U       V
M = np.array([[1.164,  0.000,  1.596],    # R
              [1.164, -0.392, -0.813],    # G
              [1.164,  2.017,  0.000]])   # B
# Take the dot product with the matrix to produce RGB output, clamp the
# results to byte range and convert to bytes
RGBG = YUV.dot(M.T).clip(0, 255).astype(np.uint8)
stream.seek(0)
Y = np.fromfile(stream, dtype=np.uint8, count=fwidth*fheight).\
        reshape((fheight, fwidth))
# Load the UV (chrominance) data from the stream, and double its size
U = np.fromfile(stream, dtype=np.uint8, count=(fwidth//2)*(fheight//2)).\
        reshape((fheight//2, fwidth//2)).\
        repeat(2, axis=0).repeat(2, axis=1)
V = np.fromfile(stream, dtype=np.uint8, count=(fwidth//2)*(fheight//2)).\
        reshape((fheight//2, fwidth//2)).\
        repeat(2, axis=0).repeat(2, axis=1)
YUV = np.dstack((Y, U, V))[:height, :width, :].astype(np.float)
YUV[:, :, 0]  = YUV[:, :, 0]  - 16   # Offset Y by 16
YUV[:, :, 1:] = YUV[:, :, 1:] - 128  # Offset UV by 128
# YUV conversion matrix from ITU-R BT.601 version (SDTV)
#              Y       U       V
M = np.array([[1.164,  0.000,  1.596],    # R
              [1.164, -0.392, -0.813],    # G
              [1.164,  2.017,  0.000]])   # B
# Take the dot product with the matrix to produce RGB output, clamp the
# results to byte range and convert to bytes
RGBC = YUV.dot(M.T).clip(0, 255).astype(np.uint8)
i=Image.fromarray(np.hstack((RGBC,RGBG)),"RGB")

i.show()