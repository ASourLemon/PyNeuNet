import pygame

class V2C02:

    def __init__(self):
        self.height_limit = 262
        self.width_limit = 342

        self.render_x = 0
        self.render_y = 0

        self.total_cycles = 0
        self.total_frames = 0
        self.frame_completed = False

    def clock(self):

        self.render_x += 1
        if self.render_x == self.width_limit:

            self.render_x = 0
            self.render_y += 1
            if self.render_y == self.height_limit:
                self.render_x = -1
                self.frame_completed = True

        self.total_cycles += 1



