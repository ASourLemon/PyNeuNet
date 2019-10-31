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
    def BEO(self):
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

    # C
    def CLC(self):
        return 0
    def CLD(self):
        return 0
    def CLI(self):
        return 0
    def CLV(self):
        return 0
    def CMP(self):
        return 0
    def CPX(self):
        return 0
    def CPY(self):
        return 0

    # D
    def DEC(self):
        return 0
    def DEX(self):
        return 0
    def DEY(self):
        return 0

    # E
    def EOR(self):
        return 0

    # I
    def INC(self):
        return 0
    def INX(self):
        return 0
    def INY(self):
        return 0

    # J
    def JMP(self):
        return 0
    def JSR(self):
        return 0

    # L
    def LDA(self):
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
    def LSR(self):
        return 0

    # N
    def NOP(self):
        return 0

    # O
    def ORA(self):
        return 0

    # P
    def PHA(self):
        return 0
    def PHP(self):
        return 0
    def PLA(self):
        return 0
    def PLP(self):
        return 0

    # R
    def ROL(self):
        return 0
    def ROR(self):
        return 0
    def RTI(self):
        return 0
    def RTS(self):
        return 0

    # S
    def SBC(self):
        return 0
    def SEC(self):
        return 0
    def SED(self):
        return 0
    def SEI(self):
        return 0
    def STA(self):
        return 0
    def STX(self):
        return 0
    def STY(self):
        return 0

    # T
    def TAX(self):
        return 0
    def TAY(self):
        return 0
    def TSX(self):
        return 0
    def TXA(self):
        return 0
    def TXS(self):
        return 0
    def TYA(self):
        return 0

# X
    def XXX(self):
        return 0

    # Instruction Set
ii = ("XXX", R6502.iad, R6502.XXX, 9, 9)

