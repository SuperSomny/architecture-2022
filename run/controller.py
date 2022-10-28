from hardware.hardware import Hardware
from instruction.nop import Nop
from instruction.ri.addiu import Addiu

class Controller:
    opMap = {
            0x09: Addiu,
    }
    funcMap = {
            0x00: Nop,
    }

    def __init__(self, hw):
        self.hw = hw

    #获取指令对象
    #输入：
    #   instr为指令编码
    #输出：
    #   instr表示的指令类型的对象
    def getInstrObj(self, instr):
        mask = (1 << 6) - 1
        op = (instr >> 26) & mask
        func = instr & mask

        if op == 0x00:
            if func in Controller.funcMap.keys():
                return Controller.funcMap[func](self.hw)
            else:
                raise Exception('instruction does not exist')
        else:
            if op in Controller.opMap.keys():
                return Controller.opMap[op](self.hw)
            else:
                raise Exception('instruction does not exist')

    #取指令阶段
    #效果：
    #   将即将执行的指令编码写入instr寄存器，pc+4
    def instrFetch(self):
        #从指令存储器中取指令
        pc = self.hw.pc.read()
        instr = self.hw.instrMem.read(pc)
        self.hw.pplReg[1][0].write(instr)

        #pc+4
        self.hw.pc.write(pc + 4)

        return instr

    #无流水线的执行
    #效果：
    #   完整执行一条指令
    def run(self):
        #取指令，获取指令对象
        instr = self.instrFetch()
        instrObj = self.getInstrObj(instr)
        self.hw.globalSync()

        for i in range(len(instrObj.stages)):
            instrObj.stages[i]()
            self.hw.globalSync()
