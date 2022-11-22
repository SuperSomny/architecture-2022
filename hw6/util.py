#寄存器
class Register:
    def __init__(self, initValue):
        self.data = initValue
        self.buff = None

    #读数据
    #输出：
    #   寄存器中的数据
    def read(self):
        return self.data

    #写数据
    #输入：
    #   data为写入的数据
    #效果：
    #   将data写入缓冲区
    def write(self, data):
        self.buff = data

    #同步
    #效果：
    #   将缓冲区中的数据写入寄存器
    def sync(self):
        if self.buff is not None:
            self.data = self.buff
            self.buff = None

#指令
class Instruction:
    #初始化
    def __init__(self, fu, dest, src1, src2, imm):
        self.fu = fu                #所需的功能部件
        self.dest = dest            #目的寄存器号
        self.src1 = src1            #源寄存器号1
        self.src2 = src2            #源寄存器号2
        self.imm = imm              #立即数

    #是否访存指令
    def isMem(fu):
        return fu == 0 or fu == 1

    #是否Load指令
    def isLoad(fu):
        return fu == 0

    #是否Store指令
    def isStore(fu):
        return fu == 1
