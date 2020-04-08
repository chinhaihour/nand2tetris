# Command Types
C_ARITHMETIC = 'C_ARITHMETIC'
C_PUSH = 'C_PUSH'
C_POP = 'C_POP'
C_LABEL = 'C_GOTO'
C_IF = 'C_IF'
C_FUNCTION = 'C_FUNCTION'
C_RETURN = 'C_RETURN'
C_CALL = 'C_CALL'


class Parser:
    def __init__(self, filepath):

        # Check the extension of the input file
        self._check_file_extension(filepath)

        vm_file = open(filepath, 'r')
        # Ignore whitespaces and comments
        self._lines = [
            line.strip() for line in vm_file if not line.startswith('//') and line.strip() != '']

        self._current_command = None
        self._index = -1

    def has_more_commands(self):
        return len(self._lines) != 0 and len(self._lines) - 1 > self._index

    def advance(self):
        '''Move to the next command'''
        self._index += 1
        self._current_command = self._lines[self._index]

    @property
    def current_command(self):
        return self._current_command

    @property
    def command_type(self):
        # TODO: make sure the command exists in the specification
        command_split = self._current_command.split()

        if len(command_split) == 3:
            return C_PUSH if command_split[0] == 'push' else C_POP
        elif len(command_split) == 1:
            return C_ARITHMETIC

    @property
    def command_opcode(self):
        if self.command_type == C_POP or self.command_type == C_PUSH:
            return self._current_command.split()[0]

    @property
    def arg1(self):
        if self.command_type == C_POP or self.command_type == C_PUSH:
            return self._current_command.split()[1]

    @property
    def arg2(self):
        if self.command_type == C_POP or self.command_type == C_PUSH:
            return self._current_command.split()[2]

    def _check_file_extension(self, filepath):
        try:
            filename, extension = filepath.split('.')
            if extension != 'vm':
                raise ValueError
        except ValueError:
            raise ValueError('File must have .vm extension')


