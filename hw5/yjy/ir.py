# 程序类
class Program:
    def __init__(self):
        self.instrList = []  # 指令列表，其中的元素或者是Instruction，或者是Loop

    # 将中间表示转化为代码并输出到文件
    def emit(self, stream, cnt):
        for instr in self.instrList:
            instr.emit(stream, cnt)

        return cnt


# 循环类
class Loop:
    def __init__(self, iterator, times):
        self.iter = iterator  # 循环变量，是一个寄存器
        self.times = times  # 循环次数，是一个寄存器
        self.instrList = []  # 指令列表，其中的元素是Instruction或Loop，应该有如下的形式
        '''
        beq i, n, out
        loop:
        [loop body]
        addi i, i, 1
        bne i, n, loop
        out:
        '''

    def emit(self, stream, cnt):
        cnt = cnt + 1
        for i in range(len(self.instrList)):
            if i == 0:
                self.instrList[0].emit(stream, cnt)
                stream.write('loop' + str(cnt) + ':\n')
            else:
                self.instrList[i].emit(stream, cnt)

        stream.write('out' + str(cnt) + ':\n')
        return cnt


# 指令类
class Instruction:
    def __init__(self):
        self.rs = []  # 源寄存器，是一个列表，其中的元素是该指令读取的所有寄存器号
        # 注意这个列表里去掉了重复的元素
        self.rt = None  # 目的寄存器，是该指令写入的寄存器号
        self.instrStr = None  # 指令字符串

    def emit(self, stream, cnt):
        pass


# 存储访问指令类
class MemInstr(Instruction):
    def emit(self, stream, cnt):
        stream.write(self.instrStr + '\n')
        return cnt


# Load
class Load(MemInstr):
    # load reg1, offset(reg2)
    def __init__(self, reg1, offset, reg2):
        super().__init__()
        self.rt = reg1
        self.rs.append('None')
        self.rs.append(reg2)
        self.offset = offset
        self.instrStr = 'load r' + str(reg1) + ', ' + str(offset) + '(r' + str(reg2) + ')'
        self.fu = 'Integer'


# Store
class Store(MemInstr):
    # store reg1, imm(reg2)
    def __init__(self, reg1, offset, reg2):
        super().__init__()

        # 去掉重复的元素
        self.rs.append(reg1)
        if reg1 != reg2:
            self.rs.append(reg2)

        self.offset = offset
        self.instrStr = 'store r' + str(reg1) + ', ' + str(offset) + '(r' + str(reg2) + ')'


# ALU型指令类
class AluInstr(Instruction):
    def emit(self, stream, cnt):
        stream.write(self.instrStr + '\n')
        return cnt


# Nop
class Nop(AluInstr):
    # nop
    def __init__(self):
        super().__init__()
        self.instrStr = 'nop'


# Add
class Add(AluInstr):
    # add reg1, reg2, reg3
    def __init__(self, reg1, reg2, reg3):
        super().__init__()
        self.rt = reg1
        self.fu = 'Add'

        # 去掉重复的元素
        self.rs.append(reg2)
        if reg2 != reg3:
            self.rs.append(reg3)

        self.instrStr = 'add r' + str(reg1) + ', r' + str(reg2) + ', ' + str(reg3)


# Sub
class Sub(AluInstr):
    # add reg1, reg2, reg3
    def __init__(self, reg1, reg2, reg3):
        super().__init__()
        self.rt = reg1
        self.fu = 'Add'

        # 去掉重复的元素
        self.rs.append(reg2)
        if reg2 != reg3:
            self.rs.append(reg3)

        self.instrStr = 'sub r' + str(reg1) + ', r' + str(reg2) + ', ' + str(reg3)

# Mul
class Mul(AluInstr):
    # Mul reg1, reg2, reg3
    def __init__(self, reg1, reg2, reg3):
        super().__init__()
        self.rt = reg1
        self.fu = 'Mul'

        # 去掉重复的元素
        self.rs.append(reg2)
        if reg2 != reg3:
            self.rs.append(reg3)

        self.instrStr = 'mul r' + str(reg1) + ', r' + str(reg2) + ', ' + str(reg3)


# Div
class Div(AluInstr):
    # Div reg1, reg2, reg3
    def __init__(self, reg1, reg2, reg3):
        super().__init__()
        self.rt = reg1
        self.fu = 'Div'

        # 去掉重复的元素
        self.rs.append(reg2)
        if reg2 != reg3:
            self.rs.append(reg3)

        self.instrStr = 'div r' + str(reg1) + ', r' + str(reg2) + ', ' + str(reg3)


# Move
class Move(AluInstr):
    # move reg1, reg2
    def __init__(self, reg1, reg2):
        super().__init__()
        self.rt = reg1
        self.rs.append(reg2)
        self.fu = 'Integer'
        self.instrStr = 'move r' + str(reg1) + ', r' + str(reg2)


# Addi
class Addi(AluInstr):
    # addi reg1, reg2, imm
    def __init__(self, reg1, reg2, imm):
        super().__init__()
        self.rt = reg1
        self.rs.append(reg2)
        self.imm = imm
        self.fu = 'Add'
        self.instrStr = 'addi r' + str(reg1) + ', r' + str(reg2) + ', ' + str(imm)


# 条件跳转指令类
class Condition(Instruction):
    pass


# Bne
class Bne(Condition):
    # bne reg1, reg2, label
    def __init__(self, reg1, reg2):
        # Bne对象的属性中不需要包含label，它应该在将中间表示转化为代码时被加上
        super().__init__()

        # 去掉重复的元素
        self.rs.append(reg1)
        if reg1 != reg2:
            self.rs.append(reg2)

        self.instrStr = 'bne r' + str(reg1) + ', r' + str(reg2)

    def emit(self, stream, cnt):
        instrStr = self.instrStr + ', out' + str(cnt)
        stream.write(instrStr + '\n')

        return cnt


# Beq
class Beq(Condition):
    # beq reg1, reg2, label
    def __init__(self, reg1, reg2):
        super().__init__()

        # 去掉重复的元素
        self.rs.append(reg1)
        if reg1 != reg2:
            self.rs.append(reg2)

        self.instrStr = 'beq r' + str(reg1) + ', r' + str(reg2)

    def emit(self, stream, cnt):
        instrStr = self.instrStr + ', loop' + str(cnt)
        stream.write(instrStr + '\n')

        return cnt

