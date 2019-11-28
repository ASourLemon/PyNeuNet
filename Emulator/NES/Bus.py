

class Bus:

    def __init__(self):

        self.rom = None

        self.cpu = None
        self.ram = None

        self.ppu = None
        self.vram = None

    # CPU Reads data from the Bus
    def cpu_read(self, address, read):

        if 0x0000 <= address <= 0x1FFF:
            return self.ram.read(address & 0x1FFF)

        elif 0x2000 <= address <= 0x3FFF:
            return self.ppu.cpu_read(address & 0x0007, read)

        elif 0x4020 <= address <= 0xFFFF:
            return self.rom.cpu_read(address)

        return 0

    # CPU Writes data to the Bus
    def cpu_write(self, address, data):

        if 0x0000 <= address <= 0x1FFF:
            self.ram.write(address & 0x1FFF, data)
        elif 0x2000 <= address <= 0x3FFF:
            self.ppu.cpu_write(address & 0x0007, data)
        elif 0x4020 <= address <= 0xFFFF:
            self.rom.cpu_write(address, data)

    # PPU Reads data from the Bus
    def ppu_read(self, address):

        if 0x0000 <= address <= 0x1FFF:
            # Pattern Memory



            return self.rom.ppu_read(address)

        elif 0x2000 <= address <= 0x3EFF:
            # Name Table Memory
            if (self.rom.header.mapper1 & 0x01) == 0:  # Horizontal Mirror
                if 0x2000 <= address <= 0x27FF:  # NT 0
                    return self.vram.read(address & 0x03FF)
                elif 0x2800 <= address <= 0x2FFF:  # NT 1
                    return self.vram.read((address & 0x03FF) + 0x0400)

        elif 0x3F00 <= address <= 0x3F1F:  # Palette Memory

            if address in (0x3F04, 0x3F08, 0x3F0C):
                address == 0x3F00

            if address == 0x3F10:
                address = 0x3F00
            elif address == 0x3F14:
                address = 0x3F04
            elif address == 0x3F18:
                address = 0x3F08
            elif address == 0x3F1C:
                address = 0x3F0C

            return self.vram.read(address)

        return 0

    # PPU Writes data to the Bus
    def ppu_write(self, address, data):

        if 0x0000 <= address <= 0x1FFF:
            # Pattern Memory
            self.rom.ppu_write(address, data)

        elif 0x2000 <= address <= 0x3EFF:  # Name Table Memory

            if (self.rom.header.mapper1 & 0x01) == 0:  # Horizontal Mirror

                if 0x2000 <= address <= 0x27FF:  # NT 0
                    self.vram.write(address & 0x03FF, data)
                elif 0x2800 <= address <= 0x2FFF:  # NT 1
                    self.vram.write((address & 0x03FF) + 0x0400, data)

        elif 0x3F00 <= address <= 0x3F1F:  # Palette Memory

            if address in (0x3F04, 0x3F08, 0x3F0C):
                address == 0x3F00

            if address == 0x3F10:
                address = 0x3F00
            elif address == 0x3F14:
                address = 0x3F04
            elif address == 0x3F18:
                address = 0x3F08
            elif address == 0x3F1C:
                address = 0x3F0C

            self.vram.write(address, data)




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


    def print_vram_contents(self, lower_bound, upper_bound, step):
        for p in range(lower_bound, upper_bound, step):
            s = "$%04X:" % p + " "
            for i in range(step):
                s += "%02X" % self.ppu_read(p + i) + " "
            print(s)
