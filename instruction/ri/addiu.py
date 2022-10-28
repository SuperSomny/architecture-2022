from instruction.ri.riInstr import SignExtRegImmInstr

#无符号加立即数
class Addiu(SignExtRegImmInstr):
    def execute(self):
        super().execute()

        op1 = self.hw.pplReg[2][0].read()
        op2 = self.hw.pplReg[2][1].read()
        rt = self.hw.pplReg[2][2].read()

        mask = (1 << 32) - 1
        res = (op1 + op2) & mask

        self.hw.pplReg[3][0].write(res)
        self.hw.pplReg[3][1].write(rt)
