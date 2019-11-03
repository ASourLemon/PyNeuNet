import numpy as np


class RAM:

    def __init__(self, size):
        self.memory = []
        self.size = size
        for i in range(size):
            self.memory.insert(i, np.uint8(0))

    # Reads data from RAM
    def read(self, address):
        if 0x0000 <= address < self.size:
            return self.memory[address]
        return 0

    # Writes data to RAM
    def write(self, address, data):
        if 0x0000 <= address < self.size:
            self.memory[address] = data

    def print_contents(self, lower_bound, upper_bound, step):
        for p in range(lower_bound, upper_bound, step):
            s = "$%04X:" % p + " "
            for i in range(step + 1):
                s += "%02X" % self.memory[p + i] + " "
            print(s)







