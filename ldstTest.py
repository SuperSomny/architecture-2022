from hardware.hardware import Hardware
from execute.controller import Controller
from execute.debugger import Debugger

hw = Hardware()
ctrl = Controller(hw)
dbg = Debugger(hw)
prog = 'prog/ldstTest.txt'
# Addiu r1,r1,3
# Store r1, 10(r0)
# Load r2, 10(r0)

dbg.loadProgram(prog)

ctrl.run()
ctrl.run()
ctrl.run()
dbg.dumpGenReg()
# dbg.dumpPplReg()
dbg.dumpDataMem(10)
