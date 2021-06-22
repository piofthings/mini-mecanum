# Source: https://stackoverflow.com/a/58717387/710962
# Combined with 4Tronix code for keyboard input

import sys
import os
import tty
import termios

import threading

import queue

class KeyboardController():
    def __init__(self, exit_condition):
        self.exit_condition = exit_condition
        self.input_queue = queue.Queue()
        self.input_thread = threading.Thread(target=self.read_kbd_input, args=(), daemon=True)
        self.input_thread.start()

    def read_kbd_input(self):
        done_queueing_input = False
        while not done_queueing_input:
            console_input = self.readkey()
            self.input_queue.put(console_input)
            if console_input.strip() == self.exit_condition:
                done_queueing_input = True

    def input_queued(self):
        return_value = False
        if self.input_queue.qsize() > 0:
            return_value = True
        return return_value

    def input_get(self):
        return_value = ""
        if self.input_queue.qsize() > 0:
            return_value = self.input_queue.get()
        return return_value

    def clear(self):
        '''
        Clears the terminal screen and scroll back to present
        the user with a nice clean, new screen. Useful for managing
        menu screens in terminal applications.
        '''
        os.system('cls||echo -e \\\\033c')
    #======================================================================
    # Reading single character by forcing stdin to raw mode

    def readchar(self):
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        if ch == '0x03':
            raise KeyboardInterrupt
        return ch

    def readkey(self, getchar_fn=None):
        getchar = getchar_fn or self.readchar
        c1 = getchar()
        if ord(c1) != 0x1b:
            return c1
        c2 = getchar()
        if ord(c2) != 0x5b:
            return c1
        c3 = getchar()
        # 16=Up, 17=Down, 18=Right, 19=Left arrows
        return chr(0x10 + ord(c3) - 65)

    # End of single character reading
    #======================================================================

if __name__ == '__main__':

    NON_BLOCK_INPUT = KeyboardController(exit_condition='quit')

    DONE_PROCESSING = False
    INPUT_STR = ""
    while not DONE_PROCESSING:
        if NON_BLOCK_INPUT.input_queued():
            INPUT_STR = NON_BLOCK_INPUT.input_get()
            if INPUT_STR.strip() == "quit":
                DONE_PROCESSING = True
            else:
                print("{}".format(INPUT_STR))