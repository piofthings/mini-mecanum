
#!/usr/bin/env python3

import os
import sys

# from smbus2 import SMBus
import serial
import time

"""
Smokey is a Python library that talks to an Arduino over UART.
It works in conjuction with arduino/smokey library in this repository

0x1 = Set Speed
        data = 0 to 255
0x2 = Set Direction
        data = 1 Forward, -1 Backwards
0x3 = Turn factor
        -10 = strafe left
          0 = go straight
        +10 = strafe right
""" 
class Smokey:
        __isDebug = False
        __ser = None

        def __init__(self, isDebug=False):
                self.__isDebug = isDebug
                self.__ser = serial.Serial('/dev/ttyS0', 115200, timeout=1)
                self.__ser.flush()


        def set_speed(self, speed):
                data  = "1:" + str(speed) + "\n"
                print(data.encode('utf-8'))
                self.__ser.write(data.encode('utf-8'))
                line = self.__ser.readline().decode('utf-8').rstrip()
                print(line) 
       
        def set_direction(self, direction):
                data  = "2:" + str(direction) + "\n"
                print(data.encode('utf-8'))
                self.__ser.write(data.encode('utf-8'))
                line = self.__ser.readline().decode('utf-8').rstrip()
                print(line) 

        def set_speed_LR(self, speedLeft, speedRight):
                data  = "3:" + str(speedLeft) + "," + str(speedRight) "\n"
                print(data.encode('utf-8'))
                self.__ser.write(data.encode('utf-8'))
                line = self.__ser.readline().decode('utf-8').rstrip()
                print(line) 

        def set_speed_LfLrRfRr(self, speedLeftFront, speedRight):
                data  = "3:" + str(speedLeft) + "," + str(speedRight) "\n"
                print(data.encode('utf-8'))
                self.__ser.write(data.encode('utf-8'))
                line = self.__ser.readline().decode('utf-8').rstrip()
                print(line) 


#        def turn(self, turn_factor):
                # data = [0x3, turn_factor]
                # self.__bus.write_i2c_block_data(self.__addr, 0, data)

#        def test(self, light_status):
                # bus.write(self.__addr, 0, light_status)


