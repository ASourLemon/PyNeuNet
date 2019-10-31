import numpy as np


class ROM:

    def __init__(self, location):
        self.data = []

        self.size = 0

    # Reads data from RAM
    def read(self, address):
        if 0x0000 <= address < self.size:
            return self.memory[address]
        return 0