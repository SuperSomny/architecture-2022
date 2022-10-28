from hardware.util import Register, Memory

#硬件资源
class Hardware:
    def __init__(self):
        #寄存器
        self.genRegCnt = 32     #通用寄存器数
        self.genReg = [Register()] * self.genRegCnt #通用寄存器组

        self.pplReg = {                             #流水线寄存器
                #WB/IF
                'pc': Register(),    #程序计数器
                #IF/ID
                'instr': Register(), #指令寄存器
                #ID/EX
                'rs': Register(),    #指令的rs字段[21: 25]对应寄存器的值
                'rt': Register(),    #指令的rt字段[16: 20]对应寄存器的值
                'rd': Register(),    #指令的rd字段[11: 15]对应寄存器的值
                'imm': Register(),   #指令的imm字段[0: 15]
                #EX/MA
                'addr': Register(),  #数据存储器的地址
                'wdata': Register(), #数据存储器的输入数据
                #MA/WB
                'wb': Register(),    #写回寄存器
                }
        self.pc = self.pplReg['pc']
        self.instr = self.pplReg['instr']
        self.rs = self.pplReg['rs']
        self.rt = self.pplReg['rt']
        self.rd = self.pplReg['rd']
        self.imm = self.pplReg['imm']
        self.addr = self.pplReg['addr']
        self.wdata = self.pplReg['wdata']
        self.wb = self.pplReg['wb']

        #存储器
        self.instrMemSize = 1 << 32 #指令存储器字节数
        self.dataMemSize = 1 << 32  #数据存储器字节数

        self.instrMem = Memory(self.instrMemSize)   #指令存储器
        self.dataMem = Memory(self.dataMemSize)     #数据存储器

    #全局同步
    #效果：
    #   对所有寄存器和存储器进行同步
    def globalSync(self):
        #通用寄存器同步
        for reg in self.genReg:
            reg.sync()

        #流水线寄存器同步
        for reg in self.pplReg:
            reg.sync()

        #存储器同步
        self.instrMem.sync()
        self.dataMem.sync()
