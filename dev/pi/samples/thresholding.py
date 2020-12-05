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
stream.seek(0)
fwidth = 128 #(width + 31) // 32 * 32
fheight = 128 #(height + 15) // 16 * 16
# Load the Y (luminance) data from the stream
Y = np.fromfile(stream, dtype=np.uint8, count=fwidth*fheight).\
        reshape((fheight, fwidth))
np.set_printoptions(threshold=sys.maxsize, linewidth=1000) 

y = Y[64: , : ]
print(y)
