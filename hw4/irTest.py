from ir.ir import *
from ir.trans import ir2code

'''
beq r1, r2, out     (1)
loop:
load r10, 0(r1)     (2)
add r14, r10, r12   (3)
store r14, 0(r1)    (4)
addi r1, r1, 1      (5)
bne r1, r2, loop    (6)
out:
'''

prog = Program()
loop = Loop(1, 2)

loop.instrList.append(Beq(1, 2))
loop.instrList.append(Load(10, 0, 1))
loop.instrList.append(Add(14, 10, 12))
loop.instrList.append(Store(14, 0, 1))
loop.instrList.append(Addi(1, 1, 1))
loop.instrList.append(Bne(1, 2))

prog.instrList.append(loop)

fileName = 'program/irTest.txt'
ir2code(prog, fileName)
