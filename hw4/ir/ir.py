#程序类
class Program:
    def __init__(self):
        self.instrList = []     #指令列表，其中的元素或者是Instruction（非Condition），或者是Loop

    #将中间表示转化为代码并输出到文件
    #所有标有 TODO 的emit函数都应该由中间表示转化模块的编写者来实现
    def emit(self):
        #TODO
        pass

#循环类
class Loop:
    def __init__(self, condition, body):
        self.condi = condition  #条件检查，是一个Instruction列表，其中有且仅有最后一项是Condition
        self.body = body        #循环体，是一个Program

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
