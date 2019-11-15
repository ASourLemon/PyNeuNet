import numpy as np


class R6502_Instruction:

    def __init__(self, op_code):

        op_code_str = "%02X" % op_code

        op_code_low = int(op_code_str[1], 16)
        op_code_high = int(op_code_str[0], 16)

        instruction = instruction_set_matrix[op_code_high][op_code_low]

        self.op_code = op_code
        self.mnemonic = instruction[0]
        self.addressing_function = instruction[1]
        self.execution_function = instruction[2]
        self.cycles = instruction[3]


class R6502:

    # Extra required for Emulation
    def __init__(self):

        self.total_cycles = 0

        self.reg_A = np.uint8(0)              # Accumulator
        self.reg_Y = np.uint8(0)              # Y Register
        self.reg_X = np.uint8(0)              # X Register
        self.reg_PC = np.uint16(0)            # Program Counter
        self.reg_S = np.uint8(0xFD)           # Stack Pointer

        self.flag_N = False         # Negative
        self.flag_V = False         # Overflow
        self.flag_U = True          # Unused
        self.flag_B = True          # Break
        self.flag_D = False         # Decimal / Unused
        self.flag_I = True          # Disable Interrupts
        self.flag_Z = False         # Zero
        self.flag_C = False         # Carry

        self.absolute_address = np.uint16(0x0000)           # Stores the address to read operand
        self.relative_address = np.uint16(0x0000)
        self.working_data = np.uint8(0)                     # Stores the operand to use
        self.is_imp = False

        self.bus = None
        self.current_instruction = None
        self.total_cycles = 0

        self.debug = False

    # Public
    def connect_bus(self, bus):
        self.bus = bus

    def load_instruction(self, instruction):
        self.is_imp = False
        cycles = instruction.addressing_function(self)
        self.working_data = self.read(self.absolute_address)
        return cycles

    def execute_instruction(self, instruction):
        return instruction.execution_function(self)

    def clock(self):
        if self.current_instruction is None or self.current_instruction.cycles == 0:
            op_code = self.read(self.reg_PC)
            self.current_instruction = R6502_Instruction(op_code)
            self.single_line_print()
            self.reg_PC += 1

            load_extra_cycles = self.load_instruction(self.current_instruction)
            execute_extra_cycles = self.execute_instruction(self.current_instruction)
            self.current_instruction.cycles += load_extra_cycles + execute_extra_cycles

        self.current_instruction.cycles -= 1
        self.total_cycles += 1

    def reset(self):
        self.total_cycles = 0
        return 0

    def nmi(self):
        self.push(self.reg_PC >> 8)
        self.push(self.reg_PC)

        self.flag_B = False
        self.flag_U = True
        self.flag_I = True
        p = (int(self.flag_N) << 7) | \
            (int(self.flag_V) << 6) | \
            (int(self.flag_U) << 5) | \
            (int(self.flag_B) << 4) | \
            (int(self.flag_D) << 3) | \
            (int(self.flag_I) << 2) | \
            (int(self.flag_Z) << 1) | \
            (int(self.flag_C) << 0)
        self.push(p)

        self.absolute_address = 0xFFFA
        low = self.read(self.absolute_address) & 0x00FF
        high = self.read(self.absolute_address + 1) & 0x00FF
        self.reg_PC = (high << 8) | low

        self.current_instruction.cycles = 8

    # Debug
    def single_line_print(self):
        if self.debug:
            line = "[%04X]" % self.reg_PC
            line += " %02X" % self.current_instruction.op_code
            line += "  A:" + "%02X" % self.reg_A
            line += "  X:" + "%02X" % self.reg_X
            line += "  Y:" + "%02X" % self.reg_Y
            p = (int(self.flag_N) << 7) | \
                (int(self.flag_V) << 6) | \
                (int(self.flag_U) << 5) | \
                (int(self.flag_B) << 4) | \
                (int(self.flag_D) << 3) | \
                (int(self.flag_I) << 2) | \
                (int(self.flag_Z) << 1) | \
                (int(self.flag_C) << 0)
            line += "  P:" + "%02X" % p
            line += "  SP:" + "%02X" % self.reg_S
            line += "  CYC:" + str(self.total_cycles)
            print(line)

    def print_contents(self):
        print("A:" + " [%02X]" % self.reg_A + " " + str(self.reg_A))
        print("X:" + " [%02X]" % self.reg_X + " " + str(self.reg_X))
        print("PC:" + "[%04X]" % self.reg_PC + " " + str(self.reg_PC))
        print("S:" + " [%02X]" % self.reg_S + " " + str(self.reg_S))
        print()
        print("N:" + str(self.flag_N))
        print("V:" + str(self.flag_V))
        print("U:" + str(self.flag_U))
        print("B:" + str(self.flag_B))
        print("D: " + str(self.flag_D))
        print("I: " + str(self.flag_I))
        print("Z: " + str(self.flag_Z))
        print("C: " + str(self.flag_C))

    def get_internal_state(self):
        if self.current_instruction.cycles != 0:
            return ()
        p = (int(self.flag_N) << 7) | \
            (int(self.flag_V) << 6) | \
            (int(self.flag_U) << 5) | \
            (int(self.flag_B) << 4) | \
            (int(self.flag_D) << 3) | \
            (int(self.flag_I) << 2) | \
            (int(self.flag_Z) << 1) | \
            (int(self.flag_C) << 0)
        i = R6502_Instruction(self.read(self.reg_PC))
        return (self.reg_PC, i.op_code, self.reg_A, self.reg_X, self.reg_Y, p, self.reg_S, self.total_cycles, i.mnemonic)

    #
    # Bus Helpers
    def read(self, address):
        return np.uint8(self.bus.cpu_read(address, True))

    def write(self, address, data):
        self.bus.cpu_write(address, data)

    def check_page_boundary(self, base_address, indexed_address):
        if self.current_instruction.op_code in (0x10, 0x11, 0x19, 0x1C, 0x1D,
                                                0x30, 0x31, 0x39, 0x3C, 0x3D,
                                                0x50, 0x51, 0x59, 0x5C, 0x5D,
                                                0x70, 0x71, 0x79, 0x7C, 0x7D,
                                                0x90,
                                                0xB0, 0xB1, 0xB3, 0xB9, 0xBB, 0xBC, 0xBD, 0xBE, 0xBF,
                                                0xD0, 0xD1, 0xD9, 0xDC, 0xDD,
                                                0xF0, 0xF1, 0xF9, 0xFC, 0xFD):
            return int((base_address & 0xFF00) != (indexed_address & 0xFF00))
        return 0

    #
    # Stack Helpers
    def push(self, value):
        self.write(0x0100 + self.reg_S, value & 0x00FF)
        self.reg_S = (self.reg_S - 1) & 0x00FF

    def pop(self):
        self.reg_S = (self.reg_S + 1) & 0x00FF
        value = self.read(0x0100 + self.reg_S)
        return value & 0x00FF

    #
    # Flags Helpers
    def update_flag_N(self, data):
        self.flag_N = (data & 0x80) != 0x00

    def update_flag_Z(self, data):
        self.flag_Z = data == 0x00

    #
    # Addressing Modes

    # Implied Addressing [Implied] / Acc
    def imp(self):
        self.is_imp = True
        self.working_data = self.reg_A
        return 0

    # Immediate Address [IMM]
    def imm(self):
        self.absolute_address = self.reg_PC
        self.reg_PC += 1
        return 0

    # Absolute Addressing [Absolute]
    def abs(self):
        low_bits = self.read(self.reg_PC)
        self.reg_PC += 1
        high_bits = self.read(self.reg_PC)
        self.reg_PC += 1

        new_address = (high_bits << 8) | low_bits
        self.absolute_address = new_address

        return 0

    # X Index Absolute Addressing [ABS, X]
    def abx(self):
        low_bits = self.read(self.reg_PC)
        self.reg_PC += 1
        high_bits = self.read(self.reg_PC)
        self.reg_PC += 1

        base_address = ((high_bits << 8) | low_bits)
        indexed_address = (base_address + self.reg_X)
        self.absolute_address = indexed_address

        return self.check_page_boundary(base_address, indexed_address)

    # X Index Absolute Addressing [ABS, Y]
    def aby(self):
        low_bits = self.read(self.reg_PC)
        self.reg_PC += 1
        high_bits = self.read(self.reg_PC)
        self.reg_PC += 1

        base_address = ((high_bits << 8) | low_bits) & 0xFFFF
        indexed_address = (base_address + self.reg_Y) & 0xFFFF
        self.absolute_address = indexed_address

        return self.check_page_boundary(base_address, indexed_address)

    # Zero Page Addressing [ZP]
    def zpa(self):
        new_address = self.read(self.reg_PC) & 0x00FF
        self.absolute_address = new_address
        self.reg_PC += 1
        return 0

    # X Indexed Zero Page Addressing [ZP, X]
    def zpx(self):
        new_address = (self.read(self.reg_PC) + self.reg_X) & 0x00FF
        self.absolute_address = new_address
        self.reg_PC += 1
        return 0

    # Y Indexed Zero Page Addressing [ZP, Y]
    def zpy(self):
        new_address = (self.read(self.reg_PC) + self.reg_Y) & 0x00FF
        self.absolute_address = new_address
        self.reg_PC += 1
        return 0

    # Relative Addressing [Relative]
    def rel(self):
        self.relative_address = self.read(self.reg_PC)
        self.reg_PC += 1

        if self.relative_address & 0x80:
            self.relative_address |= 0xFF00

        self.absolute_address = (self.reg_PC + self.relative_address) & 0xFFFF
        return 0

    # Indexed Indirect Addressing [(IND, X)]
    def izx(self):
        zp = self.read(self.reg_PC)
        self.reg_PC += 1

        low_bits = self.read((zp + self.reg_X) & 0x00FF)
        high_bits = self.read((zp + self.reg_X + 1) & 0x00FF)

        new_address = (high_bits << 8) | low_bits
        self.absolute_address = new_address
        return 0

    # Indirect Indexed Addressing [(IND), Y]
    def izy(self):
        zp = self.read(self.reg_PC)
        self.reg_PC += 1

        low_bits = self.read(zp & 0x00FF)
        high_bits = self.read((zp + 1) & 0x00FF)

        base_address = ((high_bits << 8) | low_bits) & 0xFFFF
        indexed_address = (base_address + self.reg_Y) & 0xFFFF

        self.absolute_address = indexed_address
        return self.check_page_boundary(base_address, indexed_address)

    # Absolute Indirect [Indirect]
    def ind(self):

        ptr_low = self.read(self.reg_PC)
        self.reg_PC += 1
        ptr_high = self.read(self.reg_PC)
        self.reg_PC += 1

        actual_ptr = (ptr_high << 8) | ptr_low

        data_low = self.read(actual_ptr)
        if ptr_low == 0x00FF:
            data_high = self.read(actual_ptr & 0xFF00)
        else:
            data_high = self.read(actual_ptr + 1)

        new_address = ((data_high << 8) | data_low) & 0xFFFF
        self.absolute_address = new_address
        return 0

    # Opcodes

    # A
    # A + M + C -> A
    def ADC(self):

        result = self.reg_A + self.working_data + int(self.flag_C)

        result_converted = result & 0x00FF

        self.flag_C = (result > 0xFF)
        self.update_flag_Z(result_converted)

        self.flag_V = ((~(self.reg_A ^ self.working_data) & (self.reg_A ^ result)) & 0x0080) != 0

        self.update_flag_N(result_converted)

        self.reg_A = result_converted
        return 0

    # A & M -> A
    def AND(self):
        self.reg_A &= self.working_data
        self.update_flag_Z(self.reg_A)
        self.update_flag_N(self.reg_A)
        return 0

    #
    def ASL(self):
        self.working_data <<= 1
        self.flag_C = (self.working_data & 0xFF00) > 0
        self.working_data &= 0x00FF
        self.update_flag_N(self.working_data)
        self.update_flag_Z(self.working_data)
        if self.is_imp:
            self.reg_A = self.working_data
        else:
            self.write(self.absolute_address, self.working_data)
        return 0

    # B
    # Branch if C = 0
    def BCC(self):
        if not self.flag_C:
            extra_cycles = self.check_page_boundary(self.reg_PC, self.absolute_address)
            self.reg_PC = self.absolute_address
            return extra_cycles + 1
        return 0

    # Branch if C = 1
    def BCS(self):
        if self.flag_C:
            extra_cycles = self.check_page_boundary(self.reg_PC, self.absolute_address)
            self.reg_PC = self.absolute_address
            return extra_cycles + 1
        return 0

    # Branch if Z = 1
    def BEQ(self):
        if self.flag_Z:
            extra_cycles = self.check_page_boundary(self.reg_PC, self.absolute_address)
            self.reg_PC = self.absolute_address
            return extra_cycles + 1
        return 0

    # A BitAND M
    def BIT(self):
        result = self.reg_A & self.working_data
        self.update_flag_Z(result)
        self.flag_N = (self.working_data & (1 << 7)) != 0
        self.flag_V = (self.working_data & (1 << 6)) != 0
        return 0

    # Branch if N = 1
    def BMI(self):
        if self.flag_N:
            extra_cycles = self.check_page_boundary(self.reg_PC, self.absolute_address)
            self.reg_PC = self.absolute_address
            return extra_cycles + 1
        return 0

    # Branch if Z = 0
    def BNE(self):
        if not self.flag_Z:
            extra_cycles = self.check_page_boundary(self.reg_PC, self.absolute_address)
            self.reg_PC = self.absolute_address
            return extra_cycles + 1
        return 0

    # Branch if N = 0
    def BPL(self):
        if not self.flag_N:
            extra_cycles = self.check_page_boundary(self.reg_PC, self.absolute_address)
            self.reg_PC = self.absolute_address
            return extra_cycles + 1
        return 0

    #
    def BRK(self):
        self.flag_B = True
        self.flag_U = True
        return 0

    # Branch if V = 0
    def BVC(self):
        if not self.flag_V:
            extra_cycles = self.check_page_boundary(self.reg_PC, self.absolute_address)
            self.reg_PC = self.absolute_address
            return extra_cycles + 1
        return 0

    # Branch if V = 1
    def BVS(self):
        if self.flag_V:
            extra_cycles = self.check_page_boundary(self.reg_PC, self.absolute_address)
            self.reg_PC = self.absolute_address
            return extra_cycles + 1
        return 0

    # C
    # 0 -> C
    def CLC(self):
        self.flag_C = False
        return 0

    # 0 -> D
    def CLD(self):
        self.flag_D = False
        return 0

    # 0 -> I
    def CLI(self):
        self.flag_I = False
        return 0

    # 0 -> V
    def CLV(self):
        self.flag_V = False
        return 0

    # A - M
    def CMP(self):
        result = (self.reg_A - self.working_data)
        self.update_flag_N(result & 0x00FF)
        self.update_flag_Z(result & 0x00FF)
        self.flag_C = self.reg_A >= self.working_data
        return 0

    # X - M
    def CPX(self):
        result = self.reg_X - self.working_data
        self.update_flag_N(result)
        self.update_flag_Z(result)
        self.flag_C = self.reg_X >= self.working_data
        return 0

    # Y - M
    def CPY(self):
        result = self.reg_Y - self.working_data
        self.update_flag_N(result)
        self.update_flag_Z(result)
        self.flag_C = self.reg_Y >= self.working_data
        return 0

    # D
    # M - 1 -> M
    def DEC(self):
        self.working_data = (self.working_data - 1) & 0x00FF
        self.write(self.absolute_address, self.working_data)
        self.update_flag_N(self.working_data)
        self.update_flag_Z(self.working_data)
        return 0

    # X - 1 -> X
    def DEX(self):
        self.reg_X = (self.reg_X - 1) & 0x00FF
        self.update_flag_N(self.reg_X)
        self.update_flag_Z(self.reg_X)
        return 0

    # Y - 1 -> Y
    def DEY(self):
        self.reg_Y = (self.reg_Y - 1) & 0x00FF
        self.update_flag_N(self.reg_Y)
        self.update_flag_Z(self.reg_Y)
        return 0

    # E
    # A BitOR M -> A
    def EOR(self):
        self.reg_A ^= self.working_data
        self.update_flag_Z(self.reg_A)
        self.update_flag_N(self.reg_A)
        return 0

    # I
    # M + 1 -> M
    def INC(self):
        self.working_data = (self.working_data + 1) & 0x00FF
        self.write(self.absolute_address, self.working_data)
        self.update_flag_N(self.working_data)
        self.update_flag_Z(self.working_data)
        return 0

    # X + 1 -> X
    def INX(self):
        self.reg_X = (self.reg_X + 1) & 0x00FF
        self.update_flag_N(self.reg_X)
        self.update_flag_Z(self.reg_X)
        return 0

    # Y - 1 -> Y
    def INY(self):
        self.reg_Y = (self.reg_Y + 1) & 0x00FF
        self.update_flag_N(self.reg_Y)
        self.update_flag_Z(self.reg_Y)
        return 0

    # J
    # LOCATION -> PC
    def JMP(self):
        self.reg_PC = self.absolute_address
        return 0

    # PC -> M[STK]; LOCATION -> PC
    def JSR(self):

        self.reg_PC -= 1

        self.push((self.reg_PC >> 8) & 0x00FF)
        self.push(self.reg_PC & 0x00FF)

        self.reg_PC = self.absolute_address

        return 0

    # L
    # M -> A
    def LDA(self):
        self.reg_A = self.working_data
        self.update_flag_Z(self.reg_A)
        self.update_flag_N(self.reg_A)
        return 0

    # M -> X
    def LDX(self):
        self.reg_X = self.working_data
        self.update_flag_Z(self.reg_X)
        self.update_flag_N(self.reg_X)
        return 0

    # M -> Y
    def LDY(self):
        self.reg_Y = self.working_data
        self.update_flag_Z(self.reg_Y)
        self.update_flag_N(self.reg_Y)
        return 0

    # M/A >> 1 -> M/A
    def LSR(self):
        self.flag_C = (self.working_data & 0x0001) != 0
        self.working_data >>= 1
        self.working_data &= 0x00FF
        self.update_flag_N(self.working_data)
        self.update_flag_Z(self.working_data)
        if self.is_imp:
            self.reg_A = self.working_data
        else:
            self.write(self.absolute_address, self.working_data)
        return 0

    # N
    # NO OPERATION
    def NOP(self):
        return 0

    # O
    # A BitOR M -> A
    def ORA(self):
        self.reg_A |= self.working_data
        self.update_flag_Z(self.reg_A)
        self.update_flag_N(self.reg_A)
        return 0

    # P
    # A -> M[STK]; STK - 1 -> STK
    def PHA(self):
        self.push(self.reg_A)
        return 0

    # P -> M[STK]; STK - 1 -> STK
    def PHP(self):
        p = (int(self.flag_N) << 7) | \
            (int(self.flag_V) << 6) | \
            (int(True) << 5) | \
            (int(True) << 4) | \
            (int(self.flag_D) << 3) | \
            (int(self.flag_I) << 2) | \
            (int(self.flag_Z) << 1) | \
            (int(self.flag_C) << 0)

        self.push(p)
        return 0

    # STK + 1 -> STK; M[STK] -> A
    def PLA(self):
        self.reg_A = self.pop()
        self.update_flag_N(self.reg_A)
        self.update_flag_Z(self.reg_A)
        return 0

    # STK + 1 -> STK; M[STK] -> P
    def PLP(self):
        p = self.pop()

        self.flag_C = (p & 0x01) != 0
        self.flag_Z = (p & 0x02) != 0
        self.flag_I = (p & 0x04) != 0
        self.flag_D = (p & 0x08) != 0
        #self.flag_B = (p & 0x10) != 0
        #self.flag_U = (p & 0x20) != 0
        self.flag_V = (p & 0x40) != 0
        self.flag_N = (p & 0x80) != 0

        return 0

    # R
    #
    def ROL(self):
        self.working_data = self.working_data << 1 | int(self.flag_C)
        self.flag_C = (self.working_data & 0xFF00) != 0
        self.working_data &= 0x00FF
        self.update_flag_N(self.working_data)
        self.update_flag_Z(self.working_data)
        if self.is_imp:
            self.reg_A = self.working_data
        else:
            self.write(self.absolute_address, self.working_data)
        return 0

    #
    def ROR(self):

        result = int(self.flag_C) << 7 | self.working_data >> 1

        self.flag_C = (self.working_data & 0x01) != 0
        result &= 0x00FF
        self.update_flag_N(result)
        self.update_flag_Z(result)

        if self.is_imp:
            self.reg_A = result
        else:
            self.write(self.absolute_address, result)
        self.working_data = result
        return 0

    #
    def RTI(self):

        p = self.pop()

        self.flag_C = (p & 0x01) != 0
        self.flag_Z = (p & 0x02) != 0
        self.flag_I = (p & 0x04) != 0
        self.flag_D = (p & 0x08) != 0
        #self.flag_B = (p & 0x10) != 0
        #self.flag_U = (p & 0x20) != 0
        self.flag_V = (p & 0x40) != 0
        self.flag_N = (p & 0x80) != 0

        pc_low = self.pop()
        pc_high = self.pop()

        self.reg_PC = (pc_high << 8) | pc_low

        return 0

    # M[STK] -> PC; PC + 1 -> PC
    def RTS(self):

        pc_low = self.pop()
        pc_high = self.pop()

        self.reg_PC = (pc_high << 8) | pc_low
        self.reg_PC += 1
        return 0

    # S
    # A - M - C -> A
    def SBC(self):

        neg_working_data = self.working_data ^ 0x00FF

        result = self.reg_A + neg_working_data + int(self.flag_C)
        result_converted = result & 0x00FF

        self.flag_C = (result & 0xFF00) != 0
        self.update_flag_Z(result_converted)

        self.flag_V = (((result ^ self.reg_A) & (result ^ neg_working_data)) & 0x0080) != 0

        self.update_flag_N(result_converted)

        self.reg_A = result_converted
        return 0

    # 1 -> C
    def SEC(self):
        self.flag_C = True
        return 0

    # 1 -> D I
    def SED(self):
        self.flag_D = True
        return 0

    # 1 -> I
    def SEI(self):
        self.flag_I = True
        return 0

    # A -> M
    def STA(self):
        self.write(self.absolute_address, self.reg_A)
        return 0

    # X -> M
    def STX(self):
        self.write(self.absolute_address, self.reg_X)
        return 0

    # Y -> M
    def STY(self):
        self.write(self.absolute_address, self.reg_Y)
        return 0

    # T
    # A -> X
    def TAX(self):
        self.reg_X = self.reg_A
        self.update_flag_N(self.reg_X)
        self.update_flag_Z(self.reg_X)
        return 0

    # A -> Y
    def TAY(self):
        self.reg_Y = self.reg_A
        self.update_flag_N(self.reg_Y)
        self.update_flag_Z(self.reg_Y)
        return 0

    # S -> X
    def TSX(self):
        self.reg_X = self.reg_S
        self.update_flag_N(self.reg_X)
        self.update_flag_Z(self.reg_X)
        return 0

    # X -> A
    def TXA(self):
        self.reg_A = self.reg_X
        self.update_flag_N(self.reg_A)
        self.update_flag_Z(self.reg_A)
        return 0

    # X -> S
    def TXS(self):
        self.reg_S = self.reg_X
        return 0

    # Y -> A
    def TYA(self):
        self.reg_A = self.reg_Y
        self.update_flag_N(self.reg_A)
        self.update_flag_Z(self.reg_A)
        return 0

    # X
    # Illegal instructions
    def KILL(self):
        return 0
    # A
    def ANC(self):
        return 0
    def ALR(self):
        return 0
    def AHX(self):
        return 0
    def ARR(self):
        return 0
    def AXS(self):
        return 0
    # D
    def DCP(self):
        self.DEC()
        self.CMP()
        return 0
    # I
    def ISC(self):
        self.INC()
        self.SBC()
        return 0
    # L
    def LAS(self):
        return 0
    def LAX(self):
        self.LDA()
        self.LDX()
        return 0
    # R
    def RLA(self):
        self.ROL()
        self.AND()
        return 0
    def RRA(self):
        self.ROR()
        self.ADC()
        return 0
    # S
    def SAX(self):
        self.working_data = self.reg_A & self.reg_X
        self.write(self.absolute_address, self.working_data)
        return 0
    def SHY(self):
        return 0
    def SHX(self):
        return 0
    def SRE(self):
        self.LSR()
        self.EOR()
        return 0


    def SLO(self):
        self.ASL()
        self.ORA()
        return 0
    # T
    def TAS(self):
        return 0
    # X
    def XAA(self):
        return 0


    # Instruction Set Matrix
