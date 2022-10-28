## 1 实现指令
实现一条指令的步骤如下：
- 写一个类(class)继承`instruction/instruction.py`中的`Instruction`类，实现四个方法
- 在`run/controller.py`中的`opMap`或`funcMap`中加入所写的类名
    - 如果指令的op字段不为0，则加入`opMap`，键值为op字段的值
    - 如果指令的op字段为0，则加入`funcMap`，键值为func字段的值

## 2 硬件结构
### 2.1 寄存器与存储器
寄存器和存储器的实现在`hardware/util.py`中，可以阅读一下

### 2.2 硬件结构图示
TODO

## 3 运行与调试
### 3.1 工具
`run/controller.py`中有执行指令的方法，现在只能一次执行一条指令
`run/debugger.py`中有一些方便调试的方法，包括打印寄存器和存储器、将程序加载到指令存储器等

### 3.2 例子
`prog/addiu.txt`是一个程序的例子，就是把指令的编码（16进制）直接写出来，每行一条指令
`main.py`是一个运行的例子，可以阅读一下
