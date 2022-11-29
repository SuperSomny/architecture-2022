from architecture import *

#执行一个周期
def run(arch):
    arch1 = Architecture()
    arch1.clk = arch.clk + 1

    arch1.reg[PC_REG_OFF] = runPC(arch, i)
    for i in range(INT_REG_SIZE):
        arch1.reg[INT_REG_OFF + i] = runIntReg(arch, i)
    for i in range(FP_REG_SIZE):
        arch1.reg[FP_REG_OFF + i] = runFpReg(arch, i)

    for i in range(DATA_MEM_SIZE):
        arch1.mem[DATA_MEM_OFF + i] = runMem(arch, i)
    arch1.fu[INT_FU_OFF] = runIntFU(arch)
    arch1.fu[ADD_FU_OFF] = runAddFU(arch)
    arch1.fu[MUL_FU_OFF] = runMulFU(arch)
    arch1.fu[MEM_FU_OFF] = runMemFU(arch)

    arch1.rs[INT_RS_OFF] = runIntRS(arch)
    for i in range(ADD_RS_SIZE):
        arch1.rs[ADD_RS_OFF + i] = runAddRS(arch, i)
    for i in range(MUL_RS_SIZE):
        arch1.rs[MUL_RS_OFF + i] = runMulRS(arch, i)
    for i in range(MEM_RS_SIZE):
        arch1.rs[MEM_RS_OFF + i] = runMemRS(arch, i)
    for i in range(BUF_REG_SIZE):
        arch1.reg[BUF_REG_OFF + i] = runBufReg(arch, i)

    arch1.bus = runBus(arch)

    return arch1

def runPC(arch):
    pass

def runIntReg(arch, i):
    pass

def runFpReg(arch, i):
    pass

def runMem(arch, i):
    pass

def runIntFU(arch):
    pass

def runAddFU(arch):
    pass

def runMulFU(arch):
    pass

def runMemFU(arch):
    pass

def runIntRS(arch):
    pass

def runAddRS(arch, i):
    pass

def runMulRS(arch, i):
    pass

def runMemRS(arch, i):
    pass

def runBufReg(arch, i):
    pass

def runBus(arch, i):
    pass
