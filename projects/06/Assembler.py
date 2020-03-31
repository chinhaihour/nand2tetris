class ArgumentError(BaseException):
    pass


class Parser:
    def __init__(self, file):
        self.A_COMMAND = 'A_COMMAND'
        self.C_COMMAND = 'C_COMMAND'
        self.L_COMMAND = 'L_COMMAND'

        filename, extension = file.split('.')
        if extension != 'asm':
            raise ArgumentError('File should have .asm extension')

        # Initialization: add all predefined symbols
        symbol_table = SymbolTable()
        symbol_table.add_entry('SP', 0)
        symbol_table.add_entry('LCL', 1)
        symbol_table.add_entry('ARG', 2)
        symbol_table.add_entry('THIS', 3)
        symbol_table.add_entry('THAT', 4)
        symbol_table.add_entry('R0', 0)
        symbol_table.add_entry('R1', 1)
        symbol_table.add_entry('R2', 2)
        symbol_table.add_entry('R3', 3)
        symbol_table.add_entry('R4', 4)
        symbol_table.add_entry('R5', 5)
        symbol_table.add_entry('R6', 6)
        symbol_table.add_entry('R7', 7)
        symbol_table.add_entry('R8', 8)
        symbol_table.add_entry('R9', 9)
        symbol_table.add_entry('R10', 10)
        symbol_table.add_entry('R11', 11)
        symbol_table.add_entry('R12', 12)
        symbol_table.add_entry('R13', 13)
        symbol_table.add_entry('R14', 14)
        symbol_table.add_entry('R15', 15)
        symbol_table.add_entry('SCREEN', 16384)
        symbol_table.add_entry('KBD', 24576)

        # First Phase: searching for label symbols and adding them to the symbol table
        with open(file, 'r') as asm_file:
            rom_counter = 0

            for line in asm_file:
                line = line.strip()

                # Ignore comments and empty lines
                if line.startswith('//') or line == '':
                    continue

                # Ignore inline comments
                if '//' in line:
                    comment_index = line.index('//')
                    line = line[:comment_index]
                    line = line.strip()

                self.command = line

                if self.command_type() == self.L_COMMAND:
                    symbol_table.add_entry(self.symbol(), rom_counter)
                    continue  # Don't increment the ROM counter when encounter a label

                rom_counter += 1

        # Second Phase: adding variable symbols to the symbol table and actual translation
        with open(filename + '.hack', 'w') as hack_file:
            with open(file, 'r') as asm_file:
                symbol_ram_address_counter = 16

                for line in asm_file:
                    line = line.strip()

                    # Ignore comments and empty lines
                    if line.startswith('//') or line == '':
                        continue

                    # Ignore inline comments
                    if '//' in line:
                        comment_index = line.index('//')
                        line = line[:comment_index]
                        line = line.strip()

                    self.command = line

                    if self.command_type() == self.A_COMMAND:
                        ram_address = 0

                        if self.symbol():
                            symbol = self.symbol()
                            if symbol_table.contains(symbol):
                                ram_address = symbol_table.get_address(symbol)
                            else:
                                ram_address = symbol_ram_address_counter
                                symbol_table.add_entry(symbol, ram_address)
                                symbol_ram_address_counter += 1
                        else:
                            ram_address = int(self.command[1:])

                        hack_file.write(
                            '0' + '{0:015b}'.format(ram_address) + '\n')
                    if self.command_type() == self.C_COMMAND:
                        c = self.comp()
                        d = self.dest()
                        j = self.jump()

                        cc = Code.comp(c)
                        dd = Code.dest(d)
                        jj = Code.jump(j)

                        # C instructions always start with 111 bits
                        hack_file.write('111' + cc + dd + jj + '\n')

        # for key, value in symbol_table.table.items():
        #     print('symbol: ' + key + ', address: ' + str(value))

    def command_type(self):
        if self.command[0] == '@':
            return self.A_COMMAND
        elif self.command[0] == '(' and self.command[-1] == ')':
            return self.L_COMMAND
        else:
            return self.C_COMMAND

    def symbol(self):
        if self.command_type() == self.A_COMMAND:
            if not self.command[1:].isdigit():
                return self.command[1:]

        if self.command_type() == self.L_COMMAND:
            return self.command[1:-1]

    def dest(self):
        if self.command_type() == self.C_COMMAND:
            if '=' not in self.command:
                return ''

            equal_sign_index = self.command.index('=')
            return self.command[:equal_sign_index]

    def comp(self):
        if self.command_type() == self.C_COMMAND:
            if '=' in self.command and ';' in self.command:
                equal_sign_index = self.command.index('=')
                semi_colon_index = self.command.index(';')
                return self.command[equal_sign_index+1:semi_colon_index]
            elif '=' not in self.command:
                semi_colon_index = self.command.index(';')
                return self.command[:semi_colon_index]
            else:
                equal_sign_index = self.command.index('=')
                return self.command[equal_sign_index+1:]

    def jump(self):
        if self.command_type() == self.C_COMMAND:
            if ';' not in self.command:
                return ''

            semi_colon_index = self.command.index(';')
            return self.command[semi_colon_index+1:]