class CodeWriter:
    def __init__(self, filepath):
        self.filename = filepath.split('/')[-1]

        self._output_file = open(filepath + '.asm', 'w')
        # Will use this for concatenation to make ids for some commands' symbols.
        # Avoid using the same symbol. For example, all `eq` commands would
        # the same symbol EQUAL. And all following jump calls will jump to first declaration.
        self._commands_written = 0

    def write_arithmetic(self, command):
        command_mapper = {
            'add': '@2\nD=A\n@SP\nA=M-D\nD=M\n@SP\nA=M-1\nD=D+M\nA=A-1\nM=D\n@SP\nM=M-1\n',
            'sub': '@2\nD=A\n@SP\nA=M-D\nD=M\n@SP\nA=M-1\nD=D-M\nA=A-1\nM=D\n@SP\nM=M-1\n',
            'neg': '@SP\nA=M-1\nM=-M\n',

            'eq': '@2\nD=A\n@SP\nA=M-D\nD=M\n@SP\nA=M-1\nD=D-M\n@EQUAL{0}\nD;JEQ\n@2\nD=A\n'
            '@SP\nA=M-D\nM=0\n@ENDLOOP{0}\n0;JMP\n(EQUAL{0})\n@2\nD=A\n@SP\nA=M-D\nM=-1\n(ENDLOOP{0})\n@SP\nM=M-1\n'.format(
                self._commands_written),

            'gt': '@2\nD=A\n@SP\nA=M-D\nD=M\n@SP\nA=M-1\nD=D-M\n@GTZERO{0}\nD;JGT\n@2\nD=A\n'
            '@SP\nA=M-D\nM=0\n@ENDLOOP{0}\n0;JMP\n(GTZERO{0})\n@2\nD=A\n@SP\nA=M-D\nM=-1\n(ENDLOOP{0})\n@SP\nM=M-1\n'.format(
                self._commands_written),

            'lt': '@2\nD=A\n@SP\nA=M-D\nD=M\n@SP\nA=M-1\nD=D-M\n@LTZERO{0}\nD;JLT\n@2\nD=A\n'
            '@SP\nA=M-D\nM=0\n@ENDLOOP{0}\n0;JMP\n(LTZERO{0})\n@2\nD=A\n@SP\nA=M-D\nM=-1\n(ENDLOOP{0})\n@SP\nM=M-1\n'.format(
                self._commands_written),

            'and': '@2\nD=A\n@SP\nA=M-D\nD=M\n@SP\nA=M-1\nD=D&M\nA=A-1\nM=D\n@SP\nM=M-1\n',
            'or': '@2\nD=A\n@SP\nA=M-D\nD=M\n@SP\nA=M-1\nD=D|M\nA=A-1\nM=D\n@SP\nM=M-1\n',
            'not': '@SP\nA=M-1\nM=!M\n'
        }

        asm_command = command_mapper[command]
        self._write(asm_command)

    def write_push_pop(self, command_opcode, segment, index):
        # All the segments are: local, argument, this, that, constant, static, pointer, temp
        # And these can be called as pointers. We group them together for convenience..
        single_segment_pointer_mapper = {
            'local': 'LCL',
            'argument': 'ARG',
            'this': 'THIS',
            'that': 'THAT'
        }
        segment_pointer = single_segment_pointer_mapper.get(segment, None)

        # This is the actual base address of the temp segment
        temp_base_addr = 5

        # Note: there is no `pop constant` command
        if command_opcode == 'pop':
            if segment == 'static':
                self._write(
                    '@SP\nA=M-1\nD=M\n@{0}\nM=D\n@SP\nM=M-1\n'.format(self.filename + '.' + str(index)))
            elif segment == 'temp':
                self._write(
                    '@SP\nA=M-1\nD=M\n@{0}\nM=D\n@SP\nM=M-1\n'.format(temp_base_addr + index))
            elif segment == 'pointer':
                if index == 0:
                    self._write('@SP\nA=M-1\nD=M\n@THIS\nM=D\n@SP\nM=M-1\n')
                else:
                    self._write('@SP\nA=M-1\nD=M\n@THAT\nM=D\n@SP\nM=M-1\n')
            else:
                self._write(
                    '@SP\nA=M-1\nD=M\n@popdata{0}\nM=D\n@{1}\nD=A\n@{2}\nD=D+M\n@popto{0}\nM=D\n@popdata{0}\nD=M\n@popto{0}\nA=M\nM=D\n@SP\nM=M-1\n'.format(self._commands_written, index, segment_pointer))
        elif command_opcode == 'push':
            if segment == 'static':
                self._write(
                    '@{0}\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n'.format(self.filename + '.' + str(index)))
            elif segment == 'constant':
                self._write(
                    '@{}\nD=A\n@SP\nA=M\nM=D\n@SP\nM=M+1\n'.format(index))
            elif segment == 'temp':
                self._write(
                    '@{0}\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n'.format(temp_base_addr + index))
            elif segment == 'pointer':
                if index == 0:
                    self._write('@THIS\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n')
                else:
                    self._write('@THAT\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n')
            else:
                self._write(
                    '@{}\nD=A\n@{}\nA=D+M\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n'.format(index, segment_pointer))

    def _write(self, asm_command):
        self._output_file.write(asm_command)
        self._commands_written += 1

    def close(self):
        '''Close the output file'''
        self._output_file.close()


def main():
    import sys

    for filepath in sys.argv[1:]:
        parser = Parser(filepath)
        code_writer = CodeWriter(filepath.split('.')[0])

        while parser.has_more_commands():
            # Move to the next command
            parser.advance()

            command = parser.current_command
            command_type = parser.command_type

            if command_type == C_ARITHMETIC:
                code_writer.write_arithmetic(command)
            elif command_type == C_POP or command_type == C_PUSH:
                command_opcode = parser.command_opcode
                memory_segment = parser.arg1
                index = int(parser.arg2)

                code_writer.write_push_pop(
                    command_opcode, memory_segment, index)

        code_writer.close()


if __name__ == '__main__':
    main()
