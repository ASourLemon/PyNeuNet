import numpy as np


class R6502_Instruction:

    def __init__(self, op_code):

        op_code_str = hex(op_code)[2:]

        op_code_low = int(op_code_str[1], 16)
        op_code_high = int(op_code_str[0], 16)

        instruction = instruction_set_matrix[op_code_high][op_code_low]

        self.mnemonic = instruction[0]
        self.addressing_function = instruction[1]
        self.execution_function = instruction[2]

class R6502:

    # Extra required for Emulation
    def __init__(self):

        self.reg_A = np.uint8(0)              # Accumulator
        self.reg_Y = np.uint8(0)              # Y Register
        self.reg_X = np.uint8(0)              # X Register
        self.reg_PC = np.uint16(0)            # Program Counter
        self.reg_S = np.uint8(0)              # Stack Pointer

        self.flag_N = False         # Negative
        self.flag_V = False         # Overflow
        self.flag_U = False         # Unused
        self.flag_B = False         # Break
        self.flag_D = False         # Decimal / Unused
        self.flag_I = False         # Disable Interrupts
        self.flag_Z = False         # Zero
        self.flag_C = False         # Carry

        self.memory_location = np.uint16(0x0000)        # Stores the address to read operand
        self.memory_data = np.uint8(0)                  # Stores the operand to use

        self.bus = None

    # public
    def connect_bus(self, bus):
        self.bus = bus

    def load_instruction(self, instruction):
        instruction.addressing_function(self)
        self.load_memory_location()

    def execute_instruction(self, instruction):
        instruction.execution_function(self)

    def clock(self):

        op_code = self.read(self.reg_PC)
        instruction = R6502_Instruction(op_code)

        self.reg_PC += 1

        self.load_instruction(instruction)
        self.execute_instruction(instruction)

    def print_contents(self):
        print("A: " + " [%02X]" % self.reg_A + " " + str(self.reg_A))
        print("X: " + " [%02X]" % self.reg_X + " " + str(self.reg_X))
        print("PC: " + "[%02X]" % self.reg_PC + " " + str(self.reg_PC))
        print("S: " + " [%02X]" % self.reg_S + " " + str(self.reg_S))
        print()
        print("N: " + str(self.flag_N))
        print("V: " + str(self.flag_V))
        print("U: " + str(self.flag_U))
        print("B: " + str(self.flag_B))
        print("D: " + str(self.flag_D))
        print("I: " + str(self.flag_I))
        print("Z: " + str(self.flag_Z))
        print("C: " + str(self.flag_C))

    #
    # private
    def read(self, address):
        return self.bus.read(address)

    def write(self, address, data):
        self.bus.write(address, data)

    def load_memory_location(self):
        self.memory_data = self.read(self.memory_location)

    # Flags
    def update_flag_N(self, data):
        self.flag_N = (data & 0x80) != 0x00

    def update_flag_Z(self, data):
        self.flag_Z = data == 0x00


    #
    # Addressing Modes

    # Implied Addressing [Implied]
    def iad(self):
        self.memory_data = self.reg_A
        return 0

    # Immediate Address [IMM]
    def imm(self):
        self.memory_location = self.reg_PC
        self.reg_PC += 1
        return 0

    # Accumulator Addressing [Accum]
    def acc(self):
        self.memory_location = self.reg_A
        return 0

    # Absolute Addressing [Absolute]
    def abs(self):
        low_bits = self.read(self.reg_PC)
        self.reg_PC += 1
        high_bits = self.read(self.reg_PC)
        self.reg_PC += 1
        self.memory_location = (high_bits << 8) | low_bits
        return 0

    # X Index Absolute Addressing [ABS, X]
    def abx(self):
        low_bits = self.read(self.reg_PC)
        self.reg_PC += 1
        high_bits = self.read(self.reg_PC)
        self.reg_PC += 1
        self.memory_location = (high_bits << 8) | low_bits
        self.memory_location += self.reg_X

        if (self.memory_location & 0xFF00) != (high_bits << 8):
            return 1
        else:
            return 0

    # X Index Absolute Addressing [ABS, Y]
    def aby(self):
        low_bits = self.read(self.reg_PC)
        self.reg_PC += 1
        high_bits = self.read(self.reg_PC)
        self.reg_PC += 1
        self.memory_location = (high_bits << 8) | low_bits
        self.memory_location += self.reg_Y

        if (self.memory_location & 0xFF00) != (high_bits << 8):
            return 1
        else:
            return 0
        return

    # Zero Page Addressing [ZP]
    def zpa(self):
        self.memory_location = self.read(self.reg_PC) & 0x00FF
        self.reg_PC += 1
        return 0

    # X Indexed Zero Page Addressing [ZP, X]
    def zpx(self):
        self.memory_location = (self.read(self.reg_PC) + self.reg_X) & 0x00FF
        self.reg_PC += 1
        return 0

    # Y Indexed Zero Page Addressing [ZP, Y]
    def zpy(self):
        self.memory_location = (self.read(self.reg_PC) + self.reg_Y) & 0x00FF
        self.reg_PC += 1
        return 0

    # Relative Addressing [Relative]
    def rad(self):

        self.memory_location = self.read(self.reg_PC)
        self.reg_PC += 1

        if self.memory_location & 0x80:
            self.memory_location |= 0xFF00

        return 0

    # Indexed Indirect Addressing [(IND, X)]
    def iix(self):

        zp = self.read(self.reg_PC)
        self.reg_PC += 1

        low_bits = self.read(zp + self.reg_X) & 0x00FF
        high_bits = self.read(zp + self.reg_X + 1) & 0x00FF

        self.memory_location = (high_bits << 8) | low_bits
        return 0

    # Indirect Indexed Addressing [(IND), Y]
    def iiy(self):

        zp = self.read(self.reg_PC)
        self.reg_PC += 1

        low_bits = self.read(zp & 0x00FF)
        high_bits = self.read(zp & 0x00FF)

        self.memory_location = (high_bits << 8) | low_bits
        self.memory_location += self.reg_Y

        if (self.memory_location & 0xFF00) != (high_bits << 8):
            return 1
        else:
            return 0

    # Absolute Indirect [Indirect]
    def ain(self):
        ptr_low = self.read(self.reg_PC)
        self.reg_PC += 1
        ptr_high = self.read(self.reg_PC)
        self.reg_PC += 1
        actual_ptr = (ptr_high << 8) | ptr_low

        data_low = self.read(actual_ptr)
        data_high = self.read(actual_ptr + 1)

        self.memory_location = (data_high << 8) | data_low

        return 0

    # Opcodes

    # A
    # Add Memory to Accumulator with Carry
    # OP:
    # Flag:
    def ADC(self):
        return 0

    # AND Memory with Accumulator
    # OP:   A = A & M;
    # Flag: N, Z
    def AND(self):
        return 0

    # Shift Left One Bit (Memory or Accumulator)
    # OP:    A = C <- (A << 1) <- 0
    # Flag: N, Z, C
    def ASL(self):
        return 0

    # B
    # Branch on Carry Clear
    # OP: if(!C) then pc = new_address
    def BCC(self):
        return 0

    # Branch on Carry Set
    # OP: if(C) then pc = new_address
    def BCS(self):
        return 0

    # Branch on Result Zero
    # OP: if(Z) then pc = new_address
    def BEQ(self):
        return 0

    def BIT(self):
        return 0

    def BMI(self):
        return 0

    def BNE(self):
        return 0

    def BPL(self):
        return 0

    def BRK(self):
        return 0

    def BVC(self):
        return 0

    def BVS(self):
        return 0




    def LDX(self):
        self.reg_X = self.memory_data
        self.update_flag_Z(self.reg_X)
        self.update_flag_N(self.reg_X)
        return 1

    def LDY(self):
        self.reg_Y = self.memory_data
        self.update_flag_Z(self.reg_Y)
        self.update_flag_N(self.reg_Y)
        return 1

    # Instruction Set
