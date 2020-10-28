#!/usr/bin/env python3

import os
import sys
import time
import serial

sys.path.append(os.path.abspath(os.path.join(
    os.path.dirname(__file__), "../libs/smokey")))

from smokey import Smokey

miniMecanum = Smokey()

miniMecanum.set_speed(64)
time.sleep(5)
miniMecanum.set_speed(128)
time.sleep(5)
miniMecanum.set_speed(0)
#miniMecanum.set_direction(-1)
miniMecanum.set_speed(-64)
time.sleep(5)
miniMecanum.set_speed(-128)
time.sleep(5)
miniMecanum.set_speed(0)

