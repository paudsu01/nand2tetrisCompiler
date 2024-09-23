from __future__ import annotations
from scanner import Scanner
from jack_token import TokenType
from exceptions import KeywordExpectedException,\
        SymbolExpectedException,\
        SpecificKeywordExpectedException,\
        SpecificSymbolExpectedException

from typing import Tuple

class Parser:

    def __init__(self, scanner: Scanner):
        self.__scanner = scanner

    """ LEXICAL ELEMENTS """

    def compileKeyword(self, indent: int, specific_value_required=False, *specific_values: Tuple[str])->str:

        current_token = self.__scanner.current_token()

        if not (current_token.token_type is TokenType.KEYWORD):
            raise KeywordExpectedException(f'Keyword expected: got {current_token.value} instead')

        if specific_value_required and current_token.value not in specific_values:
            raise SpecificKeywordExpectedException(f'{specific_values} keyword(s) expected: got {current_token.value} keyword instead')

        xml = " " * indent + f"<keyword>{current_token.value}</keyword>\n"
        self.__scanner.advance()
        return xml

    def compileSymbol(self, indent: int, specific_value_required=False, *expected_values: Tuple[str])->str:
        current_token = self.__scanner.current_token()

        if not (current_token.token_type is TokenType.SYMBOL):
            raise SymbolExpectedException(f'Symbol expected: got {current_token.value} instead')

        if specific_value_required and current_token.value not in expected_values:
            raise SpecificSymbolExpectedException(f'{expected_values} symbol(s) expected: got {current_token.value} keyword instead')

        xml = " " * indent + f"<symbol>{current_token.value}</symbol>\n"
        self.__scanner.advance()
        return xml

    def compileIntegerConstant(self, indent : int)->str:
        current_token = self.__scanner.current_token()

        if not (current_token.token_type is TokenType.INTEGER_CONSTANT):
            raise SymbolExpectedException(f'IntegerConstant expected: got {current_token.value} instead')

        xml = ' ' * indent + f"<integerConstant>{current_token.value}</integerConstant>\n"
        self.__scanner.advance()
        return xml 

    def compileStringConstant(self, indent : int)->str:
        current_token = self.__scanner.current_token()

        if not (current_token.token_type is TokenType.STRING_CONSTANT):
            raise SymbolExpectedException(f'StringConstant expected: got {current_token.value} instead')

        xml = ' ' * indent + f"<stringConstant>{current_token.value}</stringConstant>\n"
        self.__scanner.advance()
        return xml

    def compileIdentifier(self, indent : int)->str:

        current_token = self.__scanner.current_token()

        if not (current_token.token_type is TokenType.IDENTIFIER):
            raise SymbolExpectedException(f'Identifier expected: got {current_token} instead')

        xml = ' ' * indent + f"<identifier>{current_token.value}</identifier>\n"
        self.__scanner.advance()
        return xml


    """ PROGRAM STRUCTURE GRAMMAR """

    def compileClass(self, indent=2)->str:
        xml = '<class>\n'
        xml += ' ' * indent + self.compileKeyword(indent+2, True, "class") +\
                ' ' * indent + self.compileIdentifier(indent+2) +\
                ' ' * indent + self.compileSymbol(indent+2, True, "{")

        current_token = self.__scanner.current_token()
        while current_token.value in ['static', 'field']:
            xml += ' ' * indent + self.compileClassVarDec(indent+2)
            current_token = self.__scanner.current_token(indent+2)

        current_token = self.__scanner.current_token()
        while current_token.value in ['constructor', 'function', 'method']:
            xml += ' ' * indent + self.compileSubroutine(indent+2)
            current_token = self.__scanner.current_token(indent+2)

        xml+= " " * indent + (self.compileSymbol(indent+2, True, '}'))
        xml+=('</class>')
        return xml

    def compileClassVarDec(self, indent : int)->str:
        xml = f'<classVarDec>\n  {self.compileKeyword(True, "class")}  {self.compileIdentifier()}  {self.compileSymbol(True, "{")}'

        current_token = self.__scanner.current_token()
        while current_token.value in ['static', 'field']:
            xml += f"  {self.compileClassVarDec()}"
            current_token = self.__scanner.current_token()

        current_token = self.__scanner.current_token()
        while current_token.value in ['constructor', 'function', 'method']:
            xml += f"  {self.compileSubroutine()}"
            current_token = self.__scanner.current_token()

        xml+= "  " + (self.compileSymbol(True, '}'))
        xml+=('</class>')
        return xml       

    def compileType(self, indent : int)->str:
        pass

    def compileSubroutine(self, indent : int)->str:
        return ""

    def compileParameterList(self, indent : int)->str:
        pass

    def compileVarDec(self, indent : int)->str:
        pass

    """ STATEMENTS GRAMMAR """ 

    def compileStatements(self, indent : int)->str:
        pass

    def compileDo(self, indent : int)->str:
        pass

    def compileLet(self, indent : int)->str:
        pass

    def compileWhile(self, indent : int)->str:
        pass

    def compileReturn(self, indent : int)->str:
        pass

    def compileIf(self, indent : int)->str:
        pass
    
    """ EXPRESSIONS GRAMMAR """

    def compileExpression(self, indent : int)->str:
        pass

    def compileTerm(self, indent : int)->str:
        pass

    def compileExpressionList(self, indent : int)->str:
        pass

    def compileOp(self, indent : int)->str:
        pass

    def compileUnaryOp(self, indent : int)->str:
        pass

    def compileKeywordConstant(self, indent : int)->str:
        pass
