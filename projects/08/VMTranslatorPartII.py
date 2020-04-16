import os

# Command Types
C_ARITHMETIC = 'C_ARITHMETIC'
C_PUSH = 'C_PUSH'
C_POP = 'C_POP'
C_LABEL = 'C_LABEL'
C_GOTO = 'C_GOTO'
C_IF = 'C_IF'
C_FUNCTION = 'C_FUNCTION'
C_RETURN = 'C_RETURN'
C_CALL = 'C_CALL'


class Parser:
    def __init__(self, vm_file):
        vm_file = open(vm_file, 'r')

        self.current_command = None

        self._command_counter = 0
        # Put all commands in a list while in the process, exclude empty lines
        # and comments.
        # Note: inline comments will be taken care of later
        self._commands = [
            line.rstrip() for line in vm_file if not line.startswith('//') and line != '\n']

    def has_more_commands(self):
        return self._command_counter < len(self._commands)

    def advance(self):
        if self.has_more_commands():
            self._set_current_command()
            self._command_counter += 1

    @property
    def command_type(self):
        if self.current_command:
            opcode = self.current_command.split()[0]

            command_types = {
                'add': C_ARITHMETIC,
                'sub': C_ARITHMETIC,
                'neg': C_ARITHMETIC,
                'eq': C_ARITHMETIC,
                'gt': C_ARITHMETIC,
                'lt': C_ARITHMETIC,
                'and': C_ARITHMETIC,
                'or': C_ARITHMETIC,
                'not': C_ARITHMETIC,
                'push': C_PUSH,
                'pop': C_POP,
                'label': C_LABEL,
                'goto': C_GOTO,
                'if-goto': C_IF,
                'function': C_FUNCTION,
                'return': C_RETURN,
                'call': C_CALL
            }

            return command_types.get(opcode, None)

    def _set_current_command(self):
        """
        Set the current command and remove inline comment if has
        """
        command = self._commands[self._command_counter]

        try:
            comment_index = command.index('//')
        except ValueError:
            self.current_command = command
            return

        self.current_command = command[:comment_index].rstrip()


