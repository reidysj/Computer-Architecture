"""
CPU functionality.
Constructor that contains all of the instructions for the CPU
"""

import sys

# Branchtable variables
HLT = 0b00000001 
LDI = 0b10000010
PRN = 0b01000111
MUL = 0b10100010
ADD = 0b10100000
PUSH = 0b01000101
POP = 0b01000110
CALL = 0b01010000
RET = 0b00010001
AND = 0b10101000
CMP = 0b10100111
DEC = 0b01100110
DIV = 0b10100011
INC = 0b01100101
INT = 0b01010010
IRET = 0b00010011
JEQ = 0b01010101
JGE = 0b01011010
JGT = 0b01010111
JLE = 0b01011001
JLT = 0b01011000
JMP = 0b01010100
JNE = 0b01010110
LD = 0b10000011
MOD = 0b10100100
NOP = 0b00000000
NOT = 0b01101001
OR = 0b10101010
PRA = 0b01001000
SHL = 0b10101100
SHR = 0b10101101
ST = 0b10000100
SUB = 0b10100001
XOR = 0b10101011

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
        self.FL = 0b11000000
        # use R5 for interrupt mask, R6 for interrupt status
        self.IM = self.reg[5]
        self.IS = self.reg[6]
        # Start branch table setup 
        self.branchtable = {
            HLT : self.handle_HLT,
            LDI : self.handle_LDI,
            PRN : self.handle_PRN,
            MUL : self.handle_MUL,
            ADD : self.handle_ADD,
            PUSH : self.handle_PUSH,
            POP : self.handle_POP,
            CALL : self.handle_CALL,
            RET : self.handle_RET,
            CMP : self.handle_CMP,
            DEC : self.handle_DEC,
            DIV : self.handle_DIV,
            INC : self.handle_INC,
            INT : self.handle_INT,
            IRET : self.handle_IRET,
            JEQ: self.handle_JEQ,
            JGE: self.handle_JGE,
            JGT: self.handle_JGT,
            JLE: self.handle_JLE,
            JLT: self.handle_JLT,
            JMP: self.handle_JMP,
            JNE: self.handle_JNE,
            LD: self.handle_LD,
            MOD: self.handle_MOD,
            NOP: self.handle_NOP,
            NOT: self.handle_NOT,
            OR: self.handle_OR,
            PRA: self.handle_PRA,
            SHL: self.handle_SHL,
            SHR: self.handle_SHR,
            ST: self.handle_ST,
            SUB: self.handle_SUB,
            XOR: self.handle_XOR
        }
        # End branch table setup


    # branch table methods
    def handle_HLT(self, *args):
        self.is_running = False

    def handle_LDI(self, operand_a, operand_b):
        self.reg[operand_a] = operand_b

    def handle_PRN(self, operand_a, operand_b):
        print(self.reg[operand_a])

    def handle_PUSH(self, operand, *args):
        val = self.reg[operand]
        self.reg[7] -= 1
        self.ram[self.reg[7]] = val

    def handle_POP(self, operand, *args):
        val = self.ram[self.reg[7]]
        self.reg[operand] = val
        self.reg[7] += 1

    def handle_CALL(self, operand_a, operand_b):
        addr = self.reg[operand_a]
        rtn_addr = self.pc + 2
        self.reg[7] -= 1  
        sp = self.reg[7]  
        self.ram[sp] = rtn_addr 
        self.pc = addr

    def handle_RET(self, *args):
        rtn_addr = self.ram[self.reg[7]]
        self.reg[7] += 1
        self.pc = rtn_addr
    
    def handle_INT(self, operand, *args):
        # set r6's nth bit to the value in the given reg
        # use hashing w/ or to preserve all other digits
        # hashing number will be a 1 squished over by the amount of the value
        self.reg[6] |= (1 << self.reg[operand])

    def handle_IRET(self, *args):
        # pop r6-r0 off the stack in that order
        for i in range(6, -1, -1):
            self.handle_POP(i)
        # pop the FL reg off the stack
        self.FL = self.ram_read(self.reg[7])
        self.reg[7] += 1
        # pop the return address off and store it in pc
        self.pc = self.reg[7]
        #TODO re-enable interupts (?)


    def handle_JEQ(self, operand, *args):
        if self.FL & 0b00000001:
            self.pc = self.reg[operand]
        else:
            self.pc += 2

    def handle_JGE(self, operand, *args):
        if self.FL & 0b00000011:
            self.pc = self.reg[operand]
        else:
            self.pc += 2

    def handle_JGT(self, operand, *args):
        if self.FL & 0b00000010:
            self.pc = self.reg[operand]
        else:
            self.pc += 2

    def handle_JLE(self, operand, *args):
        if self.FL & 0b00000110:
            self.pc = self.reg[operand]
        else:
            self.pc += 2

    def handle_JLT(self, operand, *args):
        if self.FL & 0b00001000:
            self.pc = self.reg[operand]
        else:
            self.pc += 2

    def handle_JMP(self, operand, *args):
        self.pc = self.reg[operand]

    def handle_JNE(self, operand, *args):
        if not self.FL & 0b00000001:
            self.pc = self.reg[operand]
        else: 
            self.pc += 2

    def handle_LD(self, operand_a, operand_b):
        self.reg[operand_a] = self.ram[self.reg[operand_b]]

    def handle_NOP(self, *args):
        pass

    def handle_PRA(self, operand, *args):
        letter = self.reg[operand]
        print(chr(letter))

    def handle_ST(self, operand_a, operand_b):
        self.ram_write(self.reg[operand_a], self.reg[operand_b])

    # start alu branch table methods

    def handle_MUL(self, operand_a, operand_b):
        self.alu('MUL', operand_a, operand_b)

    def handle_ADD(self, operand_a, operand_b):
        self.alu('ADD', operand_a, operand_b)

    def handle_AND(self, operand_a, operand_b):
        self.alu('AND', operand_a, operand_b)

    def handle_CMP(self, operand_a, operand_b):
        self.alu('CMP', operand_a, operand_b)

    def handle_DEC(self, operand_a, operand_b):
        self.alu('DEC', operand_a, operand_b)

    def handle_DIV(self, operand_a, operand_b):
        self.alu('DIV', operand_a, operand_b)
    
    def handle_INC(self, operand_a, operand_b):
        self.alu('INC', operand_a, operand_b)

    def handle_MOD(self, operand_a, operand_b):
        self.alu('MOD', operand_a, operand_b)

    def handle_NOT(self, operand_a, operand_b):
        self.alu('NOT', operand_a, operand_b)

    def handle_OR(self, operand_a, operand_b):
        self.alu('OR', operand_a, operand_b)

    def handle_SHL(self, operand_a, operand_b):
        self.alu('SHL', operand_a, operand_b)
    
    def handle_SHR(self, operand_a, operand_b):
        self.alu('SHR', operand_a, operand_b)

    def handle_SUB(self, operand_a, operand_b):
        self.alu('SUB', operand_a, operand_b)

    def handle_XOR(self, operand_a, operand_b):
        self.alu('XOR', operand_a, operand_b)

    # end branch table methods

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
        """ALU operations."""

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
            self.FL = self.FL & 0b11111000

            if self.reg[reg_a] == self.reg[reg_b]:
                self.FL = self.FL | 0b00000001
            elif self.reg[reg_a] > self.reg[reg_b]:
                self.FL = self.FL | 0b00000010
            elif self.reg[reg_a] < self.reg[reg_b]:
                self.FL = self.FL | 0b00000100

        elif op == 'DEC':
            self.reg[reg_a] -= 1
            self.reg[reg_a] &= 0xFF

        elif op == 'DIV':
            if self.reg[reg_b]:
                self.reg[reg_a] /= self.reg[reg_b]

            else:
                self.handle_HLT()
                raise Exception("Cannot divide by 0")

        elif op == 'INC':
            self.reg[reg_a] += 1
            self.reg[reg_a] &= 0xFF

        elif op == 'MOD':
            if self.reg[reg_b]: 
                self.reg[reg_a] %= self.reg[reg_b]

            else:
                self.handle_HLT()
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

            self.branchtable[ir](operand_a, operand_b)

            jumps = [CALL, RET, JEQ, JGE, JGT, JLE, JLT, JMP, JNE, IRET]


            # if ir != CALL and ir != RET:
            #     self.pc += add_to_pc
            # print(add_to_pc)
            if ir not in jumps:
                self.pc += add_to_pc



