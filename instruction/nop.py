from instruction.instruction import Instruction

#空指令
class Nop(Instruction):
    #什么都不做
    def instrDecode(self):
        super().instrDecode()

    def execute(self):
        super().execute()

    def memAccess(self):
        super().memAccess()

    def writeBack(self):
        super().writeBack()
