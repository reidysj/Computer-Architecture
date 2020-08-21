HLT = 0b00000001 
LDI = 0b10000010
PRN = 0b01000111
PUSH = 0b01000101
POP = 0b01000110
CALL = 0b01010000
RET = 0b00010001
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
NOP = 0b00000000
PRA = 0b01001000
ST = 0b10000100



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

main_branch = {
    HLT : handle_HLT,
    LDI : handle_LDI,
    PRN : handle_PRN,
    PUSH : handle_PUSH,
    POP : handle_POP,
    CALL : handle_CALL,
    RET : handle_RET,
    INT : handle_INT,
    IRET : handle_IRET,
    JEQ: handle_JEQ,
    JGE: handle_JGE,
    JGT: handle_JGT,
    JLE: handle_JLE,
    JLT: handle_JLT,
    JMP: handle_JMP,
    JNE: handle_JNE,
    LD: handle_LD,
    NOP: handle_NOP,
    PRA: handle_PRA,
    ST: handle_ST,
}