kill_instruction = ("KILL", R6502.imp, R6502.KILL, 9, 9)

instruction_set_matrix = [
    # 0
    [("BRK", R6502.imp, R6502.BRK, 7),
     ("ORA", R6502.izx, R6502.ORA, 6),
     kill_instruction,
     ("SLO", R6502.izx, R6502.SLO, 8),
     ("NOP", R6502.zpa, R6502.NOP, 3),
     ("ORA", R6502.zpa, R6502.ORA, 3),
     ("ASL", R6502.zpa, R6502.ASL, 5),
     ("SLO", R6502.zpa, R6502.SLO, 5),
     ("PHP", R6502.imp, R6502.PHP, 3),
     ("ORA", R6502.imm, R6502.ORA, 2),
     ("ASL", R6502.imp, R6502.ASL, 2),
     ("ANC", R6502.imm, R6502.ANC, 2),
     ("NOP", R6502.abs, R6502.NOP, 4),
     ("ORA", R6502.abs, R6502.ORA, 4),
     ("ASL", R6502.abs, R6502.ASL, 6),
     ("SLO", R6502.abs, R6502.SLO, 6)],
    # 1
    [("BPL", R6502.rel, R6502.BPL, 2),
     ("ORA", R6502.izy, R6502.ORA, 5),
     kill_instruction,
     ("SLO", R6502.izy, R6502.SLO, 8),
     ("NOP", R6502.zpx, R6502.NOP, 4),
     ("ORA", R6502.zpx, R6502.ORA, 4),
     ("ASL", R6502.zpx, R6502.ASL, 6),
     ("SLO", R6502.zpx, R6502.SLO, 6),
     ("CLC", R6502.imp, R6502.CLC, 2),
     ("ORA", R6502.aby, R6502.ORA, 4),
     ("NOP", R6502.imp, R6502.NOP, 2),
     ("SLO", R6502.aby, R6502.SLO, 7),
     ("NOP", R6502.abx, R6502.NOP, 4),
     ("ORA", R6502.abx, R6502.ORA, 4),
     ("ASL", R6502.abx, R6502.ASL, 7),
     ("SLO", R6502.abx, R6502.SLO, 7)],
    # 2
    [("JSR", R6502.abs, R6502.JSR, 6),
     ("AND", R6502.izx, R6502.AND, 6),
     kill_instruction,
     ("RLA", R6502.izx, R6502.RLA, 8),
     ("BIT", R6502.zpa, R6502.BIT, 3),
     ("AND", R6502.zpa, R6502.AND, 3),
     ("ROL", R6502.zpa, R6502.ROL, 5),
     ("RLA", R6502.zpa, R6502.RLA, 5),
     ("PLP", R6502.imp, R6502.PLP, 4),
     ("AND", R6502.imm, R6502.AND, 2),
     ("ROL", R6502.imp, R6502.ROL, 2),
     ("ANC", R6502.imp, R6502.ANC, 2),
     ("BIT", R6502.abs, R6502.BIT, 4),
     ("AND", R6502.abs, R6502.AND, 4),
     ("ROL", R6502.abs, R6502.ROL, 6),
     ("RLA", R6502.abs, R6502.RLA, 6)],
    # 3
    [("BMI", R6502.rel, R6502.BMI, 2),
     ("AND", R6502.izy, R6502.AND, 5),
     kill_instruction,
     ("RLA", R6502.izy, R6502.RLA, 8),
     ("NOP", R6502.zpx, R6502.NOP, 4),
     ("AND", R6502.zpx, R6502.AND, 4),
     ("ROL", R6502.zpx, R6502.ROL, 6),
     ("RLA", R6502.zpx, R6502.RLA, 6),
     ("SEC", R6502.imp, R6502.SEC, 2),
     ("AND", R6502.aby, R6502.AND, 4),
     ("NOP", R6502.imp, R6502.NOP, 2),
     ("RLA", R6502.aby, R6502.RLA, 7),
     ("NOP", R6502.abx, R6502.NOP, 4),
     ("AND", R6502.abx, R6502.AND, 4),
     ("ROL", R6502.abx, R6502.ROL, 7),
     ("RLA", R6502.abx, R6502.RLA, 7)],
    # 4
    [("RTI", R6502.imp, R6502.RTI, 6),
     ("EOR", R6502.izx, R6502.EOR, 6),
     kill_instruction,
     ("SRE", R6502.izx, R6502.SRE, 8),
     ("NOP", R6502.zpa, R6502.NOP, 3),
     ("EOR", R6502.zpa, R6502.EOR, 3),
     ("LSR", R6502.zpa, R6502.LSR, 5),
     ("SRE", R6502.zpa, R6502.SRE, 5),
     ("PHA", R6502.imp, R6502.PHA, 3),
     ("EOR", R6502.imm, R6502.EOR, 2),
     ("LSR", R6502.imp, R6502.LSR, 2),
     ("ALR", R6502.imm, R6502.ALR, 2),
     ("JMP", R6502.abs, R6502.JMP, 3),
     ("EOR", R6502.abs, R6502.EOR, 4),
     ("LSR", R6502.abs, R6502.LSR, 6),
     ("SRE", R6502.abs, R6502.SRE, 6)],
    # 5
    [("BVC", R6502.rel, R6502.BVC, 2),
     ("EOR", R6502.izy, R6502.EOR, 5),
     kill_instruction,
     ("SRE", R6502.izy, R6502.SRE, 8),
     ("NOP", R6502.zpx, R6502.NOP, 4),
     ("EOR", R6502.zpx, R6502.EOR, 4),
     ("LSR", R6502.zpx, R6502.LSR, 6),
     ("SRE", R6502.zpx, R6502.SRE, 6),
     ("CLI", R6502.imp, R6502.CLI, 2),
     ("EOR", R6502.aby, R6502.EOR, 4),
     ("NOP", R6502.imp, R6502.NOP, 2),
     ("SRE", R6502.aby, R6502.SRE, 7),
     ("NOP", R6502.abx, R6502.NOP, 4),
     ("EOR", R6502.abx, R6502.EOR, 4),
     ("LSR", R6502.abx, R6502.LSR, 7),
     ("SRE", R6502.abx, R6502.SRE, 7)],
    # 6
    [("RTS", R6502.imp, R6502.RTS, 6),
     ("ADC", R6502.izx, R6502.ADC, 6),
     kill_instruction,
     ("RRA", R6502.izx, R6502.RRA, 8),
     ("NOP", R6502.zpa, R6502.NOP, 3),
     ("ADC", R6502.zpa, R6502.ADC, 3),
     ("ROR", R6502.zpa, R6502.ROR, 5),
     ("RRA", R6502.zpa, R6502.RRA, 5),
     ("PLA", R6502.imp, R6502.PLA, 4),
     ("ADC", R6502.imm, R6502.ADC, 2),
     ("ROR", R6502.imp, R6502.ROR, 2),
     ("ARR", R6502.imm, R6502.ARR, 2),
     ("JMP", R6502.ind, R6502.JMP, 5),
     ("ADC", R6502.abs, R6502.ADC, 4),
     ("ROR", R6502.abs, R6502.ROR, 6),
     ("RRA", R6502.abs, R6502.RRA, 6)],
    # 7
    [("BVS", R6502.rel, R6502.BVS, 2),
     ("ADC", R6502.izy, R6502.ADC, 5),
     kill_instruction,
     ("RRA", R6502.izy, R6502.RRA, 8),
     ("NOP", R6502.zpx, R6502.NOP, 4),
     ("ADC", R6502.zpx, R6502.ADC, 4),
     ("ROR", R6502.zpx, R6502.ROR, 6),
     ("RRA", R6502.zpx, R6502.RRA, 6),
     ("SEI", R6502.imp, R6502.SEI, 2),
     ("ADC", R6502.aby, R6502.ADC, 4),
     ("NOP", R6502.imp, R6502.NOP, 2),
     ("RRA", R6502.aby, R6502.RRA, 7),
     ("NOP", R6502.abx, R6502.ARR, 4),
     ("ADC", R6502.abx, R6502.ADC, 4),
     ("ROR", R6502.abx, R6502.ROR, 7),
     ("RRA", R6502.abx, R6502.RRA, 7)],
    # 8
    [("NOP", R6502.imm, R6502.NOP, 2),
     ("STA", R6502.izx, R6502.STA, 6),
     ("NOP", R6502.imm, R6502.NOP, 2),
     ("SAX", R6502.izx, R6502.SAX, 6),
     ("STY", R6502.zpa, R6502.STY, 3),
     ("STA", R6502.zpa, R6502.STA, 3),
     ("STX", R6502.zpa, R6502.STX, 3),
     ("SAX", R6502.zpa, R6502.SAX, 3),
     ("DEY", R6502.imp, R6502.DEY, 2),
     ("NOP", R6502.imm, R6502.NOP, 2),
     ("TXA", R6502.imp, R6502.TXA, 2),
     ("XAA", R6502.imm, R6502.XAA, 2),
     ("STY", R6502.abs, R6502.STY, 4),
     ("STA", R6502.abs, R6502.STA, 4),
     ("STX", R6502.abs, R6502.STX, 4),
     ("SAX", R6502.abs, R6502.SAX, 4)],
    # 9
    [("BCC", R6502.rel, R6502.BCC, 2),
     ("STA", R6502.izy, R6502.STA, 6),
     kill_instruction,
     ("AHX", R6502.izy, R6502.AHX, 6),
     ("STY", R6502.zpx, R6502.STY, 4),
     ("STA", R6502.zpx, R6502.STA, 4),
     ("STX", R6502.zpy, R6502.STX, 4),
     ("SAX", R6502.zpy, R6502.SAX, 4),
     ("TYA", R6502.imp, R6502.TYA, 2),
     ("STA", R6502.aby, R6502.STA, 5),
     ("TXS", R6502.imp, R6502.TXS, 2),
     ("TAS", R6502.aby, R6502.TAS, 5),
     ("SHY", R6502.abx, R6502.SHY, 5),
     ("STA", R6502.abx, R6502.STA, 5),
     ("SHX", R6502.aby, R6502.SHX, 5),
     ("AHX", R6502.aby, R6502.AHX, 5)],
    # A
    [("LDY", R6502.imm, R6502.LDY, 2),
     ("LDA", R6502.izx, R6502.LDA, 6),
     ("LDX", R6502.imm, R6502.LDX, 2),
     ("LAX", R6502.izx, R6502.LAX, 6),
     ("LDY", R6502.zpa, R6502.LDY, 3),
     ("LDA", R6502.zpa, R6502.LDA, 3),
     ("LDX", R6502.zpa, R6502.LDX, 3),
     ("LAX", R6502.zpa, R6502.LAX, 3),
     ("TAY", R6502.imp, R6502.TAY, 2),
     ("LDA", R6502.imm, R6502.LDA, 2),
     ("TAX", R6502.imp, R6502.TAX, 2),
     ("LAX", R6502.imm, R6502.LAX, 2),
     ("LDY", R6502.abs, R6502.LDY, 4),
     ("LDA", R6502.abs, R6502.LDA, 4),
     ("LDX", R6502.abs, R6502.LDX, 4),
     ("LAX", R6502.abs, R6502.LAX, 4)],
    # B
    [("BCS", R6502.rel, R6502.BCS, 2),
     ("LDA", R6502.izy, R6502.LDA, 5),
     kill_instruction,
     ("LAX", R6502.izy, R6502.LAX, 5),
     ("LDY", R6502.zpx, R6502.LDY, 4),
     ("LDA", R6502.zpx, R6502.LDA, 4),
     ("LDX", R6502.zpy, R6502.LDX, 4),
     ("LAX", R6502.zpy, R6502.LAX, 4),
     ("CLV", R6502.imp, R6502.CLV, 2),
     ("LDA", R6502.aby, R6502.LDA, 4),
     ("TSX", R6502.imp, R6502.TSX, 2),
     ("LAS", R6502.aby, R6502.LAS, 4),
     ("LDY", R6502.abx, R6502.LDY, 4),
     ("LDA", R6502.abx, R6502.LDA, 4),
     ("LDX", R6502.aby, R6502.LDX, 4),
     ("LAX", R6502.aby, R6502.LAX, 4)],
    # C
    [("CPY", R6502.imm, R6502.CPY, 2),
     ("CMP", R6502.izx, R6502.CMP, 6),
     ("NOP", R6502.imm, R6502.NOP, 2),
     ("DCP", R6502.izx, R6502.DCP, 8),
     ("CPY", R6502.zpa, R6502.CPY, 3),
     ("CMP", R6502.zpa, R6502.CMP, 3),
     ("DEC", R6502.zpa, R6502.DEC, 5),
     ("DCP", R6502.zpa, R6502.DCP, 5),
     ("INY", R6502.imp, R6502.INY, 2),
     ("CMP", R6502.imm, R6502.CMP, 2),
     ("DEX", R6502.imp, R6502.DEX, 2),
     ("AXS", R6502.imm, R6502.AXS, 2),
     ("CPY", R6502.abs, R6502.CPY, 4),
     ("CMP", R6502.abs, R6502.CMP, 4),
     ("DEC", R6502.abs, R6502.DEC, 6),
     ("DCP", R6502.abs, R6502.DCP, 6)],
    # D
    [("BNE", R6502.rel, R6502.BNE, 2),
     ("CMP", R6502.izy, R6502.CMP, 5),
     kill_instruction,
     ("DCP", R6502.izy, R6502.DCP, 8),
     ("NOP", R6502.zpx, R6502.NOP, 4),
     ("CMP", R6502.zpx, R6502.CMP, 4),
     ("DEC", R6502.zpx, R6502.DEC, 6),
     ("DCP", R6502.zpx, R6502.DCP, 6),
     ("CLD", R6502.imp, R6502.CLD, 2),
     ("CMP", R6502.aby, R6502.CMP, 4),
     ("NOP", R6502.imp, R6502.NOP, 2),
     ("DCP", R6502.aby, R6502.DCP, 7),
     ("NOP", R6502.abx, R6502.NOP, 4),
     ("CMP", R6502.abx, R6502.CMP, 4),
     ("DEC", R6502.abx, R6502.DEC, 7),
     ("DCP", R6502.abx, R6502.DCP, 7)],
    # E
    [("CPX", R6502.imm, R6502.CPX, 2),
     ("SBC", R6502.izx, R6502.SBC, 6),
     ("NOP", R6502.imm, R6502.NOP, 2),
     ("ISC", R6502.izx, R6502.ISC, 8),
     ("CPX", R6502.zpa, R6502.CPX, 3),
     ("SBC", R6502.zpa, R6502.SBC, 3),
     ("INC", R6502.zpa, R6502.INC, 5),
     ("ISC", R6502.zpa, R6502.ISC, 5),
     ("INX", R6502.imp, R6502.INX, 2),
     ("SBC", R6502.imm, R6502.SBC, 2),
     ("NOP", R6502.imp, R6502.NOP, 2),
     ("SBC", R6502.imm, R6502.SBC, 2),
     ("CPX", R6502.abs, R6502.CPX, 4),
     ("SBC", R6502.abs, R6502.SBC, 4),
     ("INC", R6502.abs, R6502.INC, 6),
     ("ISC", R6502.abs, R6502.ISC, 6)],
    # F
    [("BEQ", R6502.rel, R6502.BEQ, 2),
     ("SBC", R6502.izy, R6502.SBC, 5),
     kill_instruction,
     ("ISC", R6502.izy, R6502.ISC, 8),
     ("NOP", R6502.zpx, R6502.NOP, 4),
     ("SBC", R6502.zpx, R6502.SBC, 4),
     ("INC", R6502.zpx, R6502.INC, 6),
     ("ISC", R6502.zpx, R6502.ISC, 6),
     ("SED", R6502.imp, R6502.SED, 2),
     ("SBC", R6502.aby, R6502.SBC, 4),
     ("NOP", R6502.imp, R6502.NOP, 2),
     ("ISC", R6502.aby, R6502.ISC, 7),
     ("NOP", R6502.abx, R6502.NOP, 4),
     ("SBC", R6502.abx, R6502.SBC, 4),
     ("INC", R6502.abx, R6502.INC, 7),
     ("ISC", R6502.abx, R6502.ISC, 7)]
]

