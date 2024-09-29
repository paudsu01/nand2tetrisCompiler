from __future__ import annotations

class VM_writer:

    __operand_to_command_mapping = {
            '+':'add',
            '-':'sub',
            '*': 'call Math.multiply 2',
            '/': 'call Math.divide 2',
            '&': 'and',
            '|': 'or',
            '<': 'lt',
            '>': 'gt',
            '=': 'eq',
    }

    def __init__(self, filename: str):
        self.__filename = filename
        self.__output_file = open(f'{filename}.vm', 'w')

    def write_push(self, memorySegment: str, index: int) -> None:
        self.__output_file.write(f'\tpush {memorySegment} {index}\n')

    def write_pop(self, memorySegment: str, index: int) -> None:
        self.__output_file.write(f'\tpop {memorySegment} {index}\n')

    def write_arithmetic(self, command : str) -> None:
        self.__output_file.write(f'\t{self.__operand_to_command_mapping[command]}\n')

    def write_label(self, label:str) -> None:
        self.__output_file.write(f'label {label}\n')

    def write_goto(self, label: str) -> None:
        self.__output_file.write(f'\tgoto {label}\n')

    def write_if(self, label: str) -> None:
        self.__output_file.write(f'\tif-goto {label}\n')

    def write_function(self, func_name: str, nlocals: int) -> None:
        self.__output_file.write(f'function {func_name} {nlocals}\n')

    def write_call(self, func_name: str, nargs: int) -> None:
        self.__output_file.write(f'\tcall {func_name} {nargs}\n')

    def write_return(self)-> None:
        self.__output_file.write('\treturn\n')

    def close(self) -> None:
        self.__output_file.close()
