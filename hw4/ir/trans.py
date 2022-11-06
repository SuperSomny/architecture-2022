from ir.ir import *

#中间表示转化为代码
#输入：
#   ir为中间表示
#   fileName为目的代码的文件名
#效果：
#   将ir对应的汇编代码写入fileName文件，若文件不存在则创建
def ir2code(ir, fileName):
    fileStream = open(fileName, 'w')
    ir.emit(fileStream)
