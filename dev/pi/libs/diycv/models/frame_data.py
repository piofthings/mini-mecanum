
class FrameData():

    def __init__(self):
        self.rows = []
        self.average_row = None
        self.is_fork = False
        self.is_join = False
        self.veer_left = False
        self.veer_right = False
        self.is_straight = True
        self.frame_speed = 0
        self.speedL = 0
        self.speedR = 0
        self.ratio = 0.0
        self.index = 0
        self.width = 0
        self.height = 0
        self.first_white_pos = 0
        self.last_white_pos = 0
        self.thickness = 0