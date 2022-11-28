INT_REG_SIZE = 32           #整数寄存器数
FP_REG_SIZE = 32            #浮点寄存器数
PC_REG_SIZE = 1
BUF_REG_SIZE = 6
REG_SIZE = INT_REG_SIZE + FP_REG_SIZE + PC_REG_SIZE + BUF_REG_SIZE
REG_OFF = 0
INT_REG_OFF = REG_OFF
FP_REG_OFF = INT_REG_OFF + INT_REG_SIZE
PC_REG_OFF = FP_REG_OFF + FP_REG_SIZE
BUF_REG_OFF = PC_REG_OFF + PC_REG_SIZE

INSTR_MEM_SIZE = 1 << 11    #指令存储器大小
DATA_MEM_SIZE = 1 << 11     #数据存储器大小
MEM_SIZE = INSTR_MEM_SIZE + DATA_MEM_SIZE
MEM_OFF = 0
INSTR_MEM_OFF = MEM_OFF
DATA_MEM_OFF = INSTR_MEM_OFF + INSTR_MEM_SIZE

FU_SIZE = 4                 #功能部件数
FU_OFF = 0
INT_FU_OFF = FU_OFF
ADD_FU_OFF = INT_FU_OFF + 1
MUL_FU_OFF = ADD_FU_OFF + 1
MEM_FU_OFF = MUL_FU_OFF + 1

INT_RS_SIZE = 1
ADD_RS_SIZE = 3             #浮点加法部件保留站数量
MUL_RS_SIZE = 2             #浮点乘法部件保留站数量
MEM_RS_SIZE = BUF_REG_SIZE
RS_SIZE = INT_RS_SIZE + ADD_RS_SIZE + MUL_RS_SIZE + MEM_RS_SIZE
RS_OFF = 1
INT_RS_OFF = RS_OFF
ADD_RS_OFF = INT_RS_OFF + INT_RS_SIZE
MUL_RS_OFF = ADD_RS_OFF + ADD_RS_SIZE
MEM_RS_OFF = MUL_RS_OFF + MUL_RS_SIZE

#寄存器
class Register:
    def __init__(self):
        self.val = 0
        self.src = 0
        return

    def copy(self):
        reg = Register()
        reg.val = self.val
        reg.src = self.src
        return reg

#功能部件
class FuncUnit:
    def __init__(self):
        self.clk = 0
        self.res = 0
        return

    def copy(self):
        fu = FuncUnit()
        fu.clk = self.clk
        fu.res = self.res
        return fu

#保留站
class ReservStation:
    def __init__(self):
        self.busy = 0
        self.op = ''
        self.val1 = 0
        self.src1 = 0
        self.val2 = 0
        self.src2 = 0
        self.addr = 0
        return

    def copy(self):
        rs = ReservStation()
        rs.busy = self.busy
        rs.op = self.op
        rs.val1 = self.val1
        rs.src1 = self.src1
        rs.val2 = self.val2
        rs.src2 = self.src2
        rs.addr = self.addr
        return rs

#指令
class Instruction:
    def __init__(self):
        self.op = ''
        self.dest = 0
        self.op1 = 0
        self.op2 = 0
        self.imm = 0
        return

    def copy(self):
        instr = Instruction()
        instr.op = self.op
        instr.dest = self.dest
        instr.op1 = self.op1
        instr.op2 = self.op2
        instr.imm = self.imm
        return instr

#架构
class Architecture:
    def __init__(self):
        self.reg = [Register() for i in range(REG_OFF + REG_SIZE)]
        self.mem = [0 for i in range(MEM_OFF + MEM_SIZE)]
        self.fu = [FuncUnit() for i in range(FU_OFF + FU_SIZE)]
        self.rs = [ReservStation() for i in range(RS_OFF + RS_SIZE)]
        self.clk = 0                                                #时钟
        self.bus = 0                                                #总线
        return

    def copy(self):
        arch = Architecture()
        for i in range(REG_SIZE):
            arch.reg[i] = self.reg[i].copy()
        for i in range(MEM_SIZE):
            arch.mem[i] = self.mem[i]
        for i in range(FU_SIZE):
            arch.fu[i] = self.fu[i].copy()
        for i in range(RS_SIZE):
            arch.rs[i] = self.rs[i].copy()
        arch.clk = self.clk
        arch.bus = self.bus
        return arch
