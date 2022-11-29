from architecture import *
from debug import dump, getInstr, program
from run import run

arch = Architecture()
prog = [
        getInstr('load', 0, 1, 0, 0),
        getInstr('fmul', 4, 0, 2, 0),
        getInstr('store', 0, 4, 1, 0),
        getInstr('addi', 1, 1, 0, -8),
        getInstr('jump', 0, 0, 0, -4)
        ]
arch = program(arch, prog)
print('')
for i in range(2):
    arch = run(arch)
dump(arch)
