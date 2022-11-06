#程序类
class Program:
    def __init__(self):
        self.instrList = []     #指令列表，其中的元素或者是Instruction，或者是Loop

    #将中间表示转化为代码并输出到文件
    def emit(self):
        #TODO
        pass

#循环类
class Loop:
    def __init__(self, iterator, times, body):
        self.iter = iterator    #循环变量，是一个寄存器
        self.times = times      #循环次数，是一个寄存器
        self.body = body        #循环代码，是一个Program，应该有如下的形式
        '''
        beq i, n, out
        loop:
        [loop body]
        addi i, i, 1
        bne i, n, loop
        out:
        '''

    def emit(self):
        #TODO
        pass

#指令类
class Instruction:
    def __init__(self):
        self.rs = []    #源寄存器，是一个列表，其中的元素是该指令读取的所有寄存器号
                        #注意这个列表里去掉了重复的元素
        self.rt = None  #目的寄存器，是该指令写入的寄存器号

    def emit(self):
        pass

#Load
class Load(Instruction):
    def __init__(self, reg1, imm, reg2):
        #load reg1, imm(reg2)
        super().__init__()
        self.rt = reg1
        self.rs.append(reg2)
        self.offset = imm

    def emit(self):
        #TODO
        pass

#Store
class Store(Instruction):
    def __init__(self, reg1, imm, reg2):
        #store reg1, imm(reg2)
        super().__init__()

        #去掉重复的元素
        self.rs.append(reg1)
        if reg1 != reg2:
            self.rs.append(reg2)

        self.offset = imm

    def emit(self):
        #TODO
        pass

#ALU型指令类
class AluInstr(Instruction):
    def emit(self):
        pass

#Nop
class Nop(AluInstr):
    def __init__(self):
        super().__init__()

    def emit(self):
        #TODO
        pass

#Add
class Add(AluInstr):
    def __init__(self, reg1, reg2, reg3):
        #add reg1, reg2, reg3
        super().__init__()
        self.rt = reg1

        #去掉重复的元素
        self.rs.append(reg2)
        if reg2 != reg3:
            self.rs.append(reg3)

    def emit(self):
        #TODO
        pass

#Addi
class Addi(AluInstr):
    def __init__(self, reg1, reg2, imm):
        #addi reg1, reg2, imm
        super().__init__()
        self.rt = reg1
        self.rs.append(reg2)
        self.imm = imm

    def emit(self):
        #TODO
        pass

#条件跳转指令类
class Condition(Instruction):
    def emit(self):
        pass

#Bne
class Bne(Condition):
    def __init__(self, reg1, reg2):
        #bne reg1, reg2, label
        #Bne对象的属性中不需要包含label，它应该在将中间表示转化为代码时被加上
        super().__init__()

        #去掉重复的元素
        self.rs.append(reg1)
        if reg1 != reg2:
            self.rs.append(reg2)

    def emit(self):
        #TODO
        pass

#Beq
class Beq(Condition):
    def __init__(self, reg1, reg2):
        #beq reg1, reg2, label
        super().__init__()

        #去掉重复的元素
        self.rs.append(reg1)
        if reg1 != reg2:
            self.rs.append(reg2)

    def emit(self):
        #TODO
        pass
