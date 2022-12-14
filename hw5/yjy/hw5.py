from utils import *
from ir import *
from ds import Ins_Status, FU_Status

INS_NUM = 6

# IS表 长度为指令条数
IS = [Ins_Status() for _ in range(INS_NUM)]
# FUS表
FUS = {'Integer': FU_Status(),
       'Mul1': FU_Status(),
       'Mul2': FU_Status(),
       'Add': FU_Status(),
       'Divide': FU_Status()
       }
# RSS表
RSS = {'F%d' % (2 * i): 'None' for i in range(16)}

# 指令列表
ins_list = [Load(reg1='F6', offset=34, reg2='R2'),
            Load(reg1='F2', offset=45, reg2='R3'),
            Mul(reg1='F0', reg2='F2', reg3='F4'),
            Sub(reg1='F8', reg2='F6', reg3='F2'),
            Div(reg1='F10', reg2='F0', reg3='F6'),
            Add(reg1='F6', reg2='F8', reg3='F2')]


# 指令流出阶段   避免结构冲突和WAR冲突
def Issue(ins_num):
    fu = FU_allocate(ins_list[ins_num].fu, FUS)
    if (fu is not None) and Result_write(ins_list[ins_num].rt, RSS):  # 如果当前指令所需的部件空闲 and 记分牌中已经存在的指令不对当前指令的目的寄存器进行写操作
        FUS_item = FUS[fu]
        # 改写FUS表该部件行
        FUS_item.busy = 'Yes'
        FUS_item.op = type(ins_list[ins_num])
        FUS_item.fi = ins_list[ins_num].rt
        FUS_item.fj = ins_list[ins_num].rs[0]
        FUS_item.fk = ins_list[ins_num].rs[1]

        try:  # 如果源操作数不来自任何一个部件则qj为空
            FUS_item.qj = RSS[FUS_item.fj]
        except:
            FUS_item.qj = 'None'
        try:  # 如果源操作数不来自任何一个部件则qk为空
            FUS_item.qk = RSS[FUS_item.fk]
        except:
            FUS_item.qk = 'None'

        # 源操作数寄存器是否就绪
        if FUS_item.fj != 'None':
            if RS_ready(FUS_item.fj, RSS):
                FUS_item.rj = 'Yes'
            else:
                FUS_item.rj = 'No'
        else:
            FUS_item.rj = 'None'

        if RS_ready(FUS_item.fk, RSS):
            FUS_item.rk = 'Yes'
        else:
            FUS_item.rk = 'No'

        RSS[ins_list[ins_num].rt] = fu

        # 发出指令
        IS[ins_num].issue = clock
        return fu
    # 不满足条件则等待
    else:
        return 'Wait'


# 读操作数阶段   避免RAW冲突
def Read_Operands(ins_num, fu):
    if (FUS[fu].rj != 'No') and (FUS[fu].rk != 'No'):  # rj和rk就绪，读操作数
        # 检查RAW冲突
        if FUS[fu] not in hazards['RAW']:
            IS[ins_num].oper = clock
            # if FUS[fu].rj != 'None':
            #     FUS[fu].rj = 'No'
            # if FUS[fu].rk != 'None':
            #     FUS[fu].rk = 'No'
            # FUS[fu].qj = 'None'
            # FUS[fu].qk = 'None'
            return 'Success'
    else:
        return 'Wait'


# 执行阶段 无需对表的任何操作
def Execution(ins_num, fu):
    # 返回需要的时钟周期数
    if FUS[fu].rj != 'None':
        FUS[fu].rj = 'No'
    if FUS[fu].rk != 'None':
        FUS[fu].rk = 'No'
    FUS[fu].qj = 'None'
    FUS[fu].qk = 'None'
    if isinstance(ins_list[ins_num], Mul):
        return 10
    elif isinstance(ins_list[ins_num], Div):
        return 40
    elif isinstance(ins_list[ins_num], Add) or isinstance(ins_list[ins_num], Sub):
        return 2
    else:
        return 1


