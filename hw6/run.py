from scoreboard import Scoreboard

class Runner:
    #指令状态表项
    class InstrItem:
        def __init__(self):
            self.issue = 0
            self.execute = 0
            self.write = 0

    #功能部件
    class FuncUnit:
        def __init__(self, num, execTime, instrStat, scoreboard):
            self.num = num
            self.execTime = execTime
            self.instrStat = instrStat
            self.scoreboard = scoreboard

            self.clock = 0
            self.localClock = 0
            self.pc = 0

        def issue(self, pc, clock):
            self.clock = 1
            self.pc = pc
            instrItem = Runner.InstrItem()
            instrItem.issue = clock
            self.instrStat.append(instrItem)

        def run(self, clock):
            if self.clock == 1:     #读操作数
                if self.scoreboard.readControl(self.num):
                    self.instrStat[self.pc].read = clock
                    self.clock += 1
            elif self.clock == 2:   #执行
                if self.localClock == 0:    #未开始执行
                    if self.scoreboard.executeControl(self.num):
                        self.localClock = 1
                else:
                    self.localClock += 1

                if self.localClock == self.execTime:
                    self.localClock = 0
                    self.instrStat[self.pc].execute = clock
                    self.clock += 1
            elif self.clock == 3:   #写回结果
                if self.scoreboard.writeControl(self.num):
                    self.instrStat[self.pc].write = clock
                    self.clock = 0
                    self.pc = 0

    def __init__(self, program):
        self.regCnt = 32
        self.fuCnt = 4
        self.scoreboard = Scoreboard(32, 4)
        self.instrStat = []

        self.clock = 0
        self.fus = [
                Runner.FuncUnit(0, 1, self.instrStat, self.scoreboard),     #整数部件
                Runner.FuncUnit(1, 10, self.instrStat, self.scoreboard),    #乘法部件
                Runner.FuncUnit(2, 2, self.instrStat, self.scoreboard),     #加法部件
                Runner.FuncUnit(3, 40, self.instrStat, self.scoreboard)     #除法部件
                ]

        self.program = program
        self.pc = 0

    def singleStepRun(self):
        self.clock += 1
        for i in range(4):
            self.fus[i].run(self.clock)
        if self.pc < len(self.program):
            instr = self.program[self.pc]
            if self.scoreboard.issueControl(instr):
                self.fus[instr.fu].issue(self.pc, self.clock)
                self.pc += 1
        self.scoreboard.sync()

    def run(self, circles):
        for i in range(circles):
            self.singleStepRun()

    def dump(self):
        print('{:<10}{:<10}{:<10}'.format('issue', 'execute', 'write'))
        for item in self.instrStat:
            print('{:<10}{:<10}{:<10}'.format(
                item.issue,
                item.execute,
                item.write
                ))
        print('')
        self.scoreboard.dump()
