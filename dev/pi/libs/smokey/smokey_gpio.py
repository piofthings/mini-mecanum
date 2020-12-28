from gpiozero import Motor
from time import sleep
import serial


class SmokeyGpio():
    left_front_forward_id = 0
    left_front_reverse_id = 1
    left_rear_forward_id =  2
    left_rear_reverse_id =  3
    right_front_forward_id =4
    right_front_reverse_id =5
    right_rear_forward_id = 6
    right_rear_reverse_id = 7

    __left_front_forward_gpio = -1
    __left_front_reverse_gpio = -1
    __left_rear_forward_gpio = -1
    __left_rear_reverse_gpio = -1
    __right_front_forward_gpio = -1
    __right_front_reverse_gpio = -1
    __right_rear_forward_gpio = -1
    __right_rear_reverse_gpio = -1

    __motor_left_front = None
    __motor_left_rear = None
    __motor_right_front = None
    __motor_right_rear = None

    def __init__(self, pin_config)
        if len(pin_config) == 8:
            self.__left_front_forward_gpio = pin_config[self.left_front_forward_id]
            self.__left_front_reverse_gpio = pin_config[self.left_front_reverse_id]
            self.__left_rear_forward_gpio = pin_config[self.left_rear_forward_id]
            self.__left_rear_reverse_gpio = pin_config[self.left_rear_reverse_id]
            self.__right_front_forward_gpio = pin_config[self.right_front_forward_id]
            self.__right_front_reverse_gpio = pin_config[self.right_front_reverse_id]
            self.__right_rear_forward_gpio = pin_config[self.right_rear_forward_id]
            self.__right_rear_reverse_gpio = pin_config[self.right_rear_reverse_id]

            self.__motor_left_front = Motor(forward=self.__left_front_forward_gpio,
                                            backward=self.__left_front_reverse_gpio,
                                            pwm=True)

            self.__motor_left_rear = Motor(forward=self.__left_rear_forward_gpio,
                                            backward=self.__left_rear_reverse_gpio,
                                            pwm=True)

            self.__motor_right_front = Motor(forward=self.__right_front_forward_gpio,
                                            backward=self.__right_front_reverse_gpio,
                                            pwm=True)

            self.__motor_right_rear = Motor(forward=self.__right_rear_forward_gpio,
                                            backward=self.__right_rear_reverse_gpio,
                                            pwm=True)

        def set_speed(self, speed):
            current_speed = abs(speed/255)
            if speed > 0
                self.__motor_left_front.forward(current_speed)
                self.__motor_left_rear.forward(current_speed)
                self.__motor_right_front.forward(current_speed)
                self.__motor_right_rear.forward(current_speed)
            elif speed < 0:
                self.__motor_left_front.backward(current_speed)
                self.__motor_left_rear.backward(current_speed)
                self.__motor_right_front.backward(current_speed)
                self.__motor_right_rear.backward(current_speed)
            else:
                self.__motor_left_front.stop()
                self.__motor_left_rear.stop()
                self.__motor_right_front.stop()
                self.__motor_right_rear.stop()

       
        def set_direction(self, direction):
            pass

        def set_speed_LR(self, speedLeft, speedRight):
            current_speed_left = abs(speedLeft/255)
            current_speed_right = abs(speedRight/255)
            if speedLeft > 0
                self.__motor_left_front.forward(current_speed_left)
                self.__motor_left_rear.forward(current_speed_left)
            elif speedLeft < 0:
                self.__motor_left_front.backward(current_speed_left)
                self.__motor_left_rear.backward(current_speed_left)
            else:
                self.__motor_left_front.stop()
                self.__motor_left_rear.stop()
            if speedRight > 0
                self.__motor_right_front.forward(current_speed_right)
                self.__motor_right_rear.forward(current_speed_right)
            elif speedRight < 0:
                self.__motor_right_front.backward(current_speed_right)
                self.__motor_right_rear.backward(current_speed_right)
            else:
                self.__motor_right_front.stop()
                self.__motor_right_rear.stop()                


        def set_speed_LfLrRfRr(self, speedLeftFront, speedLeftRear, speedRightFront, speedRightRear):
            current_speed_left_front = abs(speedLeftFront/255)
            current_speed_left_rear = abs(speedLeftRear/255)
            current_speed_right_front = abs(speedRightFront/255)
            current_speed_right_rear = abs(speedRightRear/255)
            if speedLeftFront > 0
                self.__motor_left_front.forward(current_speed_left_front)
            elif speedLeft < 0:
                self.__motor_left_front.backward(current_speed_left_front)
            else:
                self.__motor_left_front.stop()
            if speedLeftRear > 0
                self.__motor_left_rear.forward(current_speed_left_rear)
            elif speedLeft < 0:
                self.__motor_left_rear.backward(current_speed_left_rear)
            else:
                self.__motor_left_rear.stop()
            if speedRightFront > 0
                self.__motor_right_front.forward(current_speed_right_front)
            elif speedRight < 0:
                self.__motor_right_front.backward(current_speed_right_front)
            else:
                self.__motor_right_front.stop()
            if speedRightRear > 0
                self.__motor_right_rear.forward(current_speed_right_rear)
            elif speedRight < 0:
                self.__motor_right_rear.backward(current_speed_right_rear)
            else:
                self.__motor_right_rear.stop()    

        def get_power_stats(self):
            data  = "5:0\n"
            print(data.encode('utf-8'))
            self.__ser.write(data.encode('utf-8'))
            line = self.__ser.readline().decode('utf-8').rstrip()
            print(line) 
            return line