class CodeWriter:
    def __init__(self, path, directory=False):
        if directory:
            directory_name = os.path.basename(path)
            if not directory_name:
                directory_name = path.split('/')[-2]
            self._asm_file = open(os.path.join(
                path, directory_name + '.asm'), 'w')
        else:
            # Indicated as file_name here is the full path without extension
            file_name = os.path.splitext(path)[0]
            self._asm_file = open(file_name + '.asm', 'w')

        self._outputfile_name = os.path.basename(
            self._asm_file.name).split('.')[0]

        self._current_function = None  # Function that the current command resides in
        self._symbol_counter = {
            'eq': 0,
            'gt': 0,
            'lt': 0,
            'popdata': 0,
            'local': 0
        }

        self._initialize()

    def _initialize(self):
        """
        Initialize stack pointer and call `Sys.init`
        """
        self._write_to_file('@256')
        self._write_to_file('D=A')
        self._write_to_file('@SP')
        self._write_to_file('M=D')
        self.write_call('Sys.init', 0)

    def write_arithmetic(self, command):
        opcode = command.split()[0]  # opcode of the command

        if opcode == 'add':
            self._write_add(command)

        if opcode == 'sub':
            self._write_sub(command)

        if opcode == 'neg':
            self._write_neg(command)

        if opcode in ['eq', 'gt', 'lt']:
            self._write_eq_gt_lt(command)

        if opcode == 'and':
            self._write_and(command)

        if opcode == 'or':
            self._write_or(command)

        if opcode == 'not':
            self._write_not(command)

    def write_push_pop(self, opcode, segment, index):
        if opcode == 'push':
            self._write_push(segment, index)

        if opcode == 'pop':
            self._write_pop(segment, index)

    def write_label(self, label_name):
        if self._current_function is not None:
            label_name = self._current_function + '$' + label_name
        else:
            label_name = self._outputfile_name + '$' + label_name

        self._write_to_file('({})'.format(label_name))

    def write_goto(self, label_name):
        if self._current_function is not None:
            label_name = self._current_function + '$' + label_name
        else:
            label_name = self._outputfile_name + '$' + label_name

        self._write_to_file('@{}'.format(label_name))
        self._write_to_file('0;JMP')

    def write_if_goto(self, label_name):
        if self._current_function is not None:
            label_name = self._current_function + '$' + label_name
        else:
            label_name = self._outputfile_name + '$' + label_name

        self._write_to_file('@SP')
        self._write_to_file('M=M-1')
        self._write_to_file('A=M')
        self._write_to_file('D=M')
        self._write_to_file('@{}'.format(label_name))
        self._write_to_file('D;JNE')

    def write_function(self, function_name, num_of_local_var):
        # Add function to the scope
        self._current_function = function_name

        self._write_to_file('({})'.format(function_name))

        # Set LCL pointer for the function
        self._write_to_file('@SP')
        self._write_to_file('D=M')
        self._write_to_file('@LCL')
        self._write_to_file('M=D')

        # Push 0 to the stack `num_of_local_var` times
        for _ in range(int(num_of_local_var)):
            self._write_to_file('@SP')
            self._write_to_file('A=M')
            self._write_to_file('M=0')
            self._write_to_file('@SP')
            self._write_to_file('M=M+1')

    def write_return(self):
        # endFrame = LCL
        self._write_to_file('@LCL')
        self._write_to_file('D=M')
        self._write_to_file('@endFrame')
        self._write_to_file('M=D')
        # retAddr = *(endFrame - 5)
        self._write_to_file('@5')
        self._write_to_file('D=A')
        self._write_to_file('@endFrame')
        self._write_to_file('A=M-D')
        self._write_to_file('D=M')
        self._write_to_file('@retAddr')
        self._write_to_file('M=D')
        # *ARG = pop()
        self._write_to_file('@SP')
        self._write_to_file('M=M-1')
        self._write_to_file('A=M')
        self._write_to_file('D=M')
        self._write_to_file('@ARG')
        self._write_to_file('A=M')
        self._write_to_file('M=D')
        # SP = ARG + 1
        self._write_to_file('@ARG')
        self._write_to_file('D=M')
        self._write_to_file('@SP')
        self._write_to_file('M=D+1')
        # THAT = *(endFrame - 1)
        self._write_to_file('@endFrame')
        self._write_to_file('A=M-1')
        self._write_to_file('D=M')
        self._write_to_file('@THAT')
        self._write_to_file('M=D')
        # THIS = *(endFrame - 2)
        self._write_to_file('@2')
        self._write_to_file('D=A')
        self._write_to_file('@endFrame')
        self._write_to_file('A=M-D')
        self._write_to_file('D=M')
        self._write_to_file('@THIS')
        self._write_to_file('M=D')
        # ARG = *(endFrame - 3)
        self._write_to_file('@3')
        self._write_to_file('D=A')
        self._write_to_file('@endFrame')
        self._write_to_file('A=M-D')
        self._write_to_file('D=M')
        self._write_to_file('@ARG')
        self._write_to_file('M=D')
        # LCL = *(endFrame - 4)
        self._write_to_file('@4')
        self._write_to_file('D=A')
        self._write_to_file('@endFrame')
        self._write_to_file('A=M-D')
        self._write_to_file('D=M')
        self._write_to_file('@LCL')
        self._write_to_file('M=D')
        # goto retAddr
        self._write_to_file('@retAddr')
        self._write_to_file('A=M')
        self._write_to_file('0;JMP')

    def write_call(self, function_name, num_of_arg_var):
        if self._current_function is not None:
            pre_label = self._current_function + '$ret.'
        else:
            pre_label = self._outputfile_name + '$ret.'
        counter = self._symbol_counter.setdefault(pre_label, 1)

        # Increment counter
        self._symbol_counter[pre_label] += 1

        # As return address
        label = pre_label + str(counter)

        # Push returnAddress
        self._write_to_file('@{}'.format(label))
        self._write_to_file('D=A')
        self._write_to_file('@SP')
        self._write_to_file('A=M')
        self._write_to_file('M=D')
        self._write_to_file('@SP')
        self._write_to_file('M=M+1')
        # Save the caller's states
        self._write_to_file('@LCL')
        self._write_to_file('D=M')
        self._write_to_file('@SP')
        self._write_to_file('A=M')
        self._write_to_file('M=D')
        self._write_to_file('@SP')
        self._write_to_file('M=M+1')
        self._write_to_file('@ARG')
        self._write_to_file('D=M')
        self._write_to_file('@SP')
        self._write_to_file('A=M')
        self._write_to_file('M=D')
        self._write_to_file('@SP')
        self._write_to_file('M=M+1')
        self._write_to_file('@THIS')
        self._write_to_file('D=M')
        self._write_to_file('@SP')
        self._write_to_file('A=M')
        self._write_to_file('M=D')
        self._write_to_file('@SP')
        self._write_to_file('M=M+1')
        self._write_to_file('@THAT')
        self._write_to_file('D=M')
        self._write_to_file('@SP')
        self._write_to_file('A=M')
        self._write_to_file('M=D')
        self._write_to_file('@SP')
        self._write_to_file('M=M+1')
        # Reposition ARG
        self._write_to_file('@{}'.format(5 + int(num_of_arg_var)))
        self._write_to_file('D=A')
        self._write_to_file('@SP')
        self._write_to_file('D=M-D')
        self._write_to_file('@ARG')
        self._write_to_file('M=D')
        # Reposition LCL
        self._write_to_file('@SP')
        self._write_to_file('D=M')
        self._write_to_file('@LCL')
        self._write_to_file('M=D')
        # Transfer control to the called function
        self._write_to_file('@{}'.format(function_name))
        self._write_to_file('0;JMP')
        # Declare returnAddress label
        self._write_to_file('({})'.format(label))

    def _write_add(self, command):
        self._write_to_file('@SP')
        self._write_to_file('M=M-1')
        self._write_to_file('A=M')
        self._write_to_file('D=M')
        self._write_to_file('@SP')
        self._write_to_file('M=M-1')
        self._write_to_file('A=M')
        self._write_to_file('M=D+M')
        self._write_to_file('@SP')
        self._write_to_file('M=M+1')

    def _write_sub(self, command):
        self._write_to_file('@SP')
        self._write_to_file('M=M-1')
        self._write_to_file('A=M')
        self._write_to_file('D=M')
        self._write_to_file('@SP')
        self._write_to_file('M=M-1')
        self._write_to_file('A=M')
        self._write_to_file('M=M-D')
        self._write_to_file('@SP')
        self._write_to_file('M=M+1')

    def _write_neg(self, command):
        self._write_to_file('@SP')
        self._write_to_file('M=M-1')
        self._write_to_file('A=M')
        self._write_to_file('M=-M')
        self._write_to_file('@SP')
        self._write_to_file('M=M+1')

    def _write_eq_gt_lt(self, command):
        label = command.upper()
        symbol_counter = self._symbol_counter[command]
        self._symbol_counter[command] += 1  # Increment

        if command == 'eq':
            conditional_command = 'D;JEQ'

        if command == 'gt':
            conditional_command = 'D;JGT'

        if command == 'lt':
            conditional_command = 'D;JLT'

        self._write_to_file('@SP')
        self._write_to_file('M=M-1')
        self._write_to_file('A=M')
        self._write_to_file('D=M')
        self._write_to_file('@SP')
        self._write_to_file('M=M-1')
        self._write_to_file('A=M')
        self._write_to_file('D=M-D')
        self._write_to_file('@{0}.TRUE.{1}'.format(label, symbol_counter))
        self._write_to_file(conditional_command)
        self._write_to_file('@SP')
        self._write_to_file('A=M')
        self._write_to_file('M=0')
        self._write_to_file('@{0}.SKIP.{1}'.format(label, symbol_counter))
        self._write_to_file('0;JMP')
        self._write_to_file('({0}.TRUE.{1})'.format(label, symbol_counter))
        self._write_to_file('@SP')
        self._write_to_file('A=M')
        self._write_to_file('M=-1')
        self._write_to_file('({0}.SKIP.{1})'.format(label, symbol_counter))
        self._write_to_file('@SP')
        self._write_to_file('M=M+1')

    def _write_and(self, command):
        self._write_to_file('@SP')
        self._write_to_file('M=M-1')
        self._write_to_file('A=M')
        self._write_to_file('D=M')
        self._write_to_file('@SP')
        self._write_to_file('M=M-1')
        self._write_to_file('A=M')
        self._write_to_file('M=D&M')
        self._write_to_file('@SP')
        self._write_to_file('M=M+1')

    def _write_or(self, command):
        self._write_to_file('@SP')
        self._write_to_file('M=M-1')
        self._write_to_file('A=M')
        self._write_to_file('D=M')
        self._write_to_file('@SP')
        self._write_to_file('M=M-1')
        self._write_to_file('A=M')
        self._write_to_file('M=D|M')
        self._write_to_file('@SP')
        self._write_to_file('M=M+1')

    def _write_not(self, command):
        self._write_to_file('@SP')
        self._write_to_file('M=M-1')
        self._write_to_file('A=M')
        self._write_to_file('M=!M')
        self._write_to_file('@SP')
        self._write_to_file('M=M+1')

    def _write_push(self, segment, index):
        if segment == 'constant':
            self._write_to_file('@{}'.format(index))
            self._write_to_file('D=A')
            self._write_to_file('@SP')
            self._write_to_file('A=M')
            self._write_to_file('M=D')
            self._write_to_file('@SP')
            self._write_to_file('M=M+1')

        if segment == 'temp':
            self._write_push_temp(index)

        if segment == 'pointer':
            self._write_push_pointer(index)

        if segment == 'static':
            self._write_push_static(index)

        if segment in ['local', 'argument', 'this', 'that']:
            self._write_push_local_arg_this_that(segment, index)

    def _write_push_temp(self, index):
        self._write_to_file('@{}'.format(5 + int(index)))
        self._write_to_file('D=M')
        self._write_to_file('@SP')
        self._write_to_file('A=M')
        self._write_to_file('M=D')
        self._write_to_file('@SP')
        self._write_to_file('M=M+1')

    def _write_push_pointer(self, index):
        if index not in ['0', '1']:
            raise ValueError(
                '"push pointer" with index {} is invalid'.format(index))

        if index == '0':
            label = 'THIS'
        else:
            label = 'THAT'

        self._write_to_file('@{}'.format(label))
        self._write_to_file('D=M')
        self._write_to_file('@SP')
        self._write_to_file('A=M')
        self._write_to_file('M=D')
        self._write_to_file('@SP')
        self._write_to_file('M=M+1')

    def _write_push_static(self, index):
        current_class = self._current_function.split('.')[0]

        self._write_to_file('@{0}.{1}'.format(current_class, index))
        self._write_to_file('D=M')
        self._write_to_file('@SP')
        self._write_to_file('A=M')
        self._write_to_file('M=D')
        self._write_to_file('@SP')
        self._write_to_file('M=M+1')

    def _write_push_local_arg_this_that(self, segment, index):
        if segment == 'local':
            segment_pointer = 'LCL'

        if segment == 'argument':
            segment_pointer = 'ARG'

        if segment == 'this':
            segment_pointer = 'THIS'

        if segment == 'that':
            segment_pointer = 'THAT'

        self._write_to_file('@{}'.format(index))
        self._write_to_file('D=A')
        self._write_to_file('@{}'.format(segment_pointer))
        self._write_to_file('A=D+M')
        self._write_to_file('D=M')
        self._write_to_file('@SP')
        self._write_to_file('A=M')
        self._write_to_file('M=D')
        self._write_to_file('@SP')
        self._write_to_file('M=M+1')

    def _write_pop(self, segment, index):
        if segment == 'temp':
            self._write_pop_temp(index)

        if segment == 'pointer':
            self._write_pop_pointer(index)

        if segment == 'static':
            self._write_pop_static(index)

        if segment in ['local', 'argument', 'this', 'that']:
            self._write_pop_local_arg_this_that(segment, index)

    def _write_pop_temp(self, index):
        self._write_to_file('@SP')
        self._write_to_file('M=M-1')
        self._write_to_file('A=M')
        self._write_to_file('D=M')
        self._write_to_file('@{}'.format(5 + int(index)))
        self._write_to_file('M=D')

    def _write_pop_pointer(self, index):
        if index not in ['0', '1']:
            raise ValueError(
                '"pop pointer" with index {} is invalid'.format(index))

        if index == '0':
            label = 'THIS'
        else:
            label = 'THAT'

        self._write_to_file('@SP')
        self._write_to_file('M=M-1')
        self._write_to_file('A=M')
        self._write_to_file('D=M')
        self._write_to_file('@{}'.format(label))
        self._write_to_file('M=D')

    def _write_pop_static(self, index):
        current_class = self._current_function.split('.')[0]

        self._write_to_file('@SP')
        self._write_to_file('M=M-1')
        self._write_to_file('A=M')
        self._write_to_file('D=M')
        self._write_to_file('@{0}.{1}'.format(current_class, index))
        self._write_to_file('M=D')

    def _write_pop_local_arg_this_that(self, segment, index):
        # Use symbol counter as id for assembly symbols
        popdata_symbol_counter = self._symbol_counter['popdata']
        local_symbol_counter = self._symbol_counter['local']
        self._symbol_counter['popdata'] += 1
        self._symbol_counter['local'] += 1

        if segment == 'local':
            segment_pointer = 'LCL'

        if segment == 'argument':
            segment_pointer = 'ARG'

        if segment == 'this':
            segment_pointer = 'THIS'

        if segment == 'that':
            segment_pointer = 'THAT'

        self._write_to_file('@SP')
        self._write_to_file('M=M-1')
        self._write_to_file('A=M')
        self._write_to_file('D=M')
        self._write_to_file('@popdata{}'.format(popdata_symbol_counter))
        self._write_to_file('M=D')
        self._write_to_file('@{}'.format(index))
        self._write_to_file('D=A')
        self._write_to_file('@{}'.format(segment_pointer))
        self._write_to_file('D=D+M')
        self._write_to_file('@{0}.{1}'.format(segment, local_symbol_counter))
        self._write_to_file('M=D')
        self._write_to_file('@popdata{}'.format(popdata_symbol_counter))
        self._write_to_file('D=M')
        self._write_to_file('@{0}.{1}'.format(segment, local_symbol_counter))
        self._write_to_file('A=M')
        self._write_to_file('M=D')

    def _write_to_file(self, asm_command):
        self._asm_file.write(asm_command + '\n')

    def close(self):
        """
        Close the asm file for completion
        """
        self._asm_file.close()


