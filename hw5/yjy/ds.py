
# IS表中的元素
class Ins_Status:
    def __init__(self):
        self.issue = 'None'
        self.oper = 'None'
        self.comp = 'None'
        self.result = 'None'

    def __str__(self):
        print_str = 'issue=' + str(self.issue) + '   '
        print_str += 'oper=' + str(self.oper) + '   '
        print_str += 'comp=' + str(self.comp) + '   '
        print_str += 'result=' + str(self.result)
        return print_str


# FUS表的元素
class FU_Status:

    def __init__(self):
        self.busy = 'No'
        self.op = 'None'
        self.fi = 'None'
        self.fj = 'None'
        self.fk = 'None'
        self.qj = 'None'
        self.qk = 'None'
        self.rj = 'None'
        self.rk = 'None'

    def __str__(self):
        print_str = 'busy=' + self.busy + '   '
        print_str += 'op=' + str(self.op) + '   '
        print_str += 'fi=' + self.fi + '   '
        print_str += 'fj=' + self.fj + '   '
        print_str += 'fk=' + self.fk + '   '
        print_str += 'qj=' + str(self.qj) + '   '
        print_str += 'qk=' + str(self.qk) + '   '
        print_str += 'rj=' + self.rj + '   '
        print_str += 'rk=' + self.rk
        return print_str

    def clear(self):
        self.busy = 'No'
        self.op = 'None'
        self.fi = 'None'
        self.fj = 'None'
        self.fk = 'None'
        self.qj = 'None'
        self.qk = 'None'
        self.rj = 'None'
        self.rk = 'None'
