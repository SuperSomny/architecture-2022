from hardware.hardware import Hardware
from run.controller import Controller
from run.debugger import Debugger

hw = Hardware()
ctrl = Controller(hw)
dbg = Debugger(hw)
prog = 'prog/test.txt'

dbg.loadProgram(prog)
dbg.dumpPC()
dbg.dumpInstrMem(0)
dbg.dumpInstrMem(4)
dbg.dumpInstrMem(8)

print('running...')
ctrl.run()
ctrl.run()
ctrl.run()

dbg.dumpPC()
dbg.dumpGenReg()
