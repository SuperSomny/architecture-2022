from architecture import *

#执行一个周期
def run(arch):
    arch1 = arch.copy()
    arch1.clk += 1
    arch1 = issue(arch1)
    arch1 = execute1(arch1)
    arch1 = execute2(arch1)
    arch1 = write(arch1)
    return arch1

#发出指令
def issue(arch):
    arch1 = arch.copy()
    if arch1.reg[PC_REG_OFF].src:
        return arch1
    pc = arch1.reg[PC_REG_OFF].val
    instr = arch1.mem[INSTR_MEM_OFF + pc]
    if not instr:
        return arch1
    elif isOp(instr.op):
        return issueOp(arch1, instr)
    elif isMem(instr.op):
        return issueMem(arch1, instr)
    return arch1

#执行阶段1
def execute1(arch):
    #TODO

#执行阶段2
def execute2(arch):
    #TODO

#写回结果
def write(arch):
    #TODO

def isOp(op):
    return op == 'j' or op == 'addi' or op == 'fadd' or op == 'fmul'

def isMem(op):
    return op == 'ld' or op == 'st'
