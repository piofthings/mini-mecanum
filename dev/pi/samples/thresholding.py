from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import sys
from struct import *
import array
import numpy as np

class Threshold:
        __width = 0
        __height = 0
        __stream = None
        def __init__(self, width, height):
                __width = width
                __height = height

        def run(self, stream):
                stream.seek(0)
                fwidth = 128 #(width + 31) // 32 * 32
                fheight = 128 #(height + 15) // 16 * 16
                # Load the Y (luminance) data from the stream
                Y = np.fromfile(stream, dtype=np.uint8, count=fwidth*fheight).\
                        reshape((fheight, fwidth))
                np.set_printoptions(threshold=sys.maxsize, linewidth=1000) 

                #Take the lower 50% only
                y = Y[int(width/2): , : ]
                print(y)

if __name__ == '__main__':
        threshold = Threshold(128,128)
        thisdir = os.getcwd() + "captures/2020-11-30"
        for r, d, f in os.walk(thisdir):
                for file in f:
                        if file.endswith(".data"):
                                image_name = os.path.join(r, file) #"captures/2020-12-05-21-28-12/image0.data"
                                stream = open(image_name, 'rb')
                                threshold.run()


