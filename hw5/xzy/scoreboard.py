from util import Register

#计分板
class Scoreboard:
    #功能部件状态表项
    class FuncUnitItem:
        def __init__(self, fuCnt):
            self.busy = Register(False)
            self.op = Register('')

            self.src1Valid = Register(False)
            self.src1 = Register(0)
            self.fu1 = Register(fuCnt)
            self.ready1 = Register(False)

            self.src2Valid = Register(False)
            self.src2 = Register(0)
            self.fu2 = Register(fuCnt)
            self.ready2 = Register(False)

            self.destValid = Register(False)
            self.dest = Register(0)

        #同步
        def sync(self):
            self.busy.sync()
            self.op.sync()
            self.src1Valid.sync()
            self.src1.sync()
            self.fu1.sync()
            self.ready1.sync()
            self.src2Valid.sync()
            self.src2.sync()
            self.fu2.sync()
            self.ready2.sync()
            self.destValid.sync()
            self.dest.sync()

    def __init__(self, regCnt, fuCnt):
        self.regCnt = regCnt
        self.fuCnt = fuCnt
        self.regResStat = [Register(fuCnt) for i in range(regCnt)]                  #寄存器结果状态表
        self.funcUnitStat = [Scoreboard.FuncUnitItem(fuCnt) for i in range(fuCnt)]  #功能部件状态表

    #同步
    def sync(self):
        for item in self.regResStat:
            item.sync()
        for item in self.funcUnitStat:
            item.sync()

    #检查功能部件号是否有效
    #约定：功能部件号为功能部件总数表示无效
    def fuValid(self, fu):
        return fu < self.fuCnt

    def issueControl(self, instr):
        fuItem = self.funcUnitStat[instr.fu]

        #检查功能部件忙碌
        busy = fuItem.busy.read()

        #检查写后写
        waw = False
        if instr.destValid:
            waw |= self.fuValid(self.regResStat[instr.dest].read())

        if busy or waw: #阻塞
            return False

        fuItem.busy.write(True)     #占用功能部件
        fuItem.op.write(instr.op)   #记录操作

        #记录操作数信息
        fuItem.src1Valid.write(instr.src1Valid)
        if instr.src1Valid:
            fuItem.src1.write(instr.src1)
            fu1 = self.regResStat[instr.src1].read()
            fuItem.fu1.write(fu1)
            fuItem.ready1.write(not self.fuValid(fu1))
        fuItem.src2Valid.write(instr.src2Valid)
        if instr.src2Valid:
            fuItem.src2.write(instr.src2)
            fu2 = self.regResStat[instr.src2].read()
            fuItem.fu2.write(fu2)
            fuItem.ready2.write(not self.fuValid(fu2))

        #记录结果信息
        fuItem.destValid.write(instr.destValid)
        if instr.destValid:
            fuItem.dest.write(instr.dest)
            self.regResStat[instr.dest].write(instr.fu)

        return True

    def readControl(self, fu):
        fuItem = self.funcUnitStat[fu]
        src1Valid = fuItem.src1Valid.read()
        src2Valid = fuItem.src2Valid.read()

        #检查指令未发出
        unissued = not fuItem.busy.read()

        #检查写后读
        raw = False
        if src1Valid:
            raw |= not fuItem.ready1.read()
        if src2Valid:
            raw |= not fuItem.ready2.read()

        if unissued or raw: #阻塞
            return False

        #操作数已读取
        if src1Valid:
            fuItem.fu1.write(self.fuCnt)
            fuItem.ready1.write(False)
        if src2Valid:
            fuItem.fu2.write(self.fuCnt)
            fuItem.ready2.write(False)

        return True

    def executeControl(self, fu):
        fuItem = self.funcUnitStat[fu]

        #检查指令未发出
        unissued = not fuItem.busy.read()

        if unissued:    #阻塞
            return False
        return True

    def writeControl(self, fu):
        fuItem = self.funcUnitStat[fu]
        destValid = fuItem.destValid.read()

        #检查指令未发出
        unissued = not fuItem.busy.read()

        #检查读后写
        war = False
        if destValid:
            dest = fuItem.dest.read()
            for f in self.funcUnitStat:
                if f.src1Valid.read():
                    war |= (f.src1.read() == dest) and f.ready1.read()
                if f.src2Valid.read():
                    war |= (f.src2.read() == dest) and f.ready2.read()

        if unissued or war: #阻塞
            return False

        if destValid:
            #所有依赖该结果的指令可以读操作数
            for f in self.funcUnitStat:
                if f.src1Valid.read() and f.fu1.read() == fu:
                    f.ready1.write(True)
                if f.src2Valid.read() and f.fu2.read() == fu:
                    f.ready2.write(True)

            #结果已写回
            self.regResStat[fuItem.dest.read()].write(self.fuCnt)

        #功能部件不再被占用
        fuItem.busy.write(False)
        fuItem.src1Valid.write(False)
        fuItem.src2Valid.write(False)
        fuItem.destValid.write(False)

        return True

    #打印
    def dump(self):
        #打印功能部件状态表
        print('{:<10}{:<10}{:<10}{:<10}{:<10}{:<10}{:<10}{:<10}'.format(
            'busy',
            'dest',
            'src1',
            'src2',
            'fu1',
            'fu2',
            'ready1',
            'ready2'
            ))
        for item in self.funcUnitStat:
            busy = item.busy.read()
            if item.destValid.read():
                dest = item.dest.read()
            else:
                dest = ''

            src1 = item.src1.read()
            fu1 = item.fu1.read()
            if not self.fuValid(fu1):
                fu1 = ''
            ready1 = item.ready1.read()
            if not item.src1Valid.read():
                src1 = ''
                fu1 = ''
                ready1 = ''

            src2 = item.src2.read()
            fu2 = item.fu2.read()
            if not self.fuValid(fu2):
                fu2 = ''
            ready2 = item.ready2.read()
            if not item.src2Valid.read():
                src2 = ''
                fu2 = ''
                ready2 = ''

            print('{:<10}{:<10}{:<10}{:<10}{:<10}{:<10}{:<10}{:<10}'.format(
                busy,
                dest,
                src1,
                src2,
                fu1,
                fu2,
                ready1,
                ready2
                ))
        print('')

        #打印寄存器结果状态表
        for i in range(self.regCnt):
            if i % 2 == 0:
                print('F{:<3}'.format(i), end = ' ')
        print('')
        for i in range(self.regCnt):
            if i % 2 == 0:
                fu = self.regResStat[i].read()
                if not self.fuValid(fu):
                    fu = ''
                print('{:<4}'.format(fu), end = ' ')
        print('')
