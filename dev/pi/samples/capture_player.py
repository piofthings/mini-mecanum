#!/usr/bin/env python3

import cv2
import numpy as np
import os
import time
#from matplotlib import pyplot as plt

thisdir = os.getcwd() + "/captures/2020-12-13-20-28-36"
print (thisdir)

for i in range(1,3132):
    image_name = os.path.join(thisdir, 'grayscale_{:d}.pgm'.format(i)) 
    img = cv2.imread(image_name,-1)
    if img.any():
        height, width = img.shape
        if height > 0 and width > 0:
            print(image_name)
            cv2.imshow('image', img)
            cv2.waitKey(20)
cv2.waitKey(0)
cv2.destroyAllWindows()