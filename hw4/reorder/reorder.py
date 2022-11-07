from ir.ir import *

#指令重排
#输入：
#   ir为源代码对应的中间表示
#输出：
#   ir中指令按约束重排后的中间表示
def reorder(ir):

    # reorder list，在列表中重排指令
    ROL = ir
    n = len(ROL)
    i = 0
    
    # 根据相关性插入stall
    while i < n:
        if i < n - 1:
            if (ROL[i][0] == 'l') & (ROL[i+1][0] == 'a'):
                if (ROL[i][6] == ROL[i+1][9]) or (ROL[i][6] == ROL[i+1][12]):
                    ROL.insert(i+1, 'Stall')
                    i = i + 2
                    n = n + 1

            elif (ROL[i][0] == 'a') & (ROL[i+1][0] == 'a'):
                if (ROL[i][5] == ROL[i+1][9]) or (ROL[i][5] == ROL[i+1].instrStr[12]):
                    j = i + 1
                    while j < i + 4:
                        ROL.insert(j, 'Stall')
                    i = i + 4
                    n = n + 3

            elif (ROL[i][0] == 'a') & (ROL[i+1][0] == 's'):
                if ROL[i][5] == ROL[i+1][7]:
                    k = i + 1
                    while k < i + 3:
                        ROL.insert(k, 'Stall')
                        k = k + 1
                    i = i + 3
                    n = n + 2

            elif (ROL[i][0] == 'a') & (ROL[i+1][0] == 'b'):
                if (ROL[i][6] == ROL[i+1][6]) or (ROL[i][6] == ROL[i+1][9]):
                    ROL.insert(i + 1, 'Stall')
                    i = i + 2
                    n = n + 1

            elif (ROL[i][0] == 'b'):
                ROL.insert(i + 1, 'Stall')
                i = i + 2
                n = n + 1

            else:
                i = i + 1
                print(i)

        elif ROL[i][0] == 'b':
            ROL.insert(i + 1, 'Stall')
            break

        else:
            break

