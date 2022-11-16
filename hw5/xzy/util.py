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
    def __init__(self, op, fu, destValid, dest, src1Valid, src1, src2Valid, src2):
        self.op = op                #操作
        self.fu = fu                #所需的功能部件
        self.destValid = destValid  #目的寄存器是否有效
        self.dest = dest            #目的寄存器号
        self.src1Valid = src1Valid  #源寄存器1是否有效
        self.src1 = src1            #源寄存器号1
        self.src2Valid = src2Valid  #源寄存器2是否有效
        self.src2 = src2            #源寄存器号2
