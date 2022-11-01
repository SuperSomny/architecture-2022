from hardware.hardware import Hardware

class Debugger:
    def __init__(self, hw):
        self.hw = hw

    #打印程序计数器
    #效果：
    #   打印当前pc寄存器的值
    def dumpPC(self):
        pc = self.hw.pc.read()
        print('pc: {:08x}'.format(pc))

    #打印通用寄存器
    #效果：
    #   打印当前所有通用寄存器的值
    def dumpGenReg(self):
        for i in range(self.hw.genRegCnt):
            data = self.hw.genReg[i].read()
            print('GR{:02}: {:08x}'.format(i, data))

    #打印流水线寄存器
    #效果：
    #   打印当前所有流水线寄存器的值
    def dumpPplReg(self):
        for i in range(self.hw.stageCnt):
            print('stage{}:'.format(i))

            for j in range(self.hw.pplRegCnt):
                data = self.hw.pplReg[i][j].read()
                print('PR{}: {:08x}'.format(j, data))

    #打印指令存储器
    #输入：
    #   addr为地址
    #效果：
    #   打印当前指令存储器地址addr所在的一个字
    def dumpInstrMem(self, addr):
        data = self.hw.instrMem.read(addr)
        print('IM{:08x}: {:08x}'.format(addr, data))

    #打印数据存储器
    #输入：
    #   addr为地址
    #效果：
    #   打印当前数据存储器地址addr所在的一个字
    def dumpDataMem(self, addr):
        data = self.hw.dataMem.read(addr)
        print('DM{:08x}: {:08x}'.format(addr, data))

    #获取指令列表
    #输入：
    #   fileName为程序文件名
    #输出：
    #   程序中指令的列表
    #约束：
    #   程序文件的每一行是一个8位16进制数，表示一条指令
    def getListFromFile(fileName):
        instrList = []
        program = open(fileName, 'r')
        for line in program:
            instrList.append(int(line, 16))

        return instrList

    #加载程序
    #输入：
    #   fileName为程序文件名
    #效果：
    #   将程序写入指令存储器，地址从0开始，并将pc置为0
    def loadProgram(self, fileName):
        instrList = Debugger.getListFromFile(fileName)
        addr = 0
        for instr in instrList:
            self.hw.instrMem.write(addr, instr)
            self.hw.globalSync()
            addr = addr + 4

        self.hw.pc.write(0)
        self.hw.globalSync()
