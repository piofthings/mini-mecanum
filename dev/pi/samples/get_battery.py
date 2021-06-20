#!/usr/bin/env python3

import os
import sys
import time
import serial
import picamera
import picamera.array
from datetime import datetime
import atexit
import numpy as np
sys.path.append(os.path.abspath(os.path.join(
    os.path.dirname(__file__), "../libs/smokey")))

from smokey_gpio import SmokeyGpio


miniMecanum = None
miniMecanum = SmokeyGpio([17,27,23,24,5,6,26,16])
miniMecanum.get_power_stats()
