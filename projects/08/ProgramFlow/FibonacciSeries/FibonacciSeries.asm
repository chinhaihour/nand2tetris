@1
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
@THAT
M=D
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
@THAT
D=D+M
@that.0
M=D
@popdata0
D=M
@that.0
A=M
M=D
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
@popdata1
M=D
@1
D=A
@THAT
D=D+M
@that.1
M=D
@popdata1
D=M
@that.1
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
@2
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
(FibonacciSeries$MAIN_LOOP_START)
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
@FibonacciSeries$COMPUTE_ELEMENT
D;JNE
@FibonacciSeries$END_PROGRAM
0;JMP
(FibonacciSeries$COMPUTE_ELEMENT)
@0
D=A
@THAT
A=D+M
D=M
@SP
A=M
M=D
@SP
M=M+1
@1
D=A
@THAT
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
@popdata3
M=D
@2
D=A
@THAT
D=D+M
@that.3
M=D
@popdata3
D=M
@that.3
A=M
M=D
@THAT
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
M=D+M
@SP
M=M+1
@SP
M=M-1
A=M
D=M
@THAT
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
@popdata4
M=D
@0
D=A
@ARG
D=D+M
@argument.4
M=D
@popdata4
D=M
@argument.4
A=M
M=D
@FibonacciSeries$MAIN_LOOP_START
0;JMP
(FibonacciSeries$END_PROGRAM)
