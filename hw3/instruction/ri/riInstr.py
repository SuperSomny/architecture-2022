from instruction.instruction import Instruction

#RI类指令
class RegImmInstr(Instruction):
    def instrDecode(self):
        super().instrDecode()

        instr = self.hw.pplReg[1][0].read()
        mask = (1 << 5) - 1

        rs = (instr >> 21) & mask
        rsData = self.hw.genReg[rs].read()
        rt = (instr >> 16) & mask

        self.hw.pplReg[2][0].write(rsData)
        self.hw.pplReg[2][2].write(rt)

    def memAccess(self):
        super().memAccess()

        res = self.hw.pplReg[3][0].read()
        rt = self.hw.pplReg[3][1].read()

        self.hw.genReg[rt].write(res)

#进行零扩展的RI类指令
class ZeroExtRegImmInstr(RegImmInstr):
    def instrDecode(self):
        super().instrDecode()

        instr = self.hw.pplReg[1][0].read()
        mask = (1 << 16) - 1

        imm = instr & mask
        self.hw.pplReg[2][1].write(imm)

#进行符号扩展的RI类指令
class SignExtRegImmInstr(RegImmInstr):
    #符号扩展
    #输入：
    #   imm为16bit数据
    #输出：
    #   imm的32bit符号扩展
    def signedExtend(imm):
        mask = (1 << 16) - 1 << 16
        if (imm >> 15) & 1:
            return imm | mask
        else:
            return imm

    def instrDecode(self):
        super().instrDecode()

        instr = self.hw.pplReg[1][0].read()
        mask = (1 << 16) - 1

        imm = instr & mask
        imm = SignExtRegImmInstr.signedExtend(imm)
        self.hw.pplReg[2][1].write(imm)
