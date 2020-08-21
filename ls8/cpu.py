"""
CPU functionality.
Constructor that contains all of the instructions for the CPU
"""

import sys
from main_ops import main_branch
from alu_ops import alu_branch

# Branchtable variables
HLT = 0b00000001 
CALL = 0b01010000
RET = 0b00010001
IRET = 0b00010011
JEQ = 0b01010101
JGE = 0b01011010
JGT = 0b01010111
JLE = 0b01011001
JLT = 0b01011000
JMP = 0b01010100
JNE = 0b01010110


class CPU:
    """Main CPU class."""

    def __init__(self):
        # ram that holds 256 bytes (list of 0)
        self.ram = [0] * 256
        # 8 registers (list of 0)
        self.reg = [0] * 8
        # reg7 resets/defaults to 0xF4
        self.reg[7] = 0XF0
        # internal pc register = 0
        self.pc = 0
        # setup branch table
        self.is_running = False
        # use pattern 00000LGE for FL register
        self.FL = 0b00000000
        # use R5 for interrupt mask, R6 for interrupt status
        self.IM = self.reg[5]
        self.IS = self.reg[6]
        self.main_branch = main_branch
        self.alu_branch = alu_branch



    def ram_read(self, MAR): # MAR = Memory address register
        # uses an address to read and returns the value stored at that address
        return self.ram[MAR]

    def ram_write(self, MAR, MDR): # MDR = Memory data register
        self.ram[MAR] = MDR


    def load(self, filename):
        """Load a program into memory."""

        try:
            address = 0
            with open(filename) as f:
                for line in f:
                    comment_split = line.split('#')
                    n = comment_split[0].strip()
                    if n:
                        value = int(n,2)
                        self.ram[address] = value
                        address += 1
        
        except FileNotFoundError:
            print(f"{sys.argv[0]}: {filename} not found")
        

    def alu(self, op, reg_a, reg_b):
        """
        ALU operations.
        Operations which perform math must bitwise-AND 
        w/ 0xFF (255) to ensure they stay in the range
        of 0 - 255
        """

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
            self.reg[reg_a] &= 0xFF

        elif op == 'MUL':
            self.reg[reg_a] *= self.reg[reg_b]
            self.reg[reg_a] &= 0xFF

        elif op == 'AND':
            self.reg[reg_a] &= self.reg[reg_b]
            self.reg[reg_a] &= 0xFF

        elif op == 'CMP':
            if self.reg[reg_a] == self.reg[reg_b]:
                # set E to true and leave others alone
                self.FL = self.FL | 0b00000001
            elif self.reg[reg_a] > self.reg[reg_b]:
                # set G to true and leave others alone
                self.FL = self.FL | 0b00000010
            elif self.reg[reg_a] < self.reg[reg_b]:
                # set L to true and leave others alone
                self.FL = self.FL | 0b00000100

        elif op == 'DEC':
            self.reg[reg_a] -= 1
            self.reg[reg_a] &= 0xFF

        elif op == 'DIV':
            if self.reg[reg_b]:
                self.reg[reg_a] /= self.reg[reg_b]

            else:
                self.main_branch[HLT]
                raise Exception("Cannot divide by 0")

        elif op == 'INC':
            self.reg[reg_a] += 1
            self.reg[reg_a] &= 0xFF

        elif op == 'MOD':
            if self.reg[reg_b]: 
                self.reg[reg_a] %= self.reg[reg_b]

            else:
                self.main_branch[HLT]
                raise Exception("Cannot divide by 0")

        elif op == 'NOT':
            self.reg[reg_a] = self.reg[reg_a] ^ 0b11111111

        elif op == 'OR':
            self.reg[reg_a] |= self.reg[reg_b]

        elif op == 'SHL':
            self.reg[reg_a] = (self.reg[reg_a] << self.reg[reg_b])

        elif op == 'SHR':
            self.reg[reg_a] = (self.reg[reg_a] >> self.reg[reg_b])

        elif op == 'SUB':
            self.reg[reg_a] -= self.reg[reg_b]

        elif op == 'XOR':
            self.reg[reg_a] = self.reg[reg_a] ^ self.reg[reg_b]

        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        self.is_running = True

        while self.is_running:
            # read the memory address stored in PC and store it in IR(instruction register local to this method)
            ir = self.ram_read(self.pc)

            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

            add_to_pc = (ir >> 6) + 1

            if ir in main_branch.keys():
                self.main_branch[ir](self, operand_a, operand_b)
            elif ir in alu_branch.keys():
                self.alu_branch[ir](self, operand_a, operand_b)

            jumps = [CALL, RET, JEQ, JGE, JGT, JLE, JLT, JMP, JNE, IRET]

            if ir not in jumps:
                self.pc += add_to_pc



