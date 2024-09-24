from __future__ import annotations
from scanner import Scanner
from jack_token import TokenType
from exceptions import KeywordExpectedException,\
        SymbolExpectedException,\
        IdentifierExpectedException,\
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
        if self.__scanner.has_more_tokens(): self.__scanner.advance()
        return xml

    def compileSymbol(self, indent: int, specific_value_required=False, *expected_values: Tuple[str])->str:
        current_token = self.__scanner.current_token()

        if not (current_token.token_type is TokenType.SYMBOL):
            raise SymbolExpectedException(f'Symbol expected: got {current_token.value} instead')

        if specific_value_required and current_token.value not in expected_values:
            raise SpecificSymbolExpectedException(f'{expected_values} symbol(s) expected: got {current_token.value} keyword instead')

        xml = " " * indent + f"<symbol>{current_token.value}</symbol>\n"
        if self.__scanner.has_more_tokens(): self.__scanner.advance()
        return xml

    def compileIntegerConstant(self, indent : int)->str:
        current_token = self.__scanner.current_token()

        if not (current_token.token_type is TokenType.INTEGER_CONSTANT):
            raise SymbolExpectedException(f'IntegerConstant expected: got {current_token.value} instead')

        xml = ' ' * indent + f"<integerConstant>{current_token.value}</integerConstant>\n"
        if self.__scanner.has_more_tokens(): self.__scanner.advance()
        return xml 

    def compileStringConstant(self, indent : int)->str:
        current_token = self.__scanner.current_token()

        if not (current_token.token_type is TokenType.STRING_CONSTANT):
            raise SymbolExpectedException(f'StringConstant expected: got {current_token.value} instead')

        xml = ' ' * indent + f"<stringConstant>{current_token.value}</stringConstant>\n"
        if self.__scanner.has_more_tokens(): self.__scanner.advance()
        return xml

    def compileIdentifier(self, indent : int)->str:

        current_token = self.__scanner.current_token()

        if not (current_token.token_type is TokenType.IDENTIFIER):
            raise IdentifierExpectedException(f'Identifier expected: got {current_token.value} instead')

        xml = ' ' * indent + f"<identifier>{current_token.value}</identifier>\n"
        if self.__scanner.has_more_tokens(): self.__scanner.advance()
        return xml


    """ PROGRAM STRUCTURE GRAMMAR """

    def compileClass(self, indent=0)->str:

        xml = ['<class>\n']

        xml.append(self.compileKeyword(indent+2, True, "class"))
        xml.append(self.compileIdentifier(indent+2))
        xml.append(self.compileSymbol(indent+2, True, "{"))

        while self.__scanner.current_token().value in ['static', 'field']:
            xml.append(self.compileClassVarDec(indent+2))

        while self.__scanner.current_token().value in ['constructor', 'function', 'method']:
            xml.append(self.compileSubroutine(indent+2))

        xml.append(self.compileSymbol(indent+2, True, '}'))
        xml.append('</class>')

        return ''.join(xml)


    def compileClassVarDec(self, indent : int)->str:

        xml = [' ' * indent + '<classVarDec>\n']

        xml.append(self.compileKeyword(indent+2, True, "static", "field"))
        xml.append(self.compileType(indent+2))
        xml.append(self.compileIdentifier(indent+2))

        while self.__scanner.current_token().value == ',':
            xml.append(self.compileSymbol(indent+2, True,","))
            xml.append(self.compileIdentifier(indent+2))

        xml.append(self.compileSymbol(indent+2, True, ';'))
        xml.append(' ' * indent + '</classVarDec>\n')

        return ''.join(xml)

    def compileType(self, indent : int)->str:
        token = self.__scanner.current_token()
        return self.compileIdentifier(indent) if token.token_type is TokenType.IDENTIFIER else self.compileKeyword(indent, True, 'int', 'char', 'boolean')

    def compileSubroutine(self, indent : int)->str:

        xml = [' ' * indent + '<subroutineDec>\n']

        xml.append(self.compileKeyword(indent+2, True, "constructor", "function", "method"))

        if self.__scanner.current_token().value == 'void':
            xml.append(self.compileKeyword(indent+2, True, "void"))
        else:
            xml.append(self.compileType(indent+2))

        xml.append(self.compileIdentifier(indent+2))
        xml.append(self.compileSymbol(indent+2, True, '('))
        xml.append(self.compileParameterList(indent+2))
        xml.append(self.compileSymbol(indent+2, True, ')'))

        xml.append(self.compileSubroutineBody(indent+2))
        xml.append(' ' * indent + '</subroutineDec>\n')
        return ''.join(xml)
    
    def compileSubroutineBody(self, indent: int) -> str:

        xml = [' ' * indent + '<subroutineBody>\n']
        xml.append(self.compileSymbol(indent+2, True, '{'))

        while self.__scanner.current_token().value == 'var':
            xml.append(self.compileVarDec(indent+2))

        xml.append(self.compileStatements(indent+2))
        xml.append(self.compileSymbol(indent+2, True, '}'))

        xml.append(' ' * indent + '</subroutineBody>\n')
        return ''.join(xml)


    def compileParameterList(self, indent : int)->str:
        xml = [' '* indent + '<parameterList>\n']

        current_token = self.__scanner.current_token()
        if not current_token.token_type is TokenType.SYMBOL:

            xml.append(self.compileType(indent+2))
            xml.append(self.compileIdentifier(indent+2))

            while self.__scanner.current_token().value == ',':
                xml.append(self.compileSymbol(indent+2, True, ','))
                xml.append(self.compileType(indent+2))
                xml.append(self.compileIdentifier(indent+2))

        xml.append(' '* indent + '</parameterList>\n')
        return ''.join(xml)

    def compileVarDec(self, indent : int)->str:
        xml = [' '* indent + '<varDec>\n']

        xml.append(self.compileKeyword(indent+2, True, 'var'))
        xml.append(self.compileType(indent+2))
        xml.append(self.compileIdentifier(indent+2))

        while self.__scanner.current_token().value == ',':
            xml.append(self.compileSymbol(indent+2, True, ','))
            xml.append(self.compileIdentifier(indent+2))

        xml.append(self.compileSymbol(indent+2, True, ';'))
        xml.append(' '* indent + '</varDec>\n')

        return ''.join(xml)

    """ STATEMENTS GRAMMAR """ 

    def compileStatements(self, indent : int)->str:
        xml= [' ' * indent + '<statements>\n']
        value = self.__scanner.current_token().value 

        while value in ['let', 'if', 'while', 'return', 'do']:

            if value == 'let':
                xml.append(self.compileLet(indent+2))
            elif value == 'if':
                xml.append(self.compileIf(indent+2))
            elif value == 'while':
                xml.append(self.compileWhile(indent+2))
            elif value == 'return':
                xml.append(self.compileReturn(indent+2))
            elif value == 'do':
                xml.append(self.compileDo(indent+2))

            value = self.__scanner.current_token().value 

        xml.append(' ' * indent + '</statements>\n')
        return ''.join(xml)


    def compileDo(self, indent : int)->str:
        xml= [' ' * indent + '<doStatement>\n']

        xml.append(self.compileKeyword(indent+2, True, 'do'))
        xml.append(self.compileSubroutineCall(indent))
        xml.append(self.compileSymbol(indent+2, True, ';'))

        xml.append(' ' * indent + '</doStatement>\n')
        return ''.join(xml)

    def compileLet(self, indent : int)->str:
        xml= [' ' * indent + '<letStatement>\n']

        xml.append(self.compileKeyword(indent+2, True, 'let'))
        xml.append(self.compileIdentifier(indent+2))
        
        if self.__scanner.current_token().value == '[':
            xml.append(self.compileSymbol(indent+2, True, '['))
            xml.append(self.compileExpression(indent+2))
            xml.append(self.compileSymbol(indent+2, True, ']'))

        xml.append(self.compileSymbol(indent+2, True, '='))
        xml.append(self.compileExpression(indent+2))
        xml.append(self.compileSymbol(indent+2, True, ';'))

        xml.append(' ' * indent + '</letStatement>\n')
        return ''.join(xml)


    def compileWhile(self, indent : int)->str:
        xml= [' ' * indent + '<whileStatement>\n']
        xml.append(self.compileKeyword(indent+2, True, 'while'))
        self.__compileBasicStatement(xml, indent)
        xml.append(' ' * indent + '</whileStatement>\n')

        return ''.join(xml)

    def compileReturn(self, indent : int)->str:
        xml= [' ' * indent + '<returnStatement>\n']
        xml.append(self.compileKeyword(indent+2, True, 'return'))

        if not self.__scanner.current_token().value == ';':
            xml.append(self.compileExpression(indent+2))

        xml.append(self.compileSymbol(indent+2, True, ';'))
        xml.append(' ' * indent + '</returnStatement>\n')
        return ''.join(xml)

    def compileIf(self, indent : int)->str:
        xml= [' ' * indent + '<ifStatement>\n']

        xml.append(self.compileKeyword(indent+2, True, 'if'))
        self.__compileBasicStatement(xml, indent)

        if self.__scanner.current_token().value == 'else':

            xml.append(self.compileKeyword(indent+2, True, 'else'))
            xml.append(self.compileSymbol(indent+2, True, '{'))
            xml.append(self.compileStatements(indent+2))
            xml.append(self.compileSymbol(indent+2, True, '}'))

        xml.append(' ' * indent + '</ifStatement>\n')
        return ''.join(xml)
    
    def compileSubroutineCall(self, indent: int) -> str:
        
        xml= []

        xml.append(self.compileIdentifier(indent+2))

        if self.__scanner.current_token().value == '.':
            xml.append(self.compileSymbol(indent+2, True, '.'))
            xml.append(self.compileIdentifier(indent+2))

        xml.append(self.compileSymbol(indent+2, True, '('))
        xml.append(self.compileExpressionList(indent+2))
        xml.append(self.compileSymbol(indent+2, True, ')'))

        return ''.join(xml)

    def __compileBasicStatement(self, xml, indent) -> None:

        xml.append(self.compileSymbol(indent+2, True, '('))
        xml.append(self.compileExpression(indent+2))
        xml.append(self.compileSymbol(indent+2, True, ')'))

        xml.append(self.compileSymbol(indent+2, True, '{'))
        xml.append(self.compileStatements(indent+2))
        xml.append(self.compileSymbol(indent+2, True, '}'))

    """ EXPRESSIONS GRAMMAR """

    def compileExpression(self, indent : int)->str:

        xml= [' ' * indent + '<expression>\n']
        xml.append(self.compileIntegerConstant(indent+2))
        xml.append(' ' * indent + '</expression>\n')
        return ''.join(xml)

    def compileTerm(self, indent : int)->str:
        pass

    def compileExpressionList(self, indent : int)->str:
        xml= [' ' * indent + '<expressionList>\n']
        xml.append(self.compileIntegerConstant(indent+2))
        xml.append(' ' * indent + '</expressionList>\n')
        return ''.join(xml)
