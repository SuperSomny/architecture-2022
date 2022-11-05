#指令抽象类
#   一条指令的实现应当继承这个类，并重写四个方法
class Instruction:
    #指令译码阶段
    def instrDecode(self):
        pass

    #运算阶段
    def execute(self):
        pass

    #访问存储器阶段
    def memAccess(self):
        pass

    #写回寄存器阶段
    def writeBack(self):
        pass

    def __init__(self, hw):
        self.hw = hw    #指令关联的硬件结构
        self.stages = [
                self.instrDecode,
                self.execute,
                self.memAccess,
                self.writeBack
        ]               #每条指令包含四个阶段