# 写结果阶段  避免WAR冲突
def Write_Resut(ins_num, fu):
    # 在FUS表中的每一条指令进行逐一查看，如果不存在任意一条指令的源操作数寄存器与当前指令的目的操作数寄存器相同 且对应的寄存器处于读就绪状态
    for _, item in FUS.items():
        if (item.fj == ins_list[ins_num].rt) and item.rj == 'Yes':
            return 'Wait'
        try:
            if (item.fk == ins_list[ins_num].rt) and item.rk == 'Yes':
                return 'Wait'
        finally:
            pass
    # 则修改记分牌内容
    # 检查FUS中每条指令的qj和qk域，如果存在一条指令以当前指令的结果作为源操作数，则将那一条指令对应的rj或rk设为Yes
    for _, item in FUS.items():
        if item.qj == fu:
            item.rj = 'Yes'
        if item.qk == fu:
            item.rk = 'Yes'
    # 将RSS中当前指令对应的元素设置为空
    RSS[FUS[fu].fi] = 'None'
    # 同时级联修改FUS中所有的qj和qk，如果存在当前部件则释放
    for _, value in FUS.items():
        if value.qj == fu:
            value.qj = 'None'
        if value.qk == fu:
            value.qk = 'None'

    # ???? 将FUS中对应的部件的Busy域设置为No ????
    # ???? FUS[fu].busy = 'No' ????

    # 将FUS中对应的行清空
    FUS[fu].clear()
    IS[ins_num].result = clock
    return 'Success'


def print_tables():
    print('---------------------IS---------------------')
    for item in IS:
        print(item)
    print('---------------------FUS---------------------')
    for key, value in FUS.items():
        print('{:7s}'.format(key), value)
    print('---------------------RSS---------------------')
    for key, _ in RSS.items():
        print('{:7s}'.format(key), end=' ')
    print('\n', end='')
    for _, value in RSS.items():
        print('{:7s}'.format(value), end=' ')
    print('\n')


if __name__ == '__main__':
    # 时钟
    clock = 1
    Uncomp_list = ins_list.copy()
    # 初始阶段所有指令都等待Issue
    IF_list = [i for i in range(len(ins_list))]
    ID_list = []  # ID EX WB的元素都是元组 (指令,功能部件)
    EX_list = []
    WB_list = []
    Comp_list = []

    hazards = analyze_hazard(Uncomp_list)
    ex_clock_list = {}
    # 执行直到所有任务完成
    while len(Comp_list) < len(ins_list):
        print('################   CLOCK = %d  ################ ' % clock)
        fu = ''
        issued = False
        fetched = []
        executed = []
        written = []
        if len(IF_list) != 0:  # 发出指令，若成功，在IF中去除该指令，在ID中添加该指令
            fu = Issue(IF_list[0])
            if fu != 'Wait':
                issued = True

        if len(ID_list) != 0:
            for i in range(len(ID_list)):
                if Read_Operands(ID_list[i][0], ID_list[i][1]) == 'Success':  # 取操作数，若成功，在ID中去除该指令，在EX中添加该指令
                    fetched.append(ID_list[i])

        if len(EX_list) != 0:
            for i in range(len(EX_list)):
                # 如果该指令没有在“正在运行的指令”字典中，启动局部计数器
                try:
                    if ex_clock_list[EX_list[i][0]] is not None:
                        pass
                except:
                    ex_clock = Execution(EX_list[i][0], EX_list[i][1])
                    if ex_clock == 1:  # 如果指令只需1个周期完成，则不需要计数器
                        IS[EX_list[i][0]].comp = clock
                        executed.append(EX_list[i])
                    else:
                        ex_clock_list[EX_list[i][0]] = ex_clock - 1  # 该次循环结束后已经过一个周期

            # 若某条指令的计数器终止，则认为已完成
            for i in range(len(EX_list)):
                try:
                    if ex_clock_list[EX_list[i][0]] == 0:
                        IS[EX_list[i][0]].comp = clock
                        executed.append(EX_list[i])
                        ex_clock_list.pop(EX_list[i][0])
                except:
                    pass

        if len(WB_list) != 0:
            for i in range(len(WB_list)):
                if Write_Resut(WB_list[i][0], WB_list[i][1]) == 'Success':
                    written.append(WB_list[i])

        # 统计该周期完成的动作，并且更新下一步动作
        if issued:
            ID_list.append((IF_list[0], fu))
            IF_list.remove(IF_list[0])
        if len(fetched):
            for item in fetched:
                EX_list.append(item)
                ID_list.remove(item)
        if len(executed):
            for item in executed:
                WB_list.append(item)
                EX_list.remove(item)
        if len(written):
            for item in written:
                Comp_list.append(item)
                Uncomp_list.remove(ins_list[item[0]])  # 一条指令结束后更新hazard表
                WB_list.remove(item)
            hazards = analyze_hazard(Uncomp_list)

        clock += 1
        for key, value in ex_clock_list.items():  # 局部时钟-1
            print('局部时钟：', end=' ')
            print(ins_list[key], value)
            ex_clock_list[key] -= 1
        print_tables()
