@0
D=A
@SP
A=M
M=D
@SP
M=M+1
@SP
M=M-1
A=M
D=M
@popdata0
M=D
@0
D=A
@LCL
D=D+M
@local.0
M=D
@popdata0
D=M
@local.0
A=M
M=D
(BasicLoop$LOOP_START)
@0
D=A
@ARG
A=D+M
D=M
@SP
A=M
M=D
@SP
M=M+1
@0
D=A
@LCL
A=D+M
D=M
@SP
A=M
M=D
@SP
M=M+1
@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
M=D+M
@SP
M=M+1
@SP
M=M-1
A=M
D=M
@popdata1
M=D
@0
D=A
@LCL
D=D+M
@local.1
M=D
@popdata1
D=M
@local.1
A=M
M=D
@0
D=A
@ARG
A=D+M
D=M
@SP
A=M
M=D
@SP
M=M+1
@1
D=A
@SP
A=M
M=D
@SP
M=M+1
@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
M=M-D
@SP
M=M+1
@SP
M=M-1
A=M
D=M
@popdata2
M=D
@0
D=A
@ARG
D=D+M
@argument.2
M=D
@popdata2
D=M
@argument.2
A=M
M=D
@0
D=A
@ARG
A=D+M
D=M
@SP
A=M
M=D
@SP
M=M+1
@SP
M=M-1
A=M
D=M
@BasicLoop$LOOP_START
D;JNE
@0
D=A
@LCL
A=D+M
D=M
@SP
A=M
M=D
@SP
M=M+1
