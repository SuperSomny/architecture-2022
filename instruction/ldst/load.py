from instruction.ldst.ldst import Ldst


class Load(Ldst):
    def __init__(self, hw):
        super().__init__(hw)

    def memAccess(self):
        super().memAccess()
        addr = self.hw.pplReg[3][0].read()
        memData = self.hw.dataMem.read(addr)
        rt = self.hw.pplReg[3][1].read()
        self.hw.pplReg[4][0].write(memData)  # 取内存数据
        self.hw.pplReg[4][1].write(rt)

    def writeBack(self):
        super().writeBack()
        rt = self.hw.pplReg[4][1].read()
        memData = self.hw.pplReg[4][0].read()
        self.hw.genReg[rt].write(memData)  # 数据写回目标寄存器
