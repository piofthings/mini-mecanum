import os
import sys

sys.path.append(os.path.abspath(os.path.join(
    os.path.dirname(__file__), "../libs/bno55")))

from bno55 import BNO055

import time


bno = BNO055()

# Initialize the BNO055 and stop if something went wrong.
if not bno.begin():
    raise RuntimeError('Failed to initialize BNO055! Is the sensor connected?')

out = True
while out:
    time.sleep(1)
    # Read the Euler angles for heading, roll, pitch (all in degrees).
    heading, roll, pitch = bno.getVector(0x1A)
    # Read the calibration status, 0=uncalibrated and 3=fully calibrated.
    sys, gyro, accel, mag = bno.getCalibration()
    # Print everything out.
    #print(.format(
    #      heading, roll, pitch, sys, gyro, accel, mag))
    # Other values you can optionally read:
    # Orientation as a quaternion:
    x,y,z,w = bno.getQuat()
    print('{:0.4F},{:0.4F},{:0.4F},{},{},{},{},{},{},{},{}'.format(heading, roll, pitch, sys, gyro, accel, mag,x,y,z,w))
    # Sensor temperature in degrees Celsius:
    #temp_c = bno.read_temp()
    # Magnetometer data (in micro-Teslas):
    #x,y,z = bno.read_magnetometer()
    # Gyroscope data (in degrees per second):
    #x,y,z = bno.read_gyroscope()
    # Accelerometer data (in meters per second squared):
    #x,y,z = bno.read_accelerometer()
    # Linear acceleration data (i.e. acceleration from movement, not gravity--
    # returned in meters per second squared):
    #x,y,z = bno.read_linear_acceleration()
    # Gravity acceleration data (i.e. acceleration just from gravity--returned
    # in meters per second squared):
    #x,y,z = bno.read_gravity()
    # Sleep for a second until the next reading.
    out = False