class Code:

    @staticmethod
    def dest(mnemonic):
        binary_str = ''

        if 'A' in mnemonic:
            binary_str += '1'
        else:
            binary_str += '0'

        if 'D' in mnemonic:
            binary_str += '1'
        else:
            binary_str += '0'

        if 'M' in mnemonic:
            binary_str += '1'
        else:
            binary_str += '0'

        return binary_str

    @staticmethod
    def comp(mnemonic):
        binary_str = ''

        if mnemonic == '0':
            binary_str = '0101010'

        if mnemonic == '1':
            binary_str = '0111111'

        if mnemonic == '-1':
            binary_str = '0111010'

        if mnemonic == 'D':
            binary_str = '0001100'

        if mnemonic == 'A':
            binary_str = '0110000'

        if mnemonic == 'M':
            binary_str = '1110000'

        if mnemonic == '!D':
            binary_str = '0001101'

        if mnemonic[0] == '!':
            if mnemonic[1] == 'A':
                binary_str = '0110001'
            if mnemonic[1] == 'M':
                binary_str = '1110001'

        if mnemonic == '-D':
            binary_str = '0001111'

        if mnemonic[0] == '-':
            if mnemonic[1] == 'A':
                binary_str = '0110011'
            if mnemonic[1] == 'M':
                binary_str = '1110011'

        if mnemonic == 'D+1':
            binary_str = '0011111'

        if mnemonic[1:3] == '+1':
            if mnemonic[0] == 'A':
                binary_str = '0110111'
            if mnemonic[0] == 'M':
                binary_str = '1110111'

        if mnemonic == 'D-1':
            binary_str = '0001110'

        if mnemonic[1:3] == '-1':
            if mnemonic[0] == 'A':
                binary_str = '0110010'
            if mnemonic[0] == 'M':
                binary_str = '1110010'

        if mnemonic[0:2] == 'D+':
            if mnemonic[2] == 'A':
                binary_str = '0000010'
            if mnemonic[2] == 'M':
                binary_str = '1000010'

        if mnemonic[0:2] == 'D-':
            if mnemonic[2] == 'A':
                binary_str = '0010011'
            if mnemonic[2] == 'M':
                binary_str = '1010011'

        if mnemonic[1:3] == '-D':
            if mnemonic[0] == 'A':
                binary_str = '0000111'
            if mnemonic[0] == 'M':
                binary_str = '1000111'

        if mnemonic[0:2] == 'D&':
            if mnemonic[2] == 'A':
                binary_str = '0000000'
            if mnemonic[2] == 'M':
                binary_str = '1000000'

        if mnemonic[0:2] == 'D|':
            if mnemonic[2] == 'A':
                binary_str = '0010101'
            if mnemonic[2] == 'M':
                binary_str = '1010101'

        return binary_str

    @staticmethod
    def jump(mnemonic):
        jump_dict = {'JGT': '001',
                     'JEQ': '010',
                     'JGE': '011',
                     'JLT': '100',
                     'JNE': '101',
                     'JLE': '110',
                     'JMP': '111'}

        # 000 corresponds to null
        return jump_dict.get(mnemonic, '000')


class SymbolTable:
    def __init__(self):
        self.table = dict()

    def add_entry(self, symbol, address):
        self.table[symbol] = address

    def contains(self, symbol):
        return symbol in self.table

    def get_address(self, symbol):
        return self.table[symbol]


if __name__ == '__main__':
    import sys

    for arg in sys.argv[1:]:
        Parser(arg)
