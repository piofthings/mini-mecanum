#!/usr/bin/env python3

import os
import sys

from smbus2 import SMBus

"""
Smokey is a Python library that talks to an Arduino over I2C.
It works in conjuction with adruino/smokey library in this repository

0x1 = Set Speed
        data = 0 to 255
0x2 = Set Direction
        data = 1 Forward, 2 Backwards
0x3 = Turn factor
        -10 = strafe left
          0 = go straight
        +10 = strafe right
""" 
class Smokey:
        __addr = 0x8
        __bus = None
        __isDebug = False

        def __init__(self, isDebug=False):
                self.__bus = SMBus(1) # indicates /dev/ic2-1
                self.__isDebug = isDebug


        def set_speed(self, speed):
                data  = [0x1, speed]
                self.__bus.write_i2c_block_data(self.__addr, 0, data)

        def set_direction(self, direction):
                data = [0x2, direction]
                self.__bus.write_i2c_block_data(self.__addr, 0, data)

        def turn(self, turn_factor):
                data = [0x3, turn_factor]
                self.__bus.write_i2c_block_data(self.__addr, 0, data)

        def test(self, light_status)
                bus.write(self.__addr, 0, light_status)
