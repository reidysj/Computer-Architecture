CALL = 0b01010000
HLT = 0b00000001 
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
LDI = 0b10000010
POP = 0b01000110
NOP = 0b00000000
PRA = 0b01001000
PRN = 0b01000111
PUSH = 0b01000101
RET = 0b00010001
ST = 0b10000100


def handle_CALL(self, operand_a, operand_b):
    # Get the current address
    addr = self.reg[operand_a]
    # Advance the return address
    rtn_addr = self.pc + 2
    # Subtract one ('after' the instruction) from SP
    self.reg[7] -= 1  
    sp = self.reg[7]
    # Push the address of the instruction after CALL to the stack
    self.ram[sp] = rtn_addr 
    # Set the PC to the address in the given register
    self.pc = addr

def handle_HLT(self, *args):
    # Stop all processes
    self.is_running = False

def handle_LDI(self, operand_a, operand_b):
    # Set the value of the register at op_a to op_b
    self.reg[operand_a] = operand_b

def handle_PRN(self, operand_a, operand_b):
    # print the value of the register at op_a
    print(self.reg[operand_a])

def handle_PUSH(self, operand, *args):
    val = self.reg[operand]
    # decrement the SP
    self.reg[7] -= 1
    # Put the value into the stack at the address indicated by the SP
    self.ram[self.reg[7]] = val

def handle_POP(self, operand, *args):
    # Put the value at the top of the stack into the given register
    val = self.ram[self.reg[7]]
    self.reg[operand] = val
    # Increment the stack point
    self.reg[7] += 1

def handle_RET(self, *args):
    # Subroutine complete, return
    rtn_addr = self.ram[self.reg[7]]
    # Increment by one because the value has been handled
    self.reg[7] += 1
    # value from the top of the stack gets stored to PC
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
    # Check if the flag has a 1 in the E (last position)
    # Hash with & b/c we only care about the last digit
    # If the last digit is true, this will return true
    if self.FL & 0b00000001:
        self.pc = self.reg[operand]
    else:
        self.pc += 2

def handle_JGE(self, operand, *args):
    # If the last or second last position is true, this will return true
    if self.FL & 0b00000011:
        self.pc = self.reg[operand]
    # PC incrementer in run is set to ignore these calls in case they are true
    # if they're false, the PC needs to be incremented.
    else:
        self.pc += 2

def handle_JGT(self, operand, *args):
    # if the second last position is true, this will return true
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
    # Move the pc forward, regardless
    # This call is ignored by the run method.
    self.pc = self.reg[operand]

def handle_JNE(self, operand, *args):
    # Only jump if E = 0
    if not self.FL & 0b00000001:
        self.pc = self.reg[operand]
    else: 
        self.pc += 2

def handle_LD(self, operand_a, operand_b):
    self.reg[operand_a] = self.ram[self.reg[operand_b]]

def handle_NOP(self, *args):
    pass

def handle_PRA(self, operand, *args):
    # get the value at the indicated reg
    letter = self.reg[operand]
    # convert it to a letter and print
    print(chr(letter))

def handle_ST(self, operand_a, operand_b):
    # write to memory; reg_b goes to address in reg_a
    # self.ram_write(address, value)
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