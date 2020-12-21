
class FrameData():

    def __init__(self):
        self.rows = []
        self.average_row = None
        self.is_fork = False
        self.is_join = False
        self.is_bottom_left_corner = False
        self.is_bottom_right_corner = False
        self.is_straight = True
        self.frame_speed = 0
        self.speedL = 0
        self.speedR = 0