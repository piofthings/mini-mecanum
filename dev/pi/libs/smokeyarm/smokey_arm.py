import sys
import os
import time
import board
from board import SCL, SDA
import busio
from adafruit_motor import servo
from adafruit_pca9685 import PCA9685
from adafruit_motorkit import MotorKit

from gpiozero import Button

import threading

class SmokeyArm():
    __currentZ = None 
    __currentHand = None
    __currentShoulder = None
    __currentPulse = None     
    __pca = None
    __maxAngle = 30
    __minAngle = 0
    __currentHandAngle = 0
    __isReversed = False
    __maxShoulderAngle = 65
    __minShoulderAngle = 10

    __mode = 1 # 1 = Calibrate 2 = Challenge
    __stopTime = None

    __armRaiseTimeout = 1.0

    def __init__(self, pca_board, motor, button_gpio, hand_channel, shoulder_channel=None, max_angle=30, min_angle=0, isReversed = False, arm_raise_timeout = 1.0):
        self.__pca = pca_board
        self.__currentHand = hand_channel ##servo.Servo(self.__pca.channels[hand_channel])
        if shoulder_channel != None:
            self.__currentShoulder = shoulder_channel #servo.Servo(self.__pca.channels[shoulder_channel])
        self.__currentZ = motor
        self.__currentPulse = Button(button_gpio)       
        self.__maxAngle = max_angle
        self.__minAngle = min_angle
        self.__isReversed = isReversed
        self.__armRaiseTimeout = arm_raise_timeout
        self.pinch_hand() 

    def pinch_hand(self):
        if self.__isReversed:
            self.__currentHand.angle = self.__maxAngle
        else:
            self.__currentHand.angle = self.__minAngle
        time.sleep(0.5)

    def release_hand(self):
        if self.__isReversed:
            for i in range(self.__maxAngle, self.__minAngle, -1):
                self.__currentHand.angle = i
                time.sleep(0.05)
        else:
            for i in range(self.__maxAngle):
                self.__currentHand.angle = i
                time.sleep(0.05)

    def grab_hand(self):
        if self.__isReversed:
            for i in range(self.__maxAngle, self.__minAngle, -1):
                if self.__currentPulse.is_pressed:
                    print("Button is pressed")
                    self.__currentHand.angle = self.__currentHand.angle 
                    time.sleep(0.05)
                    break            
                else:
                    self.__currentHand.angle = self.__maxAngle - i
                    time.sleep(0.05)            

        else:
            for i in range(self.__maxAngle):
                if self.__currentPulse.is_pressed:
                    print("Button is pressed")
                    self.__currentHand.angle = self.__currentHand.angle + 2
                    time.sleep(0.05)
                    break            
                else:
                    self.__currentHand.angle = self.__maxAngle - i
                    time.sleep(0.05)
            
    def arm_wide(self):
        if self.__isReversed:
            self.__currentShoulder.angle = self.__maxShoulderAngle
        else:
            self.__currentShoulder.angle = self.__minShoulderAngle
        time.sleep(0.05)

    def arm_hug(self):
        if self.__isReversed:
            self.__currentShoulder.angle = self.__minShoulderAngle
        else:
            self.__currentShoulder.angle = self.__maxShoulderAngle
        time.sleep(0.05)

    def raise_arm(self):
        if self.__mode == 1:
            self.__currentZ.throttle = 1.0
            time.sleep(0.5)
            self.__currentZ.throttle = 0.0
        else:
            self.__currentZ.throttle = 1.0
            timer = threading.Timer(self.__armRaiseTimeout, self.stop_arm)
            timer.start()  

    def stop_arm(self):
        self.__currentZ.throttle = 0.0

    def lower_arm(self):
        self.__currentZ.throttle = -1.0
        time.sleep(0.5)
        self.__currentZ.throttle = 0.0

    def set_mode(self, mode):
        self.__mode = mode

    def get_mode(self):
        return self.__mode



    