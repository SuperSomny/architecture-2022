from util import Register

#缓冲区
class Buffer:
    #缓冲区表项
    class BufferItem:
        #初始化
        def __init__(self):
            self.busy = Register(False) #缓冲区是否被占用
            self.val1 = Register(0)     #源操作数1的值
            self.src1 = Register(-1)    #源操作数1的来源
            self.val2 = Register(0)     #源操作数2的值
            self.src2 = Register(-1)    #源操作数2的来源

        #同步
        def sync(self):
            self.busy.sync()
            self.val1.sync()
            self.src1.sync()
            self.val2.sync()
            self.src2.sync()

    #初始化
    def __init__(self, itemCnt):
        self.itemCnt = itemCnt
        self.itemList = [BufferItem() for i in range(itemCnt)]

    #同步
    def sync(self):
        for item in self.itemList:
            item.sync()

    #缓冲区是否满
    #约束：
    #   缓冲区表项有busy域
    def isFull(self):
        for item in self.itemList:
            if not item.busy.read():
                return False
        return True

    #缓冲区中被占用的第一项
    def first(self):
        for item in self.itemList:
            if not item.busy.read():
                return item

#寄存器状态表
class RegStat:
    def __init__(self, regCnt):
        self.regCnt = regCnt
        self.regList = [Register(-1) for i in range(regCnt)]

    #同步
    def sync(self):
        for item in self.regList:
            item.sync()

#控制器
class Controller:
    def __init__(self, itemCntList, regCnt, regFile):
        self.itemCntList = itemCntList
        self.regCnt = regCnt

        #各个功能部件对应的缓冲区
        self.bufList = []
        for itemCnt in itemCntList():
            self.bufList.append(Buffer(itemCnt))

        #寄存器状态表
        self.regStat = RegStat(regCnt)

        #寄存器组
        self.regFile = regFile

    #同步
    def sync(self):
        for buf in self.bufList:
            buf.sync()
        self.regStat.sync()

    #发出指令控制
    def issueControl(self, instr):
        if Instruction.isLoad(instr.fu):        #Load指令
            return self.issueLoad(instr)
        elif Instruction.isStore(instru.fu):    #Store指令
            return self.issueStore(instr)
        else:                                   #计算指令
            return self.issueOp(instr)

    #发出计算指令
    def issueOp(self, instr):
        pass

    #发出访存型指令
    def issueMem(self, instr):
        pass

    #发出Load指令
    def issueLoad(self, instr):
        self.issueMem(instr)
        pass

    #发出Store指令
    def issueStore(self, instr):
        self.issueMem(instr)
        pass

    #读操作数控制
    def readControl(self, fu):
        if Instruction.isMem(fu):   #访存指令
            return self.readMem(fu)
        else:                       #计算指令
            return self.readOp(fu)

    #计算指令读操作数
    def readOp(self, fu):
        pass

    #访存指令读操作数
    def readMem(self):
        pass

    #执行控制
    def executeControl(self, fu):
        if Instruction.isLoad(fu):  #Load指令
            return self.executeLoad()
        else:                       #Store或计算指令
            return True

    #Load指令执行
    def executeLoad(self):
        pass

    #写回结果控制
    def writeControl(self):
        if Instruction.isStore(fu):
            return self.writeMem()
        else:
            return self.writeReg(fu)
