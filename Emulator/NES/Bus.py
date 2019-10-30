

class Bus:

    def __init__(self):
        self.cpu = None
        self.ram = None

    # Reads data from the Bus
    def read(self, address):
        if 0x0000 <= address <= 0xFFFF:
            return self.ram.read(address)
        return 0

    # Writes data to the Bus
    def write(self, address, data):
        if 0x0000 <= address <= 0xFFFF:
            self.ram[address] = data

    def connect_cpu(self, cpu):
        self.cpu = cpu

    def connect_ram(self, ram):
        self.ram = ram
