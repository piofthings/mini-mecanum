from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import os
import sys
from struct import *
import array
import numpy as np

class Thresholding:
        __width = 0
        __height = 0
        __stream = None
        def __init__(self, width, height):
                self.__width = width
                self.__height = height

        def with_stream(self, stream, stretch_contrast=False):
                stream.seek(0)
                # Load the Y (luminance) data from the stream

                Y = np.fromfile(stream, dtype=np.uint8, count=self.__width*self.__height).\
                        reshape((self.__height, self.__width))
                return self.with_np_array(Y, stretch_contrast)

        def min_max(self, row, row_width):
                min = row[0]
                max = row[0]
                for r in range(1, row_width):
                        c = row[r]
                        if(c < min):
                                min = c
                        if(c > max):
                                max = c

                return (min, max)


        def with_np_array(self, y_array, stretch_contrast=False):
                #np.set_printoptions(threshold=sys.maxsize, linewidth=1000) 

                (y_height, y_width) = y_array.shape
                thresholded = np.empty((y_height, y_width), dtype=np.uint8)
                r = 0 
                c = 0
                ratio = 1
                for r in range(0, y_height): # y_array:
                        if stretch_contrast:
                                row = y_array[r]
                                (darkest, brightest) = self.min_max(row, y_width)
                                #darkest = np.min(row) #.argmin()
                                #brightest = np.max(row) #.argmax()
                                diff = brightest - darkest #row[brightest] - row[darkest]
                                ratio = int(255/diff)

                        c=0
                        for c in range(0, y_width): #pixel in row:
                                pixel = y_array[r,c]
                                if stretch_contrast:
                                        pixel = (pixel - darkest) * ratio
                                if pixel < 136:
                                        thresholded[r,c] = 1
                                else:
                                        thresholded[r,c] = 255
                return thresholded

        def get_rgb_grayscale(self, stream):
            stream.seek(0)
            Y = np.fromfile(stream, dtype=np.uint8, count=self.__width*self.__height).\
                    reshape((self.__height, self.__width))
            U = np.ones((self.__height, self.__width))
            V = np.ones((self.__height, self.__width))
            YUV = np.dstack((Y, U, V))[:self.__height, :self.__width, :].astype(np.float)
            M = np.array([[1.164,  0.000,  1.596],    # R
                        [1.164, -0.392, -0.813],    # G
                        [1.164,  2.017,  0.000]])   # B
            RGBG = YUV.dot(M.T).clip(0, 255).astype(np.uint8)
            stream.seek(0)
            Y = np.fromfile(stream, dtype=np.uint8, count=self.__width*self.__height).\
                    reshape((self.__height, self.__width))
            # Load the UV (chrominance) data from the stream, and double its size
            U = np.fromfile(stream, dtype=np.uint8, count=(self.__width//2)*(self.__height//2)).\
                    reshape((self.__height//2, self.__width//2)).\
                    repeat(2, axis=0).repeat(2, axis=1)
            V = np.fromfile(stream, dtype=np.uint8, count=(self.__width//2)*(self.__height//2)).\
                    reshape((self.__height//2, self.__width//2)).\
                    repeat(2, axis=0).repeat(2, axis=1)
            YUV = np.dstack((Y, U, V))[:self.__height, :self.__width, :].astype(np.float)
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
            return i








