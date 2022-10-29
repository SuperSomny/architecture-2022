from instruction.instruction import Instruction
from hardware.hardware import Hardware

class J(Instruction):
    def instrDecode(self):
        super().instrDecode()

        instr = self.hw.pplReg[1][0].read()
        nextPC = str(bin(Hardware.pc.read() + 4))[2:6] # PC+4，再取高4位
        instr_index = str(bin(instr))[8:34] # instruction转换为字符串类型时，有‘0b’需要去除，然后取出其中的[25:0]

        self.hw.pplReg[2][0].write(nextPC)
        self.hw.pplReg[2][1].write(instr_index)

    def execute(self):
        super().execute()

        jPC = int(self.hw.pplReg[2][0].read + self.hw.pplReg[2][1].read + 2*'0') # PC <-- PC[31:28] || instr_index || 00. (||为拼接操作)

        self.hw.pplReg[3][0].write(jPC)

    def memAccess(self):
        super().memAccess()

        Hardware.pc.write(self.hw.pplReg[3][0].read())

    def writeBack(self):
        super().writeBack()