def main():
    import sys

    def translate(vm_file, writer):
        # Extension check
        assert vm_file.endswith('.vm')

        parser = Parser(vm_file)
        while parser.has_more_commands():
            parser.advance()

            command = parser.current_command
            command_type = parser.command_type

            if command_type is None:
                raise ValueError('"{}" is an invalid command.'.format(command))

            if command_type == C_ARITHMETIC:
                writer.write_arithmetic(command)

            if command_type in [C_PUSH, C_POP]:
                opcode, segment, index = command.split()

                writer.write_push_pop(opcode, segment, index)

            if command_type == C_LABEL:
                label_name = command.split()[1]

                writer.write_label(label_name)

            if command_type == C_GOTO:
                label_name = command.split()[1]

                writer.write_goto(label_name)

            if command_type == C_IF:
                label_name = command.split()[1]

                writer.write_if_goto(label_name)

            if command_type == C_FUNCTION:
                function_name, num_of_local_var = command.split()[1:]

                writer.write_function(function_name, num_of_local_var)

            if command_type == C_RETURN:
                writer.write_return()

            if command_type == C_CALL:
                function_name, num_of_arg_var = command.split()[1:]

                writer.write_call(function_name, num_of_arg_var)

    for path in sys.argv[1:]:
        if not os.path.exists(path):
            raise ValueError(
                '"{}" file or directory doesn\'t exit.'.format(path))

        if os.path.isdir(path):
            # initialize an .asm output file
            code_writer = CodeWriter(path, directory=True)

            # go into the directory, iterate over each `.vm` file
            vm_files = [filename for filename in os.listdir(
                path) if filename.endswith('.vm')]

            # join the directory path with filename
            # for example, 'foo' turns to '/bar/foo' when 'bar' is the directory
            for vm_file in [os.path.join(path, filename) for filename in vm_files]:
                translate(vm_file, code_writer)

            # Finish by properly closing the output file
            code_writer.close()

        elif os.path.isfile(path):
            code_writer = CodeWriter(path, directory=False)

            translate(path, code_writer)

            # Finish by properly closing the output file
            code_writer.close()


if __name__ == '__main__':
    main()
