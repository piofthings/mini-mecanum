from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import os
import sys
from struct import *
import array
import numpy as np

class Threshold:
        __width = 0
        __height = 0
        __stream = None
        def __init__(self, width, height):
                self.__width = width
                self.__height = height

        def run(self, stream):
                stream.seek(0)
                # Load the Y (luminance) data from the stream

                Y = np.fromfile(stream, dtype=np.uint8, count=self.__width*self.__height).\
                        reshape((self.__height, self.__width))
                np.set_printoptions(threshold=sys.maxsize, linewidth=1000) 

                #Take the lower 50% only
                y = Y[int(self.__height/2): , : ]
                (y_height, y_width) = Y.shape
                thresholded = np.arange(y_height * y_width).reshape(y_height, y_width)
                r = 0 
                c = 0
                for row in Y:
                    darkest = row.argmin()
                    brightest = row.argmax()
                    diff = brightest - darkest
                    c=0
                    for pixel in row:
                        #pixel = (pixel - darkest) * (255 /diff)
                        if pixel < 136:
                            thresholded[r,c] = 1
                        else:
                            thresholded[r,c] = 255
                        c = c+1
                    r = r+1
                #print(thresholded)
                return thresholded

        def get_rgb_grayscale(self, stream):
            stream.seek(0)
            width = 128 #(width + 31) // 32 * 32
            height = 128 #(height + 15) // 16 * 16
            Y = np.fromfile(stream, dtype=np.uint8, count=width*height).\
                    reshape((height, width))
            np.set_printoptions(suppress=True, threshold=width*height, linewidth=width*4)
            U = np.ones((height, width))
            V = np.ones((height, width))
            YUV = np.dstack((Y, U, V))[:height, :width, :].astype(np.float)
            M = np.array([[1.164,  0.000,  1.596],    # R
                        [1.164, -0.392, -0.813],    # G
                        [1.164,  2.017,  0.000]])   # B
            RGBG = YUV.dot(M.T).clip(0, 255).astype(np.uint8)
            stream.seek(0)
            Y = np.fromfile(stream, dtype=np.uint8, count=width*height).\
                    reshape((height, width))
            # Load the UV (chrominance) data from the stream, and double its size
            U = np.fromfile(stream, dtype=np.uint8, count=(width//2)*(height//2)).\
                    reshape((height//2, width//2)).\
                    repeat(2, axis=0).repeat(2, axis=1)
            V = np.fromfile(stream, dtype=np.uint8, count=(width//2)*(height//2)).\
                    reshape((height//2, width//2)).\
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
            return i



if __name__ == '__main__':
        height = 128
        width = 128
        threshold = Threshold(128,128)
        thisdir = os.getcwd() + "/captures/2020-11-30"
        print(thisdir)
        for r, d, f in os.walk(thisdir):
                for file in f:
                        image_name = os.path.join(r, file) 
                        size = int(os.stat(image_name).st_size)
                        if file.endswith(".data") and size > 0:
                                print(image_name)
                                stream = open(image_name, 'rb')
                                thresholded_Y = threshold.run(stream)
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

                                i.save(image_name+'.thresholded.jpeg', 'JPEG')




