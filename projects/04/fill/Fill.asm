// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Put your code here.
@8192
D=A
@n
M=D // (256 rows * 512 columns == 131072 pixels). And each register stores 16 pixels, so 8192 register.

(LOOP)

    @i
    M=0 // counter
    @SCREEN
    D=A
    @addr
    M=D // save the base address of the screen memory map to a variable for future use

    @KBD
    D=M
    @BLACK
    D;JNE // if RAM[KDB] is not equal zero, turn all pixels to black

    @WHITE // else turn all to white instead
    0;JMP

(BLACK)
    @n
    D=M
    @i
    D=D-M // n - i
    @LOOP
    D;JEQ // if all pixels are black, go back to the first loop

    @addr
    A=M
    M=-1

    @addr
    M=M+1 // addr = addr + 1

    @i
    M=M+1 // i = i + 1

    @BLACK
    0;JMP

(WHITE)
    @n
    D=M
    @i
    D=D-M // n - i
    @LOOP
    D;JEQ // if all pixels are white, go back to the first loop

    @addr
    A=M
    M=0

    @addr
    M=M+1 // addr = addr + 1

    @i
    M=M+1 // i = i + 1

    @WHITE
    0;JMP
