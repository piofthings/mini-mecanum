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

from smokey import Smokey


miniMecanum = None
miniMecanum = Smokey()
miniMecanum.get_power_stats()