from hw4.ir.ir import *

VREG_NUM = 500
REG_NUM = 32

reg_status = {i: None for i in range(REG_NUM)}  # 寄存器状态图，键为编号，值为使用该寄存器的指令，None表示空闲
vreg_status = {'v%d' % i: None for i in range(VREG_NUM)}  # 虚拟寄存器状态图


class AllocateException(BaseException):
    def __init__(self, info):
        self.info = info

    def __str__(self):
        return self.info


# 随机分配空闲虚拟寄存器
def allocate_vreg(ir):
    for vreg in vreg_status.keys():
        if vreg_status[vreg] is None:
            vreg_status[vreg] = ir
            return vreg
    raise AllocateException('虚拟寄存器已满！')


# 释放某一虚拟寄存器
def free_vreg(i):
    vreg_status[i] = None


def free_reg(i):
    reg_status[i] = None


def allocate_reg(ir):
    for reg in reg_status.keys():
        if reg_status[reg] is None:
            reg_status[reg] = ir
            return reg
    # 若寄存器已满，分配虚拟寄存器
    allocate_vreg(ir)


# 数据相关性分析
def analyze_hazard(cycle):
    hazard = {'RAW': [],
              'WAR': [],
              'WAW': []}
    write = []  # 记录所有写操作
    read = []  # 记录所有读操作
    # 分析数据相关性
    for instr in cycle.instrList:  # 标记所有读取和写入的寄存器
        if instr.rt is not None:
            write.append(instr.rt)
        if instr.rs is not None:
            read.append(instr.rs)
    # 检测写后读(RAW)
    for i in range(len(write)):
        for j in range(i + 1, len(read)):
            if write[i] in read[j]:
                hazard['RAW'].append((cycle.instrList[i], cycle.instrList[j]))
    # 检测读后写(WAR)
    for i in range(len(read)):
        for j in range(i + 1, len(write)):
            if write[j] in read[i]:
                hazard['WAR'].append((cycle.instrList[i], cycle.instrList[j]))
    # 检测读后读(WAW)
    for i in range(len(write)):
        for j in range(i + 1, len(write)):
            if write[i] == write[j]:
                hazard['WAW'].append((cycle.instrList[i], cycle.instrList[j]))
    return hazard


# 判断两条指令是否相关
def judge_hazard(instr1, instr2, hazard):
    if (instr1, instr2) in hazard['RAW'] or (instr1, instr2) in hazard['WAR'] or (instr1, instr2) in hazard['WAW']:
        return True
    elif (instr2, instr1) in hazard['RAW'] or (instr2, instr1) in hazard['WAR'] or (instr2, instr1) in hazard['WAW']:
        return True
    return False


# 延迟分析
def get_stall(op_this, op_next):
    if isinstance(op_this, AluInstr):
        if isinstance(op_next, AluInstr):
            return 3
        elif isinstance(op_next, Store):
            return 2
        elif isinstance(op_next, Condition):
            return 1
        else:
            return 0
    elif isinstance(op_this, Load):
        if isinstance(op_next, AluInstr):
            return 1
        elif isinstance(op_next, Store):
            return 0
        elif isinstance(op_next, Condition):
            return 1
        else:
            raise ValueError('Error Instruction!')
    elif isinstance(op_this, Condition):
        return 1
    else:
        return 0


# 在指令1和指令2之间插入一条不相关的指令
def insert_instr(cycle, hazard, instr1, instr2, isAllocated):
    for item in cycle.instrList:
        if not judge_hazard(instr1, instr2, hazard):
            if isAllocated[item] == 0:
                isAllocated[item] = 1
                return item
    return None


# 循环展开
# 输入：
#   ir为源代码的中间表示
#   times为展开的次数 不少于2
# 输出：
#   ir中循环展开times次的中间表示
def unroll(ir, times):
    global ld_rt, ld_rs, ld_offset, st_rt, st_rs, add_rt, add_rs, addi_rt, addi_rs, addi_imm, cycle
    rlt = {'before': [],
           'last': []}
    isAllocated = {}

    # 找到循环部分
    for item in ir:
        if isinstance(item, Loop):
            cycle = item
    if cycle is None:
        raise ValueError('没有循环部分！')

    # 分析原始指令的操作数
    for item in cycle.instrList:
        if isinstance(item, Load):
            ld_rt = item.rt
            ld_rs = item.rs
            ld_offset = item.offset
        elif isinstance(item, Store):
            st_rt = item.rt
            st_rs = item.rs
        elif isinstance(item, Add):
            add_rt = item.rt
            add_rs = item.rs
        elif isinstance(item, Addi):
            addi_rt = item.rt
            addi_rs = item.rs
            addi_imm = item.imm


    # 前若干次
    rlt['before'].append(cycle.instrList[0])  # beq语句
    for time in range(cycle.times):
        for item in cycle.instrList:
            flag_add = 0
            flag_load = 0
            add_rt_new = None
            load_rt_new = None
            if isinstance(item, Load):
                flag_add = 1
                offset = addi_imm * (time + 1)  # 每次offset增加一轮
                try:
                    load_rt_new = allocate_reg(item)  # 分配虚拟寄存器
                    new_load = Load(reg1=load_rt_new, offset=offset, reg2=ld_rs)
                    rlt['before'].append(new_load)
                except AllocateException as e:
                    print(e)

            elif isinstance(item, Add):
                flag_load = 1
                try:
                    add_rt_new = allocate_reg(item)
                    new_add = Add(reg1=add_rt_new, reg2=add_rs[0], reg3=add_rs[1])
                    rlt['before'].append(new_add)
                except AllocateException as e:
                    print(e)

            elif isinstance(item, Store):
                if flag_add == 1 and flag_load == 1:  # 找到与该stroe配套的load和add
                    flag_add = 0
                    flag_load = 0
                    offset = addi_imm * (time + 1)
                    try:
                        new_store = Store(reg1=item.rt, offset=offset, reg2=st_rs)
                        rlt['before'].append(new_store)
                        # store结束后即可释放之前的寄存器
                        free_reg(add_rt_new)
                        free_reg(load_rt_new)

                    except AllocateException as e:
                        print(e)
    cycle_iter_new = None
    for item in cycle.instrList:
        if isinstance(item, Addi):  # 循环变量自增语句
            cycle_iter_new = allocate_reg(item)
            new_addi = Addi(reg1=cycle_iter_new, reg2=cycle.iter, imm=cycle.times * addi_imm)
            rlt['before'].append(new_addi)
            break

    # 计算新的终止条件
    new_reg_for_stop = allocate_reg(Addi(None, None, None))
    new_addi_for_stop = Addi(reg1=new_reg_for_stop, reg2=cycle.times, imm=1 - times)
    rlt['before'].append(new_addi_for_stop)

    for item in cycle.instrList:
        if isinstance(item, Bne):  # Bne  循环终止条件为cycle.iter = cycle.times-times+1
            new_bne = Bne(reg1=cycle_iter_new, reg2=new_reg_for_stop)
            rlt['before'].append(new_bne)
            break

    # 最后一次
    rlt['last'] = cycle
    return rlt

