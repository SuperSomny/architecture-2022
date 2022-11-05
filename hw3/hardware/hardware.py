from hardware.util import Register, Memory

#硬件资源
class Hardware:
    def __init__(self):
        #寄存器
        self.pc = Register()    #程序计数器

        #通用寄存器
        self.genRegCnt = 32 #通用寄存器数
        self.genReg = []    #通用寄存器组
        for i in range(self.genRegCnt):
            self.genReg.append(Register())

        #流水线寄存器
        #   约定：指令在第i个阶段可以读pplReg[i]中的寄存器、写pplReg[i+1]中的寄存器
        self.pplRegCnt = 5  #流水线上每个阶段的寄存器数
        self.stageCnt = 5   #流水线阶段数
        self.pplReg = []    #流水线寄存器
        for i in range(self.stageCnt):
            stage = []
            for j in range(self.pplRegCnt):
                stage.append(Register())
            self.pplReg.append(stage)

        #存储器
        self.instrMemSize = 1 << 32 #指令存储器字节数
        self.dataMemSize = 1 << 32  #数据存储器字节数

        self.instrMem = Memory(self.instrMemSize)   #指令存储器
        self.dataMem = Memory(self.dataMemSize)     #数据存储器

    #全局同步
    #效果：
    #   对所有寄存器和存储器进行同步
    def globalSync(self):
        #程序计数器同步
        self.pc.sync()

        #通用寄存器同步
        for reg in self.genReg:
            reg.sync()

        #流水线寄存器同步
        for stage in self.pplReg:
            for reg in stage:
                reg.sync()

        #存储器同步
        self.instrMem.sync()
        self.dataMem.sync()
