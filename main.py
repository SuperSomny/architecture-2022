from hardware.hardware import Hardware
from run.controller import Controller
from run.debugger import Debugger

hw = Hardware()
ctrl = Controller(hw)
dbg = Debugger(hw)
prog = 'prog/addiuTest.txt'

dbg.loadProgram(prog)

print('running...')
ctrl.run()
ctrl.run()
ctrl.run()
dbg.dumpGenReg()

print('running...')
ctrl.run()
ctrl.run()
ctrl.run()
dbg.dumpGenReg()

print('running...')
ctrl.run()
dbg.dumpGenReg()
