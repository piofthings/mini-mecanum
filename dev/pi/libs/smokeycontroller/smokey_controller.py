
import sys
import os
import time

sys.path.append(os.path.abspath(os.path.join(
    os.path.dirname(__file__), "../")))

from keyboardcontroller.keyboard_controller import KeyboardController
from smokey.smokey_gpio import SmokeyGpio

import board
from board import SCL, SDA
import busio
from adafruit_motor import servo
from adafruit_pca9685 import PCA9685
from adafruit_motorkit import MotorKit

from gpiozero import Button

from smokeyarm.smokey_arm import SmokeyArm

class SmokeyController():
    __keyboardController =  None
    __smokeyGpio = None
    __currentSpeed = 125
    __i2c = busio.I2C(SCL, SDA)

    __pca = PCA9685(__i2c)
    __pca.frequency = 50

    __greenArm = None 
    __redArm = None
    __blueArm = None
    __currentArm = None

    __currentlySelectedArm = None

    __kit = MotorKit(i2c=board.I2C())

    __max_angle = 36
    __min_angle = 0

    __min_speed = 64


    def __init__(self, smokeyGpio, exit_condition):
        self.__keyboardController = KeyboardController(exit_condition)
        
        self.__smokeyGpio = smokeyGpio
        self.__greenArm = SmokeyArm(self.__pca, self.__kit.motor3, 12, servo.Servo(self.__pca.channels[2]), servo.Servo(self.__pca.channels[5]), 30, 0, False, 2)
        self.__redArm   = SmokeyArm(self.__pca, self.__kit.motor2, 22, servo.Servo(self.__pca.channels[1]))
        self.__blueArm  = SmokeyArm(self.__pca, self.__kit.motor1, 21, servo.Servo(self.__pca.channels[0]), servo.Servo(self.__pca.channels[4]), 30, 0, True, 1)

    def start(self):
        done_processing = False
        input_str = ""
        while not done_processing:
            if self.__keyboardController.input_queued():
                input_str = self.__keyboardController.input_get()
                print(input_str + '\n')
                if input_str.strip() == "quit":
                    done_processing = True
                elif input_str.strip() == "w":
                    self.go_straight_forwards()  # go straight forward
                elif input_str.strip() == "s":
                    self.go_straight_backwards() # go straight back
                elif input_str.strip() == "a":   # strafe left
                    self.strafe_left()
                elif input_str.strip() == "d":   # strafe right
                    self.strafe_right()
                elif input_str.strip() == 'q':   # diagonal left forward
                    self.diagonal_left_forward()
                elif input_str.strip() == 'e':   # diagonal right forward
                    self.diagonal_right_forward()
                elif input_str.strip() == 'z':   # diagonal right reverse
                    self.diagonal_right_reverse()
                elif input_str.strip() == 'c':   # diagonal left reverse
                    self.diagonal_left_reverse()
                elif input_str.strip() == 'y':   # spin clockwise
                    self.spin_clockwise()
                elif input_str.strip() == 't':   # spin anti-clockwise
                    self.spin_anticlockwise()
                elif input_str.strip() == 'r':   # select Red Arm
                    self.select_red_arm()
                elif input_str.strip() == 'g':   # select Green  Arm
                    self.select_green_arm()
                elif input_str.strip() == 'b':   # select Blue  Arm
                    self.select_blue_arm()
                elif input_str.strip() == 'o':   # Release hand
                    if self.__currentArm != None:
                        self.__currentArm.release_hand()
                elif input_str.strip() == 'p':   # Pinch Hand
                    if self.__currentArm != None:
                        self.__currentArm.pinch_hand()                                        
                elif input_str.strip() == 'l':   # Grab Hand
                    if self.__currentArm != None:
                        self.__currentArm.grab_hand()                                        
                elif input_str.strip() == '\'':   # Raise selected arm
                    if self.__currentArm != None:
                        self.__currentArm.raise_arm()
                elif input_str.strip() == '/':   # Lower selected arm
                    if self.__currentArm != None:
                        self.__currentArm.lower_arm()
                elif input_str.strip() == 'h':   # Swing arm inwards
                    if self.__currentArm != None:
                        self.__currentArm.arm_hug()
                elif input_str.strip() == 'j':   # Swing arm outwards
                    if self.__currentArm != None:
                        self.__currentArm.arm_wide()     
                elif input_str == "1": #Calibration mode
                    self.__blueArm.set_mode(1)
                    self.__redArm.set_mode(1)
                    self.__greenArm.set_mode(1)
                elif input_str == "2": #Challenge mode
                    self.__blueArm.set_mode(2)
                    self.__redArm.set_mode(2)
                    self.__greenArm.set_mode(2)
                elif input_str == "0": #STOP
                    self.increase_speed(0)
                elif input_str == "`": #STOP and quit
                    self.increase_speed(0)
                    done_processing = True
                    self.__keyboardController.clear()

    def select_blue_arm(self):
        print("\r\n\ Select CurrentArm: Blue")
        self.__currentArm = self.__blueArm

    def select_green_arm(self):
        self.__currentArm = self.__greenArm

    def select_red_arm(self):
        self.__currentArm = self.__redArm


    def increase_speed(self, speed):
        if(speed < 256 and speed > -1):
            self.__currentSpeed = speed
        
        self.__smokeyGpio.set_speed(self.__currentSpeed)

    def go_straight_forwards(self):
        self.__currentSpeed = self.__currentSpeed - 4
        self.__smokeyGpio.set_speed_LfLrRfRr(self.__currentSpeed, self.__currentSpeed, self.__currentSpeed, self.__currentSpeed)

    def go_straight_backwards(self):
        self.__currentSpeed = self.__currentSpeed - 4
        self.__smokeyGpio.set_speed_LfLrRfRr(self.__currentSpeed, self.__currentSpeed, self.__currentSpeed, self.__currentSpeed)

    def strafe_right(self):
        self.__smokeyGpio.set_speed_LfLrRfRr(self.__currentSpeed, -self.__currentSpeed, -self.__currentSpeed, self.__currentSpeed)

    def strafe_left(self):
        self.__smokeyGpio.set_speed_LfLrRfRr(-self.__currentSpeed, self.__currentSpeed, self.__currentSpeed, -self.__currentSpeed)
    
    def diagonal_left_forward(self):
        self.__smokeyGpio.set_speed_LfLrRfRr(self.__currentSpeed, 0, 0, self.__currentSpeed)

    def diagonal_right_forward(self):
        self.__smokeyGpio.set_speed_LfLrRfRr(0, self.__currentSpeed, self.__currentSpeed, 0)
    
    def diagonal_left_reverse(self):
        self.__smokeyGpio.set_speed_LfLrRfRr(-self.__currentSpeed, 0, 0, -self.__currentSpeed)

    def diagonal_right_reverse(self):
        self.__smokeyGpio.set_speed_LfLrRfRr(0, -self.__currentSpeed, -self.__currentSpeed, 0)

    def spin_clockwise(self):
        self.__smokeyGpio.set_speed_LfLrRfRr(self.__currentSpeed, self.__currentSpeed, -self.__currentSpeed, -self.__currentSpeed)

    def spin_anti_clockwise(self):
        self.__smokeyGpio.set_speed_LfLrRfRr(-self.__currentSpeed, -self.__currentSpeed, self.__currentSpeed, self.__currentSpeed)


    def dispose(self):
        self.__pca.deinit()
