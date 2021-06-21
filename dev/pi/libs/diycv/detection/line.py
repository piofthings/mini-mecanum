import os
import sys
from struct import *
import array
import traceback


sys.path.append(os.path.abspath(os.path.join(
    os.path.dirname(__file__), "../models")))

from frame_data import FrameData
from row_data import RowData


class Line():
    __frame_processor_queue = None
    top_speed = 230
    half_speed = 50
    __set_speed_func = None
    ideal_center = -1
    prev_frame_data = None

    def __init__ (self, queue, set_speed = None):
        self.__frame_processor_queue = queue
        self.__set_speed_func = set_speed


    def process_bytearray(self, data, width, height, thresh=True, stretch=True, index = -1):
        y = 0
        out = []
        frame_data = FrameData()
        frame_data.index = index
        frame_data.width = width
        frame_data.height = height
        self.ideal_center = frame_data.width/2
        average_out=[]
        average_out = [0 for i in range(width)]         
        contiguous_whitepixel_count = [0 for i in range(height)]         

        try:
            while y < height:
                row_white_count = 0
                prev_col_is_white = False
                row_data = RowData()

                row = memoryview(data)[y*width:(y+1)*width]
                if stretch:
                    minval = 255
                    maxval = 0
                    for val in row:
                        if val < minval:
                            minval = val
                        if val > maxval:
                            maxval = val

                    diff = maxval - minval

                    factor = 1
                    if diff != 0:
                        factor = 255/diff

                x = 0
                for val in row:
                    if stretch:
                        val = int((val - minval) * factor)
                    if thresh:
                        if val > 96:
                            val = 255
                        else:
                            val = 0
                        row[x] = val
                    else:
                        row[x] = val

                    average_out[x] = (average_out[x] + val)
                    if( y == height - 1):
                        average_out[x] = int(average_out[x] / height)

                    if val == 255:
                        if prev_col_is_white == False:
                            prev_col_is_white = True
                            row_white_count = row_white_count + 1
                    else:
                        prev_col_is_white = False
                    
                    x = x + 1
                contiguous_whitepixel_count[y] = row_white_count
                row_data.contiguous_whitepixel_count = contiguous_whitepixel_count
                y = y + 1
                out.append(row.tolist())
            # if self.__frame_processor_queue  != None:
            if self.__set_speed_func  != None:
                frame_data.rows = out
                self.nomalize_avg(average_out, width)
                frame_data.average_row = average_out
                self.get_shape(height, frame_data, contiguous_whitepixel_count)
                self.calculate_speed(frame_data)
                # self.__frame_processor_queue.put(frame_data, block=True, timeout=0.5)
                self.prev_frame_data = frame_data
                self.__set_speed_func(frame_data)
        except Exception as e:
                print(e)
                traceback.print_exc()

    def get_shape(self, height, frame_data, contiguous_whitepixel_count):
        starts_with = -1
        ends_with = 0
        max = 0
        min = height
        for row in range(0, height):
            if contiguous_whitepixel_count[row] == 0:
                pass
            else:
                if row < 5 or starts_with == -1:                
                    starts_with = contiguous_whitepixel_count[row]
                elif row > height - 5:
                    ends_with = contiguous_whitepixel_count[row]
            if contiguous_whitepixel_count[row] > max:
                max = contiguous_whitepixel_count[row]
            if contiguous_whitepixel_count[row] < min:
                min = contiguous_whitepixel_count[row]
        if max == 1:
            frame_data.is_straight = True
        else:
            frame_data.is_straight = False

            if starts_with > 1 and ends_with == 1:
                frame_data.is_fork = True
            if starts_with == 1 and ends_with > 1:
                frame_data.is_join = True
                frame_data.is_fork = True
            if starts_with == 1 and ends_with == 1 and max > starts_with:
                frame_data.is_join = True
                frame_data.is_fork = True

    def nomalize_avg(self, average_row, width):
        for col in range(0, width - 1):
            if (average_row[col] > 94):
                average_row[col] = 255
            # if(average_row[col] < 100 and average_row[col] > 9):
            #     average_row[col] = 128
            # elif (average_row[col] < 10):
            #     average_row[col] = 0
            # elif (average_row[col] > 99):
            #     average_row[col] = 255
    def set_top_speed(self, thickness):
        speed = 0
        if thickness > 3 and thickness < 14:
            speed = self.top_speed
        elif thickness < 3 or thickness > 25:
             speed = int(self.top_speed / 2)
        else:
            speed = self.half_speed
        return speed

    def calculate_speed(self, frame_data):
        try:        
            first_white_pos = 0
            last_white_pos = 0
            current_pos_white = False
            prev_post_white = False
            speed = 0
            first_grey_pos = 0
            last_grey_pos = 0
            for pos in range(0,frame_data.width):
                if frame_data.average_row[pos] == 255:
                    if first_white_pos == 0:
                        first_white_pos = pos
                    else:
                        last_white_pos = pos
                    current_pos_white = True
                else:
                    prev_post_white = current_pos_white
                    current_pos_white = False
                    if frame_data.average_row[pos] > 50:
                        if first_grey_pos == 0:
                            first_grey_pos = pos
                        if pos > last_grey_pos:
                            last_grey_pos = pos
            thickness = last_white_pos - first_white_pos + 1
            speed = self.set_top_speed(thickness)
            if  thickness > 1:
                
                #good thickness

                ratio = (first_white_pos + (thickness/2) )/self.ideal_center 
                frame_data.ratio = ratio
                # 0 0 0 0 0 0 1 1 1 1 0 0 0 0 0 0 | ideal, ratio = 1
                # 0 0 1 1 1 1 0 0 0 0 0 0 0 0 0 0 | move left wheels faster, ratio > 1
                # 0 0 0 0 0 0 0 0 0 0 1 1 1 1 0 0 | move right wheels faster, ratio < 1
            else:
                #speed = self.half_speed
                frame_data.speedL = 0
                frame_data.speedR = 0
                thickness = last_grey_pos - first_grey_pos # ????????????
                if thickness > 0:
                    grey_center = thickness/2
                    ratio = (first_grey_pos + (thickness/2) )/self.ideal_center
                    frame_data.ratio = ratio
                else:
                    ratio = self.prev_frame_data.ratio
                    frame_data.ratio = ratio
                    speed = int(self.top_speed / 2)
                if first_grey_pos > (frame_data.width - last_grey_pos):
                    frame_data.veer_right = True
                else:
                    frame_data.veer_left = True
            if ratio > 1:
                frame_data.speedR = int(speed/ratio)
                frame_data.speedL = speed
            elif ratio < 1:
                frame_data.speedR = speed
                frame_data.speedL = int(speed * ratio)
            else :
                frame_data.speedL = speed
                frame_data.speedR = speed

            frame_data.first_white_pos = first_white_pos
            frame_data.last_white_pos = last_white_pos
            frame_data.thickness = thickness
        except Exception as e:
                print(e)
                traceback.print_exc()


