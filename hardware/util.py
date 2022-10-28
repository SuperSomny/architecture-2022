#寄存器
#   约定：寄存器为1word=32bit
class Register:
    def __init__(self):
        self.data = 0
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

#存储器
#   约定：每个存储单元为1byte=8bit，但存取时需要按字对齐
class Memory:
    def __init__(self, size):
        self.size = size >> 2
        self.dict = {}
        self.addr = None
        self.buff = None

    #读数据
    #输入：
    #   addr为读取的地址
    #输出：
    #   地址addr所在的一个字，若addr不是4的整数倍，将向下取整
    def read(self, addr):
        addr = addr >> 2

        #检查地址是否越界
        if addr < 0 or addr >= self.size:
            raise Exception("memory address out of bounds")

        if addr in self.dict.keys():
            #该地址被访问过
            return self.dict[addr]
        else:
            #该地址未被访问过
            self.dict[addr] = 0
            return 0

    #写数据
    #输入：
    #   addr为写入的地址
    #   data为写入的数据
    #效果：
    #   将data写入地址addr所在的一个字的缓冲区
    #
    #一个周期内只能写入一个数据
    def write(self, addr, data):
        addr = addr >> 2

        #检查地址是否越界
        if addr < 0 or addr >= self.size:
            raise Exception("memory address out of bounds")

        self.addr = addr
        self.buff = data

    #同步
    #效果：
    #   将缓冲区中的数据写入存储器
    def sync(self):
        if self.addr is not None:
            self.dict[self.addr] = self.buff
            self.addr = None
            self.buff = None
