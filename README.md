## hardware
### util
工具类，实现了寄存器和存储器

### hardware
所有需要访问的寄存器和存储器

## run
### controller
用于控制指令的执行，建设中

### debugger
用于debug，建设中

## 注意
实现一条指令时，应该继承Instruction类，实现其中的instrDecode、execute、memAccess、writeBack方法，然后将实现的类加入controller中的opMap或funcMap中，使得这一条指令能够被执行

## instruction
### instruction
指令类的抽象，实现某一条指令时需要实现Instruction类

### nop
nop指令，什么也不做