ii = ("XXX", R6502.iad, 9, 9)

instruction_set_matrix = [
    [("BRK", R6502.iad, 1, 7), ("ORA", R6502.iix, 2, 6), ii, ii, ii, ("ORA", R6502.zpa, 2, 3), ("ASL", R6502.zpa, 2, 5), ii, ("PHP", R6502.iad, 1, 3), ("ORA", R6502.imm, 2, 2), ("ASL", R6502.acc, 1, 2), ii, ii, ("ORA", R6502.abs, 3, 4), ("ASL", R6502.abs, 3, 6), ii],
    [("BPL", R6502.rad, 2, 2), ("ORA", R6502.iiy, 2, 5), ii, ii, ii, ("ORA", R6502.zpx, 2, 4), ("ASL", R6502.zpx, 2, 6), ii, ("CLC", R6502.iad, 1, 2), ("ORA", R6502.aby, 3, 4), ii, ii, ii, ("ORA", R6502.abx, 3, 4), ("ASL", R6502.abx, 3, 7), ii],
    [("JSR", R6502.abs, 3, 6), ("ORA", R6502.iiy, 2, 5), ii, ii, ii, ("ORA", R6502.zpx, 2, 4), ("ASL", R6502.zpx, 2, 6), ii, ("CLC", R6502.iad, 1, 2), ("ORA", R6502.aby, 3, 4), ii, ii, ii, ("ORA", R6502.abx, 3, 4), ("ASL", R6502.abx, 3, 7), ii],
    [("BMI", R6502.abs, 2, 2), ("ORA", R6502.iiy, 2, 5), ii, ii, ii, ("ORA", R6502.zpx, 2, 4), ("ASL", R6502.zpx, 2, 6), ii, ("CLC", R6502.iad, 1, 2), ("ORA", R6502.aby, 3, 4), ii, ii, ii, ("ORA", R6502.abx, 3, 4), ("ASL", R6502.abx, 3, 7), ii],
    [("RTI", R6502.rad, 1, 6), ("ORA", R6502.iiy, 2, 5), ii, ii, ii, ("ORA", R6502.zpx, 2, 4), ("ASL", R6502.zpx, 2, 6), ii, ("CLC", R6502.iad, 1, 2), ("ORA", R6502.aby, 3, 4), ii, ii, ii, ("ORA", R6502.abx, 3, 4), ("ASL", R6502.abx, 3, 7), ii],
    [("BVC", R6502.rad, 2, 2), ("ORA", R6502.iiy, 2, 5), ii, ii, ii, ("ORA", R6502.zpx, 2, 4), ("ASL", R6502.zpx, 2, 6), ii, ("CLC", R6502.iad, 1, 2), ("ORA", R6502.aby, 3, 4), ii, ii, ii, ("ORA", R6502.abx, 3, 4), ("ASL", R6502.abx, 3, 7), ii],
    [("RTS", R6502.rad, 1, 6), ("ORA", R6502.iiy, 2, 5), ii, ii, ii, ("ORA", R6502.zpx, 2, 4), ("ASL", R6502.zpx, 2, 6), ii, ("CLC", R6502.iad, 1, 2), ("ORA", R6502.aby, 3, 4), ii, ii, ii, ("ORA", R6502.abx, 3, 4), ("ASL", R6502.abx, 3, 7), ii],
    [("BVS", R6502.rad, 2, 2), ("ORA", R6502.iiy, 2, 5), ii, ii, ii, ("ORA", R6502.zpx, 2, 4), ("ASL", R6502.zpx, 2, 6), ii, ("CLC", R6502.iad, 1, 2), ("ORA", R6502.aby, 3, 4), ii, ii, ii, ("ORA", R6502.abx, 3, 4), ("ASL", R6502.abx, 3, 7), ii],
    [ii, ("ORA", R6502.iiy, 2, 5), ii, ii, ii, ("ORA", R6502.zpx, 2, 4), ("ASL", R6502.zpx, 2, 6), ii, ("CLC", R6502.iad, 1, 2), ("ORA", R6502.aby, 3, 4), ii, ii, ii, ("ORA", R6502.abx, 3, 4), ("ASL", R6502.abx, 3, 7), ii],
    [("BCC", R6502.rad, 2, 2), ("ORA", R6502.iiy, 2, 5), ii, ii, ii, ("ORA", R6502.zpx, 2, 4), ("ASL", R6502.zpx, 2, 6), ii, ("CLC", R6502.iad, 1, 2), ("ORA", R6502.aby, 3, 4), ii, ii, ii, ("ORA", R6502.abx, 3, 4), ("ASL", R6502.abx, 3, 7), ii],
    [("LDY", R6502.rad, 2, 2), ("LDA", R6502.iix, 2, 6), ("LDX", R6502.imm, R6502.LDX, 2, 2), ii, ii, ("ORA", R6502.zpx, 2, 4), ("ASL", R6502.zpx, 2, 6), ii, ("CLC", R6502.iad, 1, 2), ("ORA", R6502.aby, 3, 4), ii, ii, ii, ("ORA", R6502.abx, 3, 4), ("ASL", R6502.abx, 3, 7), ii],
    [("BCS", R6502.rad, 2, 2), ("ORA", R6502.iiy, 2, 5), ii, ii, ii, ("ORA", R6502.zpx, 2, 4), ("ASL", R6502.zpx, 2, 6), ii, ("CLC", R6502.iad, 1, 2), ("ORA", R6502.aby, 3, 4), ii, ii, ii, ("ORA", R6502.abx, 3, 4), ("ASL", R6502.abx, 3, 7), ii],
    [("CPY", R6502.imm, 2, 2), ("ORA", R6502.iiy, 2, 5), ii, ii, ii, ("ORA", R6502.zpx, 2, 4), ("ASL", R6502.zpx, 2, 6), ii, ("CLC", R6502.iad, 1, 2), ("ORA", R6502.aby, 3, 4), ii, ii, ii, ("ORA", R6502.abx, 3, 4), ("ASL", R6502.abx, 3, 7), ii],
    [("BNE", R6502.rad, 2, 2), ("ORA", R6502.iiy, 2, 5), ii, ii, ii, ("ORA", R6502.zpx, 2, 4), ("ASL", R6502.zpx, 2, 6), ii, ("CLC", R6502.iad, 1, 2), ("ORA", R6502.aby, 3, 4), ii, ii, ii, ("ORA", R6502.abx, 3, 4), ("ASL", R6502.abx, 3, 7), ii],
    [("CPX", R6502.imm, 2, 2), ("ORA", R6502.iiy, 2, 5), ii, ii, ii, ("ORA", R6502.zpx, 2, 4), ("ASL", R6502.zpx, 2, 6), ii, ("CLC", R6502.iad, 1, 2), ("ORA", R6502.aby, 3, 4), ii, ii, ii, ("ORA", R6502.abx, 3, 4), ("ASL", R6502.abx, 3, 7), ii],
    [("BEO", R6502.rad, 2, 2), ("ORA", R6502.iiy, 2, 5), ii, ii, ii, ("ORA", R6502.zpx, 2, 4), ("ASL", R6502.zpx, 2, 6), ii, ("CLC", R6502.iad, 1, 2), ("ORA", R6502.aby, 3, 4), ii, ii, ii, ("ORA", R6502.abx, 3, 4), ("ASL", R6502.abx, 3, 7), ii]
]

