import sys
import math
import numpy as np



class CPU:

    def __init__(self):
        self.registers = [0, 0, 0]
        self.skip_next = False

    def EXIT(self):
        print(
            str(self.registers[0]) + " " +
            str(self.registers[1]) + " " +
            str(self.registers[2])
        )

    def LD(self, register, value):
        self.registers[register] = value

    def ADD(self, register_x, register_y):
        r = self.registers[register_x] + self.registers[register_y]
        if r > 256:
            self.registers[2] = 1
        else:
            self.registers[2] = 0
        self.registers[register_x] = r & 0xFF

    def SUB(self, register_x, register_y):
        r = self.registers[register_x] - self.registers[register_y]
        if r < 0:
            self.registers[2] = 1
        else:
            self.registers[2] = 0
        self.registers[register_x] = r & 0xFF

    def OR(self, register_x, register_y):
        self.registers[register_x] = self.registers[register_x] | self.registers[register_y]

    def AND(self, register_x, register_y):
        self.registers[register_x] = self.registers[register_x] & self.registers[register_y]

    def XOR(self, register_x, register_y):
        self.registers[register_x] = self.registers[register_x] ^ self.registers[register_y]

    def SEV(self, register, value):
        self.skip_next = self.registers[register] == value

    def SNEV(self, register, value):
        self.skip_next = self.registers[register] != value

    def SER(self, register_x, register_y):
        self.skip_next = self.registers[register_x] == self.registers[register_y]

    def SNER(self, register_x, register_y):
        self.skip_next = self.registers[register_x] != self.registers[register_y]

    def exec_instruction(self, instruction):

        if self.skip_next:
            self.skip_next = False
        else:

            opcode = instruction[0]
            if opcode == "0":
                self.EXIT()
                return True

            elif opcode == "1":
                #LD k <- nn
                k = int(instruction[1])
                nn = int(instruction[2:], 16)
                self.LD(k, nn)

            elif opcode == "2":
                #ADD x <- x + y
                x = int(instruction[2])
                y = int(instruction[3])
                self.ADD(x, y)

            elif opcode == "3":
                #SUB x <- x - y
                x = int(instruction[2])
                y = int(instruction[3])
                self.SUB(x, y)

            elif opcode == "4":
                #OR x <- x | y
                x = int(instruction[2])
                y = int(instruction[3])
                self.OR(x, y)

            elif opcode == "5":
                #AND x <- x | y
                x = int(instruction[2])
                y = int(instruction[3])
                self.AND(x, y)

            elif opcode == "6":
                #XOR x <- x | y
                x = int(instruction[2])
                y = int(instruction[3])
                self.XOR(x, y)

            elif opcode == "7":
                #SE x <- reg(k) == nn
                k = int(instruction[1])
                nn = int(instruction[2:], 16)
                self.SEV(k, nn)

            elif opcode == "8":
                #SNE x <- reg(k) != nn
                k = int(instruction[1])
                nn = int(instruction[2:], 16)
                self.SNEV(k, nn)

            elif opcode == "9":
                #SE x <- reg(x) == reg(y)
                x = int(instruction[2])
                y = int(instruction[3])
                self.SER(x, y)

            elif opcode == "A":
                #SNE x <- reg(x) != reg(y)
                x = int(instruction[2])
                y = int(instruction[3])
                self.SNER(x, y)

        return False

def main():


    v = 0x3F00
    print(hex(v))
    v += 0x001F
    print(hex(v))
    v += 5
    print(hex(v & 0x3F1F))



    return

    program = input()

    cpu = CPU()

    for i in range(0, len(program), 4):
        instruction = program[i:i+4]
        if cpu.exec_instruction(instruction):
            return 0


main()