instruction_set_matrix = [
    [("BRK", R6502.iad, R6502.BRK, 1, 7), ("ORA", R6502.iix, R6502.ORA, 2, 6), ii, ii, ii, ("ORA", R6502.zpa, R6502.ORA, 2, 3), ("ASL", R6502.zpa, R6502.ASL, 2, 5), ii, ("PHP", R6502.iad, R6502.PHP, 1, 3), ("ORA", R6502.imm, R6502.ORA, 2, 2), ("ASL", R6502.acc, R6502.ASL, 1, 2), ii, ii, ("ORA", R6502.abs, R6502.ORA, 3, 4), ("ASL", R6502.abs, R6502.ASL, 3, 6), ii],
    [("BPL", R6502.rad, R6502.BPL, 2, 2), ("ORA", R6502.iiy, R6502.ORA, 2, 5), ii, ii, ii, ("ORA", R6502.zpx, R6502.ORA, 2, 4), ("ASL", R6502.zpx, R6502.ASL, 2, 6), ii, ("CLC", R6502.iad, R6502.CLC, 1, 2), ("ORA", R6502.aby, R6502.ORA, 3, 4), ii, ii, ii, ("ORA", R6502.abx, R6502.ORA, 3, 4), ("ASL", R6502.abx, R6502.ASL, 3, 7), ii],
    [("JSR", R6502.abs, R6502.JSR, 3, 6), ("AND", R6502.iix, R6502.AND, 2, 6), ii, ii, ("BIT", R6502.zpa, R6502.BIT, 2, 3), ("AND", R6502.zpa, R6502.AND, 2, 3), ("ROL", R6502.zpa, R6502.ROL, 2, 5), ii, ("PLP", R6502.iad, R6502.PLP, 1, 4), ("AND", R6502.imm, R6502.AND, 2, 2), ("ROL", R6502.acc, R6502.ROL, 1, 2), ii, ("BIT", R6502.abs, R6502.BIT, 3, 4), ("AND", R6502.abs, R6502.AND, 3, 4), ("ROL", R6502.abs, R6502.ROL, 3, 6), ii],
    [("BMI", R6502.rad, R6502.BMI, 2, 2), ("AND", R6502.iiy, R6502.AND, 2, 5), ii, ii, ii, ("AND", R6502.zpx, R6502.AND, 2, 4), ("ROL", R6502.zpx, R6502.ROL, 2, 6), ii, ("SEC", R6502.iad, R6502.SEC, 1, 2), ("AND", R6502.aby, R6502.AND, 3, 4), ii, ii, ii, ("AND", R6502.abx, R6502.AND, 3, 4), ("ASL", R6502.abx, R6502.ROL, 3, 7), ii],
    [("RTI", R6502.iad, R6502.RTI, 1, 6), ("EOR", R6502.iix, R6502.EOR, 2, 6), ii, ii, ii, ("EOR", R6502.zpa, R6502.EOR, 2, 3), ("LSR", R6502.zpa, R6502.LSR, 2, 5), ii, ("PHA", R6502.iad, R6502.PHA, 1, 3), ("EOR", R6502.imm, R6502.EOR, 2, 2), ("LSR", R6502.acc, R6502.LSR, 1, 2), ii,  ("JMP", R6502.abs, R6502.JMP, 3, 3), ("EOR", R6502.abs, R6502.EOR, 3, 3), ("LSR", R6502.abs, R6502.JMP, 3, 6), ii],
    [("BVC", R6502.rad, R6502.BVC, 2, 2), ("EOR", R6502.iiy, R6502.EOR, 2, 5), ii, ii, ii, ("EOR", R6502.zpx, R6502.EOR, 2, 4), ("LSR", R6502.zpx, R6502.LSR, 2, 6), ii, ("CLI", R6502.iad, R6502.CLI, 1, 2), ("EOR", R6502.aby, R6502.EOR, 3, 4), ii, ii, ii, ("EOR", R6502.abx, R6502.EOR, 3, 4), ("LSR", R6502.abx, R6502.LSR, 3, 7), ii],
    [("RTS", R6502.iad, R6502.RTS, 1, 6), ("ADC", R6502.iix, R6502.ADC, 2, 6), ii, ii, ii, ("ADC", R6502.zpa, R6502.ADC, 2, 3), ("ROR", R6502.zpa, R6502.ROR, 2, 5), ii, ("PLA", R6502.iad, R6502.PLA, 1, 4), ("ADC", R6502.imm, R6502.ADC, 2, 2), ("ROR", R6502.acc, R6502.ROR, 1, 2), ii, ("JMP", R6502.iad, R6502.JMP, 3, 5), ("ADC", R6502.abs, R6502.ADC, 3, 4), ("ROR", R6502.abs, R6502.ROR, 3, 6), ii],
    [("BVS", R6502.rad, R6502.BVS, 2, 2), ("ADC", R6502.iiy, R6502.BVS, 2, 5), ii, ii, ii, ("ADC", R6502.zpx, R6502.ADC, 2, 4), ("ROR", R6502.zpx, R6502.ROR, 2, 6), ii, ("SEI", R6502.iad, R6502.SEI, 1, 2), ("ADC", R6502.aby, R6502.ADC, 3, 4), ii, ii, ii, ("ADC", R6502.abx, R6502.ADC, 3, 4), ("ROR", R6502.abx, R6502.ROR, 3, 7), ii],
    [ii, ("STA", R6502.iix, R6502.STA, 2, 6), ii, ii, ("STY", R6502.zpa, R6502.STY, 2, 3), ("STA", R6502.zpa, R6502.STA, 2, 3), ("STX", R6502.zpa, R6502.STX, 2, 3), ii, ("DEY", R6502.iad, R6502.DEY, 1, 2), ii, ("TXA", R6502.iad, R6502.TXA, 1, 2), ii, ("STY", R6502.abs, R6502.STY, 3, 4), ("STA", R6502.abs, R6502.STA, 3, 4), ("STX", R6502.abs, R6502.STX, 3, 4), ii],
    [("BCC", R6502.rad, R6502.BCC, 2, 2), ("STA", R6502.iiy, R6502.STA, 2, 6), ii, ii, ("STY", R6502.zpx, R6502.STY, 2, 4), ("STA", R6502.zpx, R6502.STA, 2, 4), ("STX", R6502.zpy, R6502.STX, 2, 4), ii, ("TYA", R6502.iad, R6502.BCC, 1, 2), ("STA", R6502.aby, R6502.BCC, 3, 5), ("TXS", R6502.iad, R6502.BCC, 1, 2), ii, ii, ("STA", R6502.abx, R6502.STA, 3, 5), ii, ii],
    [("LDY", R6502.imm, R6502.LDY, 2, 2), ("LDA", R6502.iix, R6502.LDA, 2, 6), ("LDX", R6502.imm, R6502.LDX, 2, 2), ii, ("LDY", R6502.zpa, R6502.LDY, 2, 3), ("LDA", R6502.zpa, R6502.LDA, 2, 3), ("LDX", R6502.zpa, R6502.LDX, 2, 3), ii, ("TAY", R6502.iad, R6502.TAY, 1, 2), ("LDA", R6502.imm, R6502.LDA, 2, 2), ("TAX", R6502.iad, R6502.TAX, 1, 2), ii, ("LDY", R6502.abs, R6502.LDY, 3, 4), ("LDA", R6502.abs, R6502.LDA, 3, 4), ("LDX", R6502.abs, R6502.LDX, 3, 4), ii],
    [("BCS", R6502.rad, R6502.BCS, 2, 2), ("LDA", R6502.iiy, R6502.LDA, 2, 5), ii, ii, ("LDY", R6502.zpx, R6502.LDY, 2, 4), ("LDA", R6502.zpx, R6502.LDA, 2, 4), ("LDX", R6502.zpy, R6502.LDX, 2, 4), ii, ("CLV", R6502.iad, R6502.CLV, 1, 2), ("LDA", R6502.aby, R6502.BCS, 3, 4), ("TSX", R6502.iad, R6502.BCS, 1, 2), ii, ("LDY", R6502.abx, R6502.LDY, 3, 4), ("LDA", R6502.abx, R6502.LDA, 3, 4), ("LDX", R6502.aby, R6502.LDX, 3, 4), ii],


    [("CPY", R6502.imm, R6502.CPY, 2, 2), ("CMP", R6502.iix, R6502.CMP, 2, 6), ii, ii, ("CPY", R6502.zpa, R6502.CPY, 2, 3), ("CMP", R6502.zpa, R6502.CMP, 2, 3), ("DEC", R6502.zpa, R6502.DEC, 2, 5), ii, ("INY", R6502.iad, R6502.INY, 1, 2), ("CMP", R6502.imm, R6502.CMP, 2, 2), ("DEX", R6502.iad, R6502.DEX, 1, 2), ii, ("CPY", R6502.abs, R6502.CPY, 1, 2), ("TSX", R6502.abs, R6502.TSY, 1, 2), ("TSX", R6502.abs, R6502.BCS, 1, 2), ii],


    [("BNE", R6502.rad, R6502.BNE, 2, 2), ("ORA", R6502.iiy, 2, 5), ii, ii, ii, ("ORA", R6502.zpx, 2, 4), ("ASL", R6502.zpx, 2, 6), ii, ("CLC", R6502.iad, 1, 2), ("ORA", R6502.aby, 3, 4), ii, ii, ii, ("ORA", R6502.abx, 3, 4), ("ASL", R6502.abx, 3, 7), ii],
    [("CPX", R6502.imm, R6502.CPX, 2, 2), ("ORA", R6502.iiy, 2, 5), ii, ii, ii, ("ORA", R6502.zpx, 2, 4), ("ASL", R6502.zpx, 2, 6), ii, ("CLC", R6502.iad, 1, 2), ("ORA", R6502.aby, 3, 4), ii, ii, ii, ("ORA", R6502.abx, 3, 4), ("ASL", R6502.abx, 3, 7), ii],
    [("BEO", R6502.rad, R6502.BEO, 2, 2), ("ORA", R6502.iiy, 2, 5), ii, ii, ii, ("ORA", R6502.zpx, 2, 4), ("ASL", R6502.zpx, 2, 6), ii, ("CLC", R6502.iad, 1, 2), ("ORA", R6502.aby, 3, 4), ii, ii, ii, ("ORA", R6502.abx, 3, 4), ("ASL", R6502.abx, 3, 7), ii]
]

