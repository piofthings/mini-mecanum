
import sys
import os

sys.path.append(os.path.abspath(os.path.join(
    os.path.dirname(__file__), "../")))

from keyboardcontroller.keyboard_controller import KeyboardController
from smokey.smokey_gpio import SmokeyGpio


class SmokeyController():
    __keyboardController =  None
    __smokeyGpio = None
    __currentSpeed = 125

    def __init__(self, smokeyGpio, exit_condition):
        self.__keyboardController = KeyboardController(exit_condition)
        self.__smokeyGpio = smokeyGpio

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
                    self.go_straight_forwards() # go straight forward
                elif input_str.strip() == "s":
                    self.go_straight_backwards() # go straight back
                elif input_str.strip() == "a":        # strafe left
                    self.strafe_left()
                elif input_str.strip() == "d":        # strafe right
                    self.strafe_right()
                elif input_str.strip() == 'q':  # diagonal left forward
                    self.diagonal_left_forward()
                elif input_str.strip() == 'e':  # diagonal right forward
                    self.diagonal_right_forward()
                elif input_str.strip() == 'z':  # diagonal right reverse
                    self.diagonal_right_reverse()
                elif input_str.strip() == 'c':  # diagonal left reverse
                    self.diagonal_left_reverse()
                elif input_str.strip() == 'r':  # spin clockwise
                    self.spin_clockwise()
                elif input_str.strip() == 'f':  # spin anti-clockwise
                    self.spin_anticlockwise()
                elif input_str == "p": #STOP and quit
                    self.increase_speed(0)
                    done_processing = True
                    self.__keyboardController.clear()

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