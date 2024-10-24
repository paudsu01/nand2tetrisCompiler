from __future__ import annotations
from enum import Enum

import re

class Token:

    ## PRIVATE CLASS ATTRIBUTES ##

    __SYMBOLS = ['{','}','(',')','[',']','.',',',';','+','-',\
            '*','/','&','|','<','>','=','~']
    __KEYWORDS = ['class', 'constructor', 'function', 'method', 'field',\
                'static', 'var', 'int', 'char', 'boolean', 'void', 'true', 'false',\
                'null', 'this','let', 'do', 'if', 'else', 'while', 'return']
    
    ## Constructor ##

    def __init__(self, raw_code: str):

        if raw_code in self.__KEYWORDS:
            self.__token_type = TokenType.KEYWORD
            self.__value = raw_code

        elif raw_code in self.__SYMBOLS:
            self.__token_type = TokenType.SYMBOL
            self.__value = raw_code

        elif self.token_is_integer_constant(raw_code):
            self.__token_type = TokenType.INTEGER_CONSTANT
            self.__value = raw_code

        elif self.token_is_string_constant(raw_code):
            self.__token_type = TokenType.STRING_CONSTANT
            self.__value = raw_code[1:-1]

        else:
            self.__token_type = TokenType.IDENTIFIER
            self.__value = raw_code

    def token_is_string_constant(self, raw_value: str) -> bool:
        pattern1 = re.compile(r'^".*?"$')
        pattern2 = re.compile(r"^'.*?'$")
        return True if pattern1.match(raw_value) or pattern2.match(raw_value) else False

    def token_is_integer_constant(self, raw_value: str) -> bool:
        try:
            int(raw_value)
            return True
        except:
            return False

    ## CLASS PUBLIC GETTERS ##

    @classmethod
    @property
    def keywords(cls):
        return cls.__KEYWORDS

    @classmethod
    @property
    def symbols(cls):
        return cls.__SYMBOLS

    ## INSTANCE GETTERS ## 

    @property
    def token_type(self) -> TokenType:
        return self.__token_type

    @property
    def value(self) -> str:
        return self.__value

class TokenType(Enum):
     
    KEYWORD = 1
    SYMBOL = 2
    INTEGER_CONSTANT = 3
    STRING_CONSTANT = 4
    IDENTIFIER = 5
