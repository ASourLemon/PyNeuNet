import numpy as np


class Mapper_000:

    def __init__(self, n_prg_banks):
        self.n_prg_banks = n_prg_banks

    def prg_read(self, address):
        if 0x8000 <= address <= 0xFFFF:
            mask = 0x7FFF
            if self.n_prg_banks == 1:
                mask = 0x3FFF
            return True, address & mask
        return False, 0

    def chr_read(self, address):
        if 0x0000 <= address <= 0x1FFF:
            return True, address
        return False, 0


class Header:

    def __init__(self, file_pointer):
        self.name = file_pointer.read(4)
        self.n_prg_banks = ord(file_pointer.read(1))
        self.n_chr_banks = ord(file_pointer.read(1))
        self.mapper1 = ord(file_pointer.read(1))
        self.mapper2 = ord(file_pointer.read(1))
        self.prg_ram_size = ord(file_pointer.read(1))
        self.tv_system1 = ord(file_pointer.read(1))
        self.tv_system2 = ord(file_pointer.read(1))
        self.unused = file_pointer.read(5)


class Cartridge:

    def __init__(self, location):

        with open(location, "rb") as f:
            self.header = Header(f)
            self.prg_data = []
            self.chr_data = []

            if self.header.mapper1 & 0x04:
                f.read(512)

            self.mapper = Mapper_000(self.header.n_prg_banks)

            for i in range(self.header.n_prg_banks * 16384):
                self.prg_data.insert(i, ord(f.read(1)))

            for i in range(self.header.n_chr_banks * 8192):
                self.chr_data.insert(i, ord(f.read(1)))

    # Reads data from RAM
    def cpu_read(self, address):
        success, mapped_address = self.mapper.prg_read(address)
        if success:
            return self.prg_data[mapped_address]

    def ppu_read(self, address):
        success, mapped_address = self.mapper.chr_read(address)
        if success:
            return self.chr_data[mapped_address]
