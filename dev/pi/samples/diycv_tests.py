"""
    This sample is nearly straight from PiCamera examples, it uses Numpy like suggested
    but it is very slow on a single core Pi like the PiZero. You won't get more than 
    3-5 FPS with thresholding and contrast stretching. Max about 10fps without contrast stretching
"""

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import os
import sys
from struct import *
import array
import numpy as np

sys.path.append(os.path.abspath(os.path.join(
    os.path.dirname(__file__), "../libs")))

from diycv.effects.thresholding import Thresholding

height = 128
width = 128
threshold = Thresholding(128,128)
thisdir = os.getcwd() + "/captures/2020-11-30"
print(thisdir)
for r, d, f in os.walk(thisdir):
    for file in f:
        image_name = os.path.join(r, file) 
        size = int(os.stat(image_name).st_size)
        if file.endswith(".data") and size > 0:
            print(image_name)
            stream = open(image_name, 'rb')
            contrast_stretch = True
            thresholded_Y = threshold.with_stream(stream, contrast_stretch)
            U = np.ones((int(height), width))
            V = np.ones((int(height), width))
            YUV = np.dstack((thresholded_Y, U, V))[:int(height), :width, :].astype(np.float)
            # YUV conversion matrix from ITU-R BT.601 version (SDTV)
            #              Y       U       V
            M = np.array([[1.164,  0.000,  1.596],    # R
                        [1.164, -0.392, -0.813],    # G
                        [1.164,  2.017,  0.000]])   # B
            # Take the dot product with the matrix to produce RGB output, clamp the
            # results to byte range and convert to bytes
            RGBT = YUV.dot(M.T).clip(0, 255).astype(np.uint8)
            RGBC = threshold.get_rgb_grayscale(stream)
            # i=Image.fromarray(RGBT,"RGB")
            i= Image.fromarray(np.hstack((RGBC,RGBT)),"RGB")  

            i.save(image_name+'.' + str(contrast_stretch) +'.jpeg', 'JPEG')