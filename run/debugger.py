from hardware.hardware import Hardware

class Debugger:
    def __init__(self, hw):
        self.hw = hw

    #打印通用寄存器
    #效果：
    #   打印当前所有通用寄存器的值
    def dumpGenReg(self):
        for i in range(self.hw.genRegCnt):
            data = self.hw.genReg[i].read()
            print('{:2}: {:08x}'.format(i, data))

    #打印流水线寄存器
    #效果：
    #   打印当前所有流水线寄存器的值
    def dumpPplReg(self):
        for name in self.hw.pplReg.keys():
            data = self.hw.pplReg[name].read()
            print('{:5}: {:08x}'.format(name, data))

    #打印指令存储器
    #输入：
    #   addr为地址
    #效果：
    #   打印当前指令存储器地址addr所在的一个字
    def dumpInstrMem(self, addr):
        data = self.hw.instrMem.read(addr)
        print('{}: {:08x}'.format(addr, data))

    #打印数据存储器
    #输入：
    #   addr为地址
    #效果：
    #   打印当前数据存储器地址addr所在的一个字
    def dumpDataMem(self, addr):
        data = self.hw.dataMem.read(addr)
        print('{}: {:08x}'.format(addr, data))
