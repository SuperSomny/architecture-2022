# 数据相关性分析
def analyze_hazard(ins_list):
    hazard = {'RAW': [],
              'WAR': [],
              'WAW': []}
    write = []  # 记录所有的写操作
    read = []  # 记录所有的读操作
    # 分析数据相关性
    for instr in ins_list:  # 标记所有读取和写入的寄存器
        if instr.rt is not None:
            write.append(instr.rt)
        if instr.rs is not None:
            read.append(instr.rs)
    # 检测写后读(RAW)
    for i in range(len(write)):
        for j in range(i + 1, len(read)):
            if write[i] in read[j]:
                hazard['RAW'].append((i, j))
    # 检测读后写(WAR)
    for i in range(len(read)):
        for j in range(i + 1, len(write)):
            if write[j] in read[i]:
                hazard['WAR'].append((i, j))
    # 检测读后读(WAW)
    for i in range(len(write)):
        for j in range(i + 1, len(write)):
            if write[i] == write[j]:
                hazard['WAW'].append((i, j))
    return hazard


# 为指令分配功能部件，如果没有空余返回None
def FU_allocate(fu, FUS):
    if fu == 'Mul':
        if not (FUS['Mul1'].busy == 'Yes' and FUS['Mul2'].busy == 'Yes'):
            if FUS['Mul1'].busy == 'No':
                return 'Mul1'
            else:
                return 'Mul2'
    elif fu == 'Add':
        if FUS['Add'].busy == 'No':
            return 'Add'
    elif fu == 'Div':
        if FUS['Divide'].busy == 'No':
            return 'Divide'
    else:
        if FUS['Integer'].busy == 'No':
            return 'Integer'
    return None


def Result_write(rs, RSS):
    if RSS[rs] == 'None':
        return True
    return False


def RS_ready(rs, RSS):
    try:
        if RSS[rs] == 'None':
            return True
        else:
            return False
    except:
        return True
