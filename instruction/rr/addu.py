from instruction.instruction import Instruction
#from hardware.hardware import Hardware

#RR类指令
class Addu(Instruction):
    def __init__(self, hw):
        super().__init__(hw)

    def instrDecode(self):
        super().instrDecode()
        instr = self.hw.pplReg[1][0].read()
        mask = (1 << 5) - 1
        rs = (instr >> 21) & mask
        rsData = self.hw.genReg[rs].read()
        rt = (instr >> 16) & mask
        rtData = self.hw.genReg[rs].read()
        rd = (instr >> 11) & mask

        self.hw.pplReg[2][0].write(rsData)
        self.hw.pplReg[2][1].write(rtData)
        self.hw.pplReg[2][3].write(rd)

    def execute(self):
        super().execute()

        op1 = self.hw.pplReg[2][0].read()
        op2 = self.hw.pplReg[2][1].read()
        rd  = self.hw.pplReg[2][3].read()

        mask = (1 << 32) - 1
        res = (op1 + op2) & mask

        self.hw.pplReg[3][0].write(res)
        self.hw.pplReg[3][1].write(rd)

    def memAccess(self):
        super().memAccess()

        addr = self.hw.pplReg[3][0].read()
        memData = self.hw.dataMem.read(addr)
        rd = self.hw.pplReg[3][1].read()

        self.hw.pplReg[4][0].write(memData)  # 取内存数据
        self.hw.pplReg[4][1].write(rd)

    def writeBack(self):
        super().writeBack()
        rd = self.hw.pplReg[4][1].read()
        memData = self.hw.pplReg[4][0].read()
        self.hw.genReg[rd].write(memData)  # 数据写回目标寄存器