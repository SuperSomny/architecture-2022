from instruction.instruction import Instruction


# 存取类指令
class Ldst(Instruction):
    def __init__(self, hw):
        super().__init__(hw)

    def instrDecode(self):
        super().instrDecode()
        instr = self.hw.pplReg[1][0].read()
        mask1 = (1 << 5) - 1
        base = (instr >> 21) & mask1  # 这里的rs为base
        baseData = self.hw.genReg[base].read()
        rt = (instr >> 16) & mask1
        mask2 = (1 << 16) - 1
        offset = instr & mask2

        self.hw.pplReg[2][0].write(baseData)  # A <= Reg[base]
        self.hw.pplReg[2][1].write(rt)  # B <= rt
        self.hw.pplReg[2][2].write(offset)  # C <= offset

    def execute(self):
        super().execute()
        rt = self.hw.pplReg[2][1].read()
        addr = self.hw.pplReg[2][0].read() + self.hw.pplReg[2][2].read()  # 计算地址 = baseData+offset
        self.hw.pplReg[3][0].write(addr)
        self.hw.pplReg[3][1].write(rt)
