@17
D=A
@SP
A=M
M=D
@SP
M=M+1
@17
D=A
@SP
A=M
M=D
@SP
M=M+1
@2
D=A
@SP
A=M-D
D=M
@SP
A=M-1
D=D-M
@EQUAL2
D;JEQ
@2
D=A
@SP
A=M-D
M=0
@ENDLOOP2
0;JMP
(EQUAL2)
@2
D=A
@SP
A=M-D
M=-1
(ENDLOOP2)
@SP
M=M-1
@17
D=A
@SP
A=M
M=D
@SP
M=M+1
@16
D=A
@SP
A=M
M=D
@SP
M=M+1
@2
D=A
@SP
A=M-D
D=M
@SP
A=M-1
D=D-M
@EQUAL5
D;JEQ
@2
D=A
@SP
A=M-D
M=0
@ENDLOOP5
0;JMP
(EQUAL5)
@2
D=A
@SP
A=M-D
M=-1
(ENDLOOP5)
@SP
M=M-1
@16
D=A
@SP
A=M
M=D
@SP
M=M+1
@17
D=A
@SP
A=M
M=D
@SP
M=M+1
@2
D=A
@SP
A=M-D
D=M
@SP
A=M-1
D=D-M
@EQUAL8
D;JEQ
@2
D=A
@SP
A=M-D
M=0
@ENDLOOP8
0;JMP
(EQUAL8)
@2
D=A
@SP
A=M-D
M=-1
(ENDLOOP8)
@SP
M=M-1
@892
D=A
@SP
A=M
M=D
@SP
M=M+1
@891
D=A
@SP
A=M
M=D
@SP
M=M+1
@2
D=A
@SP
A=M-D
D=M
@SP
A=M-1
D=D-M
@LTZERO11
D;JLT
@2
D=A
@SP
A=M-D
M=0
@ENDLOOP11
0;JMP
(LTZERO11)
@2
D=A
@SP
A=M-D
M=-1
(ENDLOOP11)
@SP
M=M-1
@891
D=A
@SP
A=M
M=D
@SP
M=M+1
@892
D=A
@SP
A=M
M=D
@SP
M=M+1
@2
D=A
@SP
A=M-D
D=M
@SP
A=M-1
D=D-M
@LTZERO14
D;JLT
@2
D=A
@SP
A=M-D
M=0
@ENDLOOP14
0;JMP
(LTZERO14)
@2
D=A
@SP
A=M-D
M=-1
(ENDLOOP14)
@SP
M=M-1
@891
D=A
@SP
A=M
M=D
@SP
M=M+1
@891
D=A
@SP
A=M
M=D
@SP
M=M+1
@2
D=A
@SP
A=M-D
D=M
@SP
A=M-1
D=D-M
@LTZERO17
D;JLT
@2
D=A
@SP
A=M-D
M=0
@ENDLOOP17
0;JMP
(LTZERO17)
@2
D=A
@SP
A=M-D
M=-1
(ENDLOOP17)
@SP
M=M-1
@32767
D=A
@SP
A=M
M=D
@SP
M=M+1
@32766
D=A
@SP
A=M
M=D
@SP
M=M+1
@2
D=A
@SP
A=M-D
D=M
@SP
A=M-1
D=D-M
@GTZERO20
D;JGT
@2
D=A
@SP
A=M-D
M=0
@ENDLOOP20
0;JMP
(GTZERO20)
@2
D=A
@SP
A=M-D
M=-1
(ENDLOOP20)
@SP
M=M-1
@32766
D=A
@SP
A=M
M=D
@SP
M=M+1
@32767
D=A
@SP
A=M
M=D
@SP
M=M+1
@2
D=A
@SP
A=M-D
D=M
@SP
A=M-1
D=D-M
@GTZERO23
D;JGT
@2
D=A
@SP
A=M-D
M=0
@ENDLOOP23
0;JMP
(GTZERO23)
@2
D=A
@SP
A=M-D
M=-1
(ENDLOOP23)
@SP
M=M-1
@32766
D=A
@SP
A=M
M=D
@SP
M=M+1
@32766
D=A
@SP
A=M
M=D
@SP
M=M+1
@2
D=A
@SP
A=M-D
D=M
@SP
A=M-1
D=D-M
@GTZERO26
D;JGT
@2
D=A
@SP
A=M-D
M=0
@ENDLOOP26
0;JMP
(GTZERO26)
@2
D=A
@SP
A=M-D
M=-1
(ENDLOOP26)
@SP
M=M-1
@57
D=A
@SP
A=M
M=D
@SP
M=M+1
@31
D=A
@SP
A=M
M=D
@SP
M=M+1
@53
D=A
@SP
A=M
M=D
@SP
M=M+1
@2
D=A
@SP
A=M-D
D=M
@SP
A=M-1
D=D+M
A=A-1
M=D
@SP
M=M-1
@112
D=A
@SP
A=M
M=D
@SP
M=M+1
@2
D=A
@SP
A=M-D
D=M
@SP
A=M-1
D=D-M
A=A-1
M=D
@SP
M=M-1
@SP
A=M-1
M=-M
@2
D=A
@SP
A=M-D
D=M
@SP
A=M-1
D=D&M
A=A-1
M=D
@SP
M=M-1
@82
D=A
@SP
A=M
M=D
@SP
M=M+1
@2
D=A
@SP
A=M-D
D=M
@SP
A=M-1
D=D|M
A=A-1
M=D
@SP
M=M-1
@SP
A=M-1
M=!M
