from instruction.ldst.ldst import Ldst


class Store(Ldst):
    def __init__(self, hw):
        super().__init__(hw)

    def memAccess(self):
        super().memAccess()
        addr = self.hw.pplReg[3][0].read()
        rt = self.hw.pplReg[3][1].read()
        regData = self.hw.genReg[rt].read()    # 取寄存器数据
        self.hw.dataMem.write(addr, regData)   # 写入存储器


