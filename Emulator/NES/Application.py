from NES.R6502 import *
from NES.RAM import *
from NES.Bus import *

import numpy as np


def main():

    np.seterr(over="ignore")

    # Constructs console architecture
    bus = Bus()
    cpu = R6502()
    ram = RAM(1024 * 4)

    cpu.connect_bus(bus)

    bus.connect_cpu(cpu)
    bus.connect_ram(ram)

    ram.memory[0] = 0x08
    ram.memory[1] = 0x28

    cpu.clock()

    ram.print_contents(0x0110, 16)
    cpu.print_contents()

    print("Done!")


main()
