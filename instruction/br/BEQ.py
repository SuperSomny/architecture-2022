from instruction.instruction import Instruction
from hardware.hardware import Hardware
class Beq(Instruction):
    def __init__(self, hw):
        super().__init__(hw)

    def instrDecode(self):
        super().instrDecode()
        instr = self.hw.pplReg[1][0].read()
        mask1 = (1 << 5) - 1
        rs = (instr >> 21) & mask1  # 这里的rs为base
        rsData = self.hw.genReg[rs].read()
        rt = (instr >> 16) & mask1
        rtData = self.hw.genReg[rt].read()
        mask2 = (1 << 16) - 1
        offset = instr & mask2

        self.hw.pplReg[2][0].write(rsData)  # A <= Reg[base]
        self.hw.pplReg[2][1].write(rtData)  # B <= rt
        self.hw.pplReg[2][2].write(offset)  # C <= offset
    def execute(self):
        super().execute()
        pc=self.hw.pc.read()
        if self.hw.pplReg[2][0].read==self.hw.pplReg[2][1].read:
            jpc=pc+4+self.hw.pplReg[2][2].read*4#offest后补两个0
        else:
            jpc=pc+4
        self.hw.pplReg[3][0].write(jpc)

    def memAccess(self):
        super().memAccess()

        Hardware.pc.write(self.hw.pplReg[3][0].read())

    def writeBack(self):
        super().writeBack()

