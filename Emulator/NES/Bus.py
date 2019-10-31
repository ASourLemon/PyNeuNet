

class Bus:

    def __init__(self):
        self.cpu = None
        self.ram = None
        self.rom = None

    # Reads data from the Bus
    def read(self, address):
        if 0x0000 <= address <= 0x1FFF:
            return self.ram.read(address & 0x1FFF)
        elif 0x4020 <= address <= 0xFFFF:
            return self.rom.read(address)
        return 0

    # Writes data to the Bus
    def write(self, address, data):
        if 0x0000 <= address <= 0x1FFF:
            self.ram.write(address & 0x1FFF, data)

    def connect_cpu(self, cpu):
        self.cpu = cpu

    def connect_ram(self, ram):
        self.ram = ram

    def connect_rom(self, rom):
        self.rom = rom
