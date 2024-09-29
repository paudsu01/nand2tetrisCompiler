from __future__ import annotations
from typing import Union
from variable import Variable, VariableType

class SymbolTable:

    __STATIC_COUNTER = 0
    __FIELD_COUNTER = 0
    __ARGUMENT_COUNTER = 0
    __LOCAL_COUNTER = 0

    __IDENTIFIER_TO_VAR_CLASS_MAPPING = {}
    __IDENTIFIER_TO_VAR_SUBROUTINE_MAPPING = {}

    @classmethod
    def get_variable(cls, identifier: str) -> Union[Variable, None]:
        if identifier in cls.__IDENTIFIER_TO_VAR_SUBROUTINE_MAPPING:
            return cls.__IDENTIFIER_TO_VAR_SUBROUTINE_MAPPING[identifier]
        else:
            return cls.__IDENTIFIER_TO_VAR_CLASS_MAPPING.get(identifier)

    @classmethod
    def contains(cls, identifier: str) -> True:
        return True if (identifier in cls.__IDENTIFIER_TO_VAR_SUBROUTINE_MAPPING \
                or identifier in cls.__IDENTIFIER_TO_VAR_CLASS_MAPPING) else False

    @classmethod
    def add(cls, identifier: str, var_type: str, class_name: str) -> None:
        variable = Variable(identifier, var_type, class_name)

        if variable.type is VariableType.static:
            variable.index = cls.__STATIC_COUNTER
            cls.__STATIC_COUNTER += 1
            cls.__IDENTIFIER_TO_VAR_CLASS_MAPPING[identifier] = variable

        elif variable.type is VariableType.field:
            variable.index = cls.__FIELD_COUNTER
            cls.__FIELD_COUNTER += 1
            cls.__IDENTIFIER_TO_VAR_CLASS_MAPPING[identifier] = variable

        elif variable.type is VariableType.local:
            variable.index = cls.__LOCAL_COUNTER
            cls.__LOCAL_COUNTER += 1
            cls.__IDENTIFIER_TO_VAR_SUBROUTINE_MAPPING[identifier] = variable

        elif variable.type is VariableType.argument:
            variable.index = cls.__ARGUMENT_COUNTER
            cls.__ARGUMENT_COUNTER += 1
            cls.__IDENTIFIER_TO_VAR_SUBROUTINE_MAPPING[identifier] = variable

    @classmethod
    def reset_subroutine_table(cls):
        cls.__ARGUMENT_COUNTER = 0
        cls.__LOCAL_COUNTER = 0
        cls.__IDENTIFIER_TO_VAR_SUBROUTINE_MAPPING = {}

    @classmethod
    def reset_class_table(cls):
        cls.reset_subroutine_table()
        cls.__FIELD_COUNTER = 0
        cls.__IDENTIFIER_TO_VAR_CLASS_MAPPING = {}
    
    # Necessary for object methods
    @classmethod
    def set_argument_counter_to_one(cls):
        cls.__ARGUMENT_COUNTER = 1

    @classmethod
    def get_total_fields(cls):
        return cls.__FIELD_COUNTER

    @classmethod
    def get_total_locals(cls):
        return cls.__LOCAL_COUNTER
