from run import Runner
from util import Instruction

program = []
program.append(Instruction('load', 0, True, 6, False, 0, True, 2))
program.append(Instruction('load', 0, True, 2, False, 0, True, 3))
program.append(Instruction('mult', 1, True, 0, True, 2, True, 4))
program.append(Instruction('sub', 2, True, 8, True, 6, True, 2))
program.append(Instruction('div', 3, True, 10, True, 0, True, 6))
program.append(Instruction('add', 2, True, 6, True, 8, True, 2))

runner = Runner(program)
runner.run(1)
runner.dump()
