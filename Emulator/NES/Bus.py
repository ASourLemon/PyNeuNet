

class Bus:

    def __init__(self):
        self.cpu = None
        self.ram = None
        self.rom = None
        self.ppu = None
        self.vram = None

    # CPU Reads data from the Bus
    def cpu_bus_read(self, address):
        if 0x0000 <= address <= 0x1FFF:
            return self.ram.read(address & 0x1FFF)

        elif 0x2000 <= address <= 0x2007:
            return self.ppu.cpu_read(address & 0x0007)

        elif 0x4020 <= address <= 0xFFFF:
            return self.rom.cpu_read(address)
        return 0

    # CPU Writes data to the Bus
    def cpu_bus_write(self, address, data):
        if 0x0000 <= address <= 0x1FFF:
            self.ram.write(address & 0x1FFF, data)

    # PPU Reads data from the Bus
    def ppu_bus_read(self, address):
        if 0x0000 <= address <= 0x1FFF:
            return self.rom.ppu_read(address)
        elif 0x2000 <= address <= 0x2FFF:
            return self.vram.read(address)
        elif 0x3F00 <= address <= 0x3FFF:
            # Palettes
            return 0
        return 0




    def connect_cpu(self, cpu):
        self.cpu = cpu
    def connect_ram(self, ram):
        self.ram = ram
    def connect_rom(self, rom):
        self.rom = rom
    def connect_ppu(self, ppu):
        self.ppu = ppu
    def connect_vram(self, vram):
        self.vram = vram
