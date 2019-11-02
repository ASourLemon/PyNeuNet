from NES.R6502 import *
from NES.RAM import *
from NES.ROM import *
from NES.Bus import *


import numpy as np


def main():

    np.seterr(over="ignore")

    # Constructs console architecture
    bus = Bus()
    cpu = R6502()
    ram = RAM(1024 * 2)
    rom = ROM("Resources/official_only.nes")

    cpu.connect_bus(bus)

    bus.connect_cpu(cpu)
    bus.connect_ram(ram)
    bus.connect_rom(rom)

    cpu.reg_PC = 0xC000
    cpu.reg_S = 0x00
    cpu.flag_I = True
    cpu.flag_U = True

    while True:
        if not cpu.clock(8813):
            break

        #ram.print_contents(0x050, 16)
        #cpu.print_contents()

    print("Done!")


main()
