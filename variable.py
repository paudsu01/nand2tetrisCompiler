from enum import Enum

class VariableType(Enum):
    
    static = 0
    field = 1
    local = 2
    argument = 3
    none = 4

class Variable:

    var_type_to_enum = {
        'static': VariableType.static,
         'field': VariableType.field,
         'var': VariableType.local,
         'arg': VariableType.argument
            }

    def __init__(self, identifier: str, var_type: str, class_name: str):
        self.__identifier = identifier
        self.__var_type = self.var_type_to_enum[var_type]
        self.__class_name = class_name

    @property
    def class_name(self) -> int:
        return self.__class_name

    @property
    def identifier(self) -> int:
        return self.__identifier

    @property
    def type(self) -> VariableType:
        return self.__var_type

    @property
    def memory_segment(self) -> str:
        memorySegment = self.type.name
        if memorySegment == 'field': 
            memorySegment = 'this'
        return memorySegment

    @property
    def index(self) -> int:
        return self.__index

    @index.setter
    def index(self, new_index: int) -> None:
        self.__index = new_index
