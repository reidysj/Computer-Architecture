# Variables for branch table below
ADD = 0b10100000
AND = 0b10101000
CMP = 0b10100111
DEC = 0b01100110
DIV = 0b10100011
INC = 0b01100101
MOD = 0b10100100
MUL = 0b10100010
NOT = 0b01101001
OR = 0b10101010
SHL = 0b10101100
SHR = 0b10101101
SUB = 0b10100001
XOR = 0b10101011

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

def handle_MUL(self, operand_a, operand_b):
    self.alu('MUL', operand_a, operand_b)

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

# Imported to CPU class as a branch table

alu_branch = {
    ADD : handle_ADD,
    AND: handle_AND,
    CMP : handle_CMP,
    DEC : handle_DEC,
    DIV : handle_DIV,
    INC : handle_INC,
    MOD: handle_MOD,
    MUL : handle_MUL,
    NOT: handle_NOT,
    OR: handle_OR,
    SHL: handle_SHL,
    SHR: handle_SHR,
    SUB: handle_SUB,
    XOR: handle_XOR,
}