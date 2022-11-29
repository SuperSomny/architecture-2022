from architecture import *

#执行一个周期
def run(arch):
    arch1 = Architecture()

    for i in range(INSTR_MEM_SIZE):
        arch1.mem[INSTR_MEM_OFF + i] = arch.mem[INSTR_MEM_OFF + i]

    arch1.clk = arch.clk + 1

    arch1.reg[PC_REG_OFF] = runPC(arch)
    '''
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
    '''

    return arch1

def runPC(arch):
    pc = Register()

    if issue(arch):
        pc.val = arch.reg[PC_REG_OFF].val + 1

        instr = fetch(arch)
        if instr.op == 'jump':
            pc.src = INT_RS_OFF
        else:
            pc.src = arch.reg[PC_REG_OFF].src
    elif arch.reg[PC_REG_OFF].src and not arch.fu[INT_FU_OFF].clk:
        pc.val = arch.fu[INT_FU_OFF].res
        pc.src = 0
    else:
        pc.val = arch.reg[PC_REG_OFF].val
        pc.src = arch.reg[PC_REG_OFF].src

    return pc

def runIntReg(arch, i):
    reg = Register()

    fuOff = writeReg(arch, INT_REG_OFF + i)
    if fuOff:
        reg.val = arch.fu[fuOff].res
    else:
        reg.val = arch.reg[INT_REG_OFF + i].val

    rsOff = issue(arch)
    if rsOff:
        instr = fetch(arch)

        if instr.op == 'addi':
            #TODO

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

def issue(arch):
    if not arch.reg[PC_REG_OFF].src:
        instr = fetch(arch)
        if instr:
            rsMap = {
                    'addi': (INT_RS_OFF, INT_RS_SIZE),
                    'jump': (INT_RS_OFF, INT_RS_SIZE),
                    'fadd': (ADD_RS_OFF, ADD_RS_SIZE),
                    'fmul': (MUL_RS_OFF, MUL_RS_SIZE),
                    'load': (MEM_RS_OFF, MEM_RS_SIZE),
                    'store': (MEM_RS_OFF, MEM_RS_SIZE)
                    }
            offset, size = rsMap[instr.op]
            return first(arch, offset, size):
    return 0

def fetch(arch):
    return arch.mem[INSTR_MEM_OFF + arch.reg[PC_REG_OFF].val]

def first(arch, offset, size):
    for i in range(size):
        if not arch.rs[offset + i].busy:
            return offset + i
    return 0

def writeReg(arch, i):
    src = arch.reg[i].src
    if src == INT_RS_OFF:
        return INT_FU_OFF
    elif src >= ADD_RS_OFF and src < ADD_RS_OFF + ADD_RS_SIZE:
        return ADD_FU_OFF
    elif src >= MUL_RS_OFF and src < MUL_RS_OFF + MUL_RS_SIZE:
        return MUL_FU_OFF
    elif src >= MEM_RS_OFF and src < MEM_RS_OFF + MEM_RS_SIZE:
        return MEM_FU_OFF
    else:
        return 0
