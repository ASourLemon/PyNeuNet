import numpy as np
import random
import time

palColors = [
    [(84, 84, 84), (0, 30, 116), (8, 16, 144), (48, 0, 136), (68, 0, 100), (92, 0, 48), (84, 4, 0), (60, 24, 0), (32, 42, 0), (8, 58, 0), (0, 64, 0), (0, 60, 0), (0, 50, 60), (0, 0, 0)],
    [(152, 150, 152), (8, 76, 196), (48, 50, 236), (92, 30, 228), (136, 20, 176), (160, 20, 100), (152, 34, 32), (120, 60, 0), (84, 90, 0), (40, 114, 0), (8, 124, 0), (0, 118, 40), (0, 102, 120), (0, 0, 0)],
    [(236, 238, 236), (76, 154, 236), (120, 124, 236), (176, 98, 236), (228, 84, 236), (236, 88, 180), (236, 106, 100), (212, 136, 32), (160, 170, 0), (116, 196, 0), (76, 208, 32), (56, 204, 108), (56, 180, 204), (60, 60, 60)],
    [(236, 238, 236), (168, 204, 236), (188, 188, 236), (212, 178, 236), (236, 174, 236), (236, 174, 212), (236, 180, 176), (228, 196, 144), (204, 210, 120), (180, 222, 120), (168, 226, 144), (152, 226, 180), (160, 214, 228), (160, 162, 160)]
]

PPUCTRL_NN = 0x0003
PPUCTRL_I = 0x0004
PPUCTRL_S = 0x0008
PPUCTRL_B = 0x0010
PPUCTRL_H = 0x0020
PPUCTRL_P = 0x0040
PPUCTRL_V = 0x0080

PPUSTATUS_O = 0x0020
PPUSTATUS_S = 0x0040
PPUSTATUS_V = 0x0080


class V2C02:

    def __init__(self, game_engine):

        # Control
        self.bus = None

        self.reg_PPUCTRL = np.uint8(0)
        self.reg_PPUMASK = np.uint8(0)
        self.reg_PPUSTATUS = np.uint8(0)
        self.reg_OAMADDR = np.uint8(0)
        self.reg_OAMDATA = np.uint8(0)
        self.reg_PPUSCROLL = np.uint8(0)
        self.reg_PPUADDR = np.uint8(0)
        self.reg_PPUDATA = np.uint8(0)
        self.reg_OAMDMA = np.uint8(0)

        self.ppu_address_latch = False
        self.ppu_data_delay = 0
        self.total_cycles = 0
        self.nmi = False



        # Render
        self.scan_height_limit = 261
        self.scan_width_limit = 341

        self.screen_height_limit = 240
        self.screen_width_limit = 256

        self.render_x = 0
        self.render_y = 0

        self.total_frames = 0
        self.frame_completed = False

        self.game = game_engine
        self.game.init()

        #self.screen = self.game.display.set_mode((self.scan_width_limit, self.scan_height_limit))
        #self.screen.fill((0, 0, 0))

        self.start_time = time.time()

        self.debug = False

    def connect_bus(self, bus):
        self.bus = bus

    def clock(self):

        self.reg_PPUSTATUS |= int(self.screen_height_limit <= self.render_y <= self.scan_height_limit) * PPUSTATUS_V

        if (self.reg_PPUCTRL & PPUCTRL_V) != 0 and self.render_y == self.screen_height_limit and self.render_x == 0:
            self.nmi = True

        #if self.render_x < self.screen_width_limit and 0 < self.render_y < self.screen_height_limit:
        #   r = random.randint(0, 1)
        #   self.screen.set_at((self.render_x, self.render_y), (r * 255, r * 255, r * 255))

        self.render_x += 1
        if self.render_x == self.scan_width_limit:
            self.render_x = 0
            self.render_y += 1
            if self.render_y == self.scan_height_limit:

                #self.game.display.update()
                self.frame_completed = True
                self.total_frames += 1

                self.render_y = 0

                self.game.display.set_caption("FPS: " + str(self.total_frames / (time.time() - self.start_time)))

        self.total_cycles += 1

        if self.debug:
            print("PPU: " + str(self.total_cycles) + " cycles.")

    def cpu_write(self, address, data):

        if address == 0x0000:
            self.reg_PPUCTRL = data

        elif address == 0x0001:
            self.reg_PPUMASK = data

        elif address == 0x0003:
            self.reg_OAMADDR = data
        elif address == 0x0004:
            self.reg_OAMDATA = data
        elif address == 0x0005:
            self.reg_PPUSCROLL = data

        elif address == 0x0006:
            if not self.ppu_address_latch:
                self.reg_PPUADDR = ((data << 8) & 0xFF00) | (self.reg_PPUADDR & 0x00FF)
                self.ppu_address_latch = True
            else:
                self.reg_PPUADDR = (self.reg_PPUADDR & 0xFF00) | data
                self.ppu_address_latch = False

        elif address == 0x0007:
            self.write(self.reg_PPUADDR, data)

            self.reg_PPUADDR += 1

    def cpu_read(self, address, read):
        if address == 0x0000:
            return self.reg_PPUCTRL
        elif address == 0x0001:
            return 0
        elif address == 0x0002:
            self.reg_PPUSTATUS |= PPUSTATUS_V
            data = self.reg_PPUSTATUS & 0xE0
            self.reg_PPUSTATUS &= ~PPUSTATUS_V
            self.ppu_address_latch = False
            return data
        elif address == 0x0003:
            return 0
        elif address == 0x0004:
            return 0
        elif address == 0x0005:
            return 0
        elif address == 0x0006:
            return 0
        elif address == 0x0007:

            data = self.ppu_data_delay
            self.ppu_data_delay = np.uint8(self.read(self.reg_PPUADDR))

            if self.reg_PPUADDR >= 0x3F00:
                data = self.ppu_data_delay

            #self.reg_PPUADDR += 1
            return data

    def write(self, address, data):
        self.bus.ppu_write(address, data)

    def read(self, address):
        return self.bus.ppu_read(address)
