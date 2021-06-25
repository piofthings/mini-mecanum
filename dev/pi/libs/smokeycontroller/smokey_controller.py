
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


class SmokeyController():
    __keyboardController =  None
    __smokeyGpio = None
    __currentSpeed = 125
    __i2c = busio.I2C(SCL, SDA)

    __pca = PCA9685(__i2c)
    __pca.frequency = 50

    __currentZ = None 
    __currentArm = None
    __currentShoulder = None
    __currentPulse = None 

    __greenButton = None 
    __redButton = None
    __blueButton = None

    __kit = MotorKit(i2c=board.I2C())

    __max_angle = 36
    __min_angle = 0


    def __init__(self, smokeyGpio, exit_condition):
        self.__keyboardController = KeyboardController(exit_condition)
        self.__smokeyGpio = smokeyGpio
        self.__greenButton = Button(12)
        self.__blueButton = Button(21)
        self.__redButton = Button(8)

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
                    self.release_current_hand()
                elif input_str.strip() == 'p':   # Pinch Hand
                    self.pinch_current_hand()                                        
                elif input_str.strip() == 'l':   # Grab Hand
                    self.grab_current_hand()                                        
                elif input_str.strip() == '\'':   # Raise selected arm
                    self.raise_selected_arm()
                elif input_str.strip() == '/':   # Lower selected arm
                    self.lower_selected_arm()
                elif input_str == "0": #STOP
                    self.increase_speed(0)
                elif input_str == "`": #STOP and quit
                    self.increase_speed(0)
                    done_processing = True
                    self.__keyboardController.clear()

    def select_blue_arm(self):
        self.__currentArm = servo.Servo(self.__pca.channels[0])
        self.__currentShoulder = servo.Servo(self.__pca.channels[4])
        self.__currentZ = self.__kit.motor1
        self.__currentPulse = self.__blueButton

    def select_green_arm(self):
        self.__currentArm = servo.Servo(self.__pca.channels[1])
        self.__currentShoulder = servo.Servo(self.__pca.channels[5])
        self.__currentZ = self.__kit.motor3
        self.__currentPulse = self.__blueButton

    def select_red_arm(self):
        self.__currentArm = servo.Servo(self.__pca.channels[2])
        self.__currentShoulder = None
        self.__currentZ = self.__kit.motor2
        self.__currentPulse = self.__redButton

    def pinch_current_hand(self):
        self.__currentArm.angle = 0
        time.sleep(0.5)

    def release_current_hand(self):
        for i in range(self.__max_angle):
            self.__currentArm.angle = i
            time.sleep(0.05)

    def grab_current_hand(self):
        for i in range(self.__max_angle):
            if self.__currentPulse.is_pressed:
                print("Button is pressed")
                self.__currentArm.angle = self.__currentArm.angle + 3
                time.sleep(0.05)
                break            
            else:
                self.__currentArm.angle = self.__max_angle - i
                time.sleep(0.05)

    def raise_selected_arm(self):
        self.__currentZ.throttle = 1.0
        time.sleep(0.5)
        self.__currentZ.throttle = 0.0


    def lower_selected_arm(self):
        self.__currentZ.throttle = -1.0
        time.sleep(0.5)
        self.__currentZ.throttle = 0.0

    def increase_speed(self, speed):
        if(speed < 256 and speed > -1):
            self.__currentSpeed = speed
        
        self.__smokeyGpio.set_speed(self.__currentSpeed)

    def go_straight_forwards(self):
        self.__smokeyGpio.set_speed_LfLrRfRr(self.__currentSpeed, self.__currentSpeed, self.__currentSpeed, self.__currentSpeed)

    def go_straight_backwards(self):
        self.__smokeyGpio.set_speed_LfLrRfRr(-self.__currentSpeed, -self.__currentSpeed, -self.__currentSpeed, -self.__currentSpeed)

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
