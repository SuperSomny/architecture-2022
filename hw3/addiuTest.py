from hardware.hardware import Hardware
from execute.controller import Controller
from execute.debugger import Debugger

hw = Hardware()
ctrl = Controller(hw)
dbg = Debugger(hw)
prog = 'program/addiuTest.txt'

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
