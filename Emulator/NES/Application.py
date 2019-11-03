from NES.R6502 import *
from NES.RAM import *
from NES.ROM import *
from NES.Bus import *
import numpy as np



class NES:

    def __init__(self):
        self.bus = Bus()
        self.cpu = R6502()
        self.ram = RAM(1024 * 2)

        self.cpu.connect_bus(self.bus)
        self.bus.connect_cpu(self.cpu)
        self.bus.connect_ram(self.ram)

# nestest
log_data_entries = []
def load_nestest_log(location):
    with open(location, "r") as file:
        line_entry = 0
        for line in file:
            parts = line.split(" ")
            PC = int(parts[0], 16)
            OC = int(parts[2], 16)
            for p in parts:
                if "A:" in p:
                    A = int(p.replace("A:", ""), 16)
                elif "X:" in p:
                    X = int(p.replace("X:", ""), 16)
                elif "Y:" in p:
                    Y = int(p.replace("Y:", ""), 16)
                elif "SP:" in p:
                    SP = int(p.replace("SP:", ""), 16)
                elif "P:" in p:
                    P = int(p.replace("P:", ""), 16)
                elif "CYC:" in p:
                    CYC = int(p.replace("CYC:", ""))

            log_data_entries.insert(line_entry, (PC, OC, A, X, Y, P, SP, CYC))
            line_entry += 1
def compare_to_log(instruction, cpu_state):
    log_data = log_data_entries[instruction]
    correct = \
        (log_data[0] == cpu_state[0]) and \
        (log_data[1] == cpu_state[1]) and \
        (log_data[2] == cpu_state[2]) and \
        (log_data[3] == cpu_state[3]) and \
        (log_data[4] == cpu_state[4]) and \
        (log_data[5] == cpu_state[5]) and \
        (log_data[6] == cpu_state[6]) and \
        (log_data[7] == cpu_state[7])
    return correct
def run_nestest(console):

    console.cpu.reg_PC = 0xC000
    console.cpu.total_cycles = 7
    console.cpu.flag_B = False
    console.cpu.debug = True

    rom = ROM("Resources/nestest.nes")
    console.bus.connect_rom(rom)

    load_nestest_log("Resources/nestest.log")

    instructions_completed = 1
    for _ in range(30000):

        console.cpu.clock()
        cpu_state = console.cpu.get_internal_state()

        if instructions_completed == len(log_data_entries):
            break

        if cpu_state != ():
            if not compare_to_log(instructions_completed, cpu_state):
                line = "[%04X]" % cpu_state[0]
                #line += " " + cpu_state[8]
                line += " %02X" % cpu_state[1]
                line += "  A:" + "%02X" % cpu_state[2]
                line += "  X:" + "%02X" % cpu_state[3]
                line += "  Y:" + "%02X" % cpu_state[4]
                line += "  P:" + "%02X" % cpu_state[5]
                line += "  SP:" + "%02X" % cpu_state[6]
                line += "  CYC:" + str(cpu_state[7])
                print("Error was caught on the last instruction. Expected:")
                print(line)
                break
            instructions_completed += 1

def run_instr_test_v5(console):

    console.cpu.reg_PC = 0xC000
    console.cpu.reg_S = 0xFD
    console.cpu.debug = True

    rom = ROM("Resources/official_only.nes")
    console.bus.connect_rom(rom)

    instructions_completed = 1
    #for _ in range(30000):
    #    console.cpu.clock()

    console.ram.print_contents(6000, 6032, 16)

def main():

    np.seterr(over="ignore")

    console = NES()
    run_nestest(console)

    print("Done!")


main()
