from architecture import *

def dump(arch):
    dumpPC(arch)
    print('')
    dumpIntReg(arch)
    print('')
    dumpFpReg(arch)
    print('')
    dumpIntUnit(arch)
    print('')
    dumpAddUnit(arch)
    print('')
    dumpMulUnit(arch)
    print('')
    dumpMemUnit(arch)

def valid(check, data):
    if check:
        return data
    else:
        return ''

def dumpPC(arch):
    print('pc:\n{:<6}{:<6}'.format('value', arch.reg[PC_REG_OFF].val), end = '')
    src = arch.reg[PC_REG_OFF].src
    src = valid(src, src)
    print('\n{:<6}{:<6}'.format('Qi', src), end = '')
    print('')
    return

def dumpReg(arch, offset, size):
    print('{:<6}'.format(''), end = '')
    for i in range(size):
        print('{:<4}'.format(i), end = '')
    print('\n{:<6}'.format('value'), end = '')
    for i in range(size):
        print('{:<4}'.format(arch.reg[offset + i].val), end = '')
    print('\n{:<6}'.format('Qi'), end = '')
    for i in range(size):
        src = arch.reg[offset + i].src
        src = valid(src, src)
        print('{:<4}'.format(src), end = '')
    print('')

def dumpIntReg(arch):
    print('integer registers:')
    dumpReg(arch, INT_REG_OFF, INT_REG_SIZE)
    return

def dumpFpReg(arch):
    print('floating point registers:')
    dumpReg(arch, FP_REG_OFF, FP_REG_SIZE)
    return

def dumpRS(arch, offset):
    busy = arch.rs[offset].busy
    op = valid(busy, arch.rs[offset].op)
    val1 = valid(busy, arch.rs[offset].val1)
    val2 = valid(busy, arch.rs[offset].val2)
    src1 = valid(busy, arch.rs[offset].src1)
    src2 = valid(busy, arch.rs[offset].src2)
    addr = valid(busy, arch.rs[offset].addr)
    src1 = valid(src1, src1)
    src2 = valid(src2, src2)
    addr = valid(addr, addr)
    print('{:<6}{:<6}{:<6}{:<6}{:<6}{:<6}{:<6}'.format(
        busy,
        op,
        val1,
        val2,
        src1,
        src2,
        addr))
    return

def dumpFU(arch, fuOff, rsOff, rsSize):
    print('{:<6}{:<6}'.format('clk', 'res'))
    print('{:<6}{:<6}'.format(arch.fu[fuOff].clk, arch.fu[fuOff].res))
    print('{:<6}{:<6}{:<6}{:<6}{:<6}{:<6}{:<6}'.format(
        'busy',
        'op',
        'Vj',
        'Vk',
        'Qj',
        'Qk',
        'A'))
    for i in range(rsSize):
        dumpRS(arch, rsOff + i)
    return

def dumpIntUnit(arch):
    print('integer unit:')
    dumpFU(arch, INT_FU_OFF, INT_RS_OFF, INT_RS_SIZE)
    return

def dumpAddUnit(arch):
    print('add unit:')
    dumpFU(arch, ADD_FU_OFF, ADD_RS_OFF, ADD_RS_SIZE)
    return

def dumpMulUnit(arch):
    print('multiply unit:')
    dumpFU(arch, MUL_FU_OFF, MUL_RS_OFF, MUL_RS_SIZE)
    return

def dumpMemUnit(arch):
    print('memory access unit:')
    dumpFU(arch, MEM_FU_OFF, MEM_RS_OFF, MEM_RS_SIZE)
    print('memory access buffer:')
    print('{:<6}'.format('A'), end = '')
    for i in range(BUF_REG_SIZE):
        src = arch.reg[BUF_REG_OFF + i].src
        addr = valid(src, arch.reg[BUF_REG_OFF + i].val)
        print('{:<6}'.format(addr), end = '')
    print('\n{:<6}'.format('Qi'), end = '')
    for i in range(BUF_REG_SIZE):
        src = arch.reg[BUF_REG_OFF + i].src
        src = valid(src, src)
        print('{:<6}'.format(src), end = '')
    print('')
    return
