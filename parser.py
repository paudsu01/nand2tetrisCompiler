from __future__ import annotations
from scanner import Scanner
from jack_token import TokenType
from exceptions import KeywordExpectedException,\
        SymbolExpectedException,\
        IdentifierExpectedException,\
        SpecificKeywordExpectedException,\
        SpecificSymbolExpectedException

from typing import Tuple
from symbol_table import SymbolTable
from vm_writer import VM_writer

class Parser:
    
    def __init__(self, scanner: Scanner, className: str):
        self.__scanner = scanner
        self.__vm_writer = VM_writer(className)
        self.__class_name = className
        self.__label_number = 0

    """ LEXICAL ELEMENTS """

    def compileKeyword(self, specific_value_required=False, *specific_values: Tuple[str]) -> None:

        current_token = self.__scanner.current_token()

        if not (current_token.token_type is TokenType.KEYWORD):
            raise KeywordExpectedException(f'Keyword expected: got {current_token.value} instead')

        if specific_value_required and current_token.value not in specific_values:
            raise SpecificKeywordExpectedException(f'{specific_values} keyword(s) expected: got {current_token.value} keyword instead')

        if self.__scanner.has_more_tokens(): self.__scanner.advance()


    def compileSymbol(self, specific_value_required=False, *expected_values: Tuple[str]) -> None:
        current_token = self.__scanner.current_token()

        if not (current_token.token_type is TokenType.SYMBOL):
            raise SymbolExpectedException(f'Symbol expected: got {current_token.value} instead')

        if specific_value_required and current_token.value not in expected_values:
            raise SpecificSymbolExpectedException(f'{expected_values} symbol(s) expected: got {current_token.value} keyword instead')
        
        if self.__scanner.has_more_tokens(): self.__scanner.advance()


    def compileIntegerConstant(self) -> None:
        current_token = self.__scanner.current_token()

        if not (current_token.token_type is TokenType.INTEGER_CONSTANT):
            raise SymbolExpectedException(f'IntegerConstant expected: got {current_token.value} instead')

        if self.__scanner.has_more_tokens(): self.__scanner.advance()


    def compileStringConstant(self) -> None:
        current_token = self.__scanner.current_token()

        if not (current_token.token_type is TokenType.STRING_CONSTANT):
            raise SymbolExpectedException(f'StringConstant expected: got {current_token.value} instead')

        if self.__scanner.has_more_tokens(): self.__scanner.advance()


    def compileIdentifier(self) -> None:

        current_token = self.__scanner.current_token()

        if not (current_token.token_type is TokenType.IDENTIFIER):
            raise IdentifierExpectedException(f'Identifier expected: got {current_token.value} instead')

        if self.__scanner.has_more_tokens(): self.__scanner.advance()

    """ PROGRAM STRUCTURE GRAMMAR """

    def compileClass(self) -> None:

        self.compileKeyword(True, "class")
        self.compileIdentifier()
        self.compileSymbol(True, "{")

        while self.__scanner.current_token().value in ['static', 'field']:
            self.compileClassVarDec()

        while self.__scanner.current_token().value in ['constructor', 'function', 'method']:
            self.compileSubroutine()

        self.compileSymbol(True, '}')
    
        self.__vm_writer.close()

    def compileClassVarDec(self) -> None:

        var_type = self.__scanner.current_token().value
        self.compileKeyword(True, "static", "field")

        class_type = self.__scanner.current_token().value
        self.compileType()

        identifier = self.__scanner.current_token().value
        self.compileIdentifier()

        SymbolTable.add(identifier, var_type, class_type)

        while self.__scanner.current_token().value == ',':
            self.compileSymbol(True,",")
            identifier = self.__scanner.current_token().value
            self.compileIdentifier()
            SymbolTable.add(identifier, var_type , class_type)

        self.compileSymbol(True, ';')

    def compileType(self) -> None:
        token = self.__scanner.current_token()
        self.compileIdentifier() if token.token_type is TokenType.IDENTIFIER else self.compileKeyword(True, 'int', 'char', 'boolean')


    def compileSubroutine(self, constructor=False) -> None:

        def compileSubroutineBody() -> None:
            nonlocal constructor

            self.compileSymbol(True, '{')

            while self.__scanner.current_token().value == 'var':
                self.compileVarDec()

            self.__vm_writer.write_function(f'{self.__class_name}.{function_name}', SymbolTable.get_total_locals())
            if subroutine_type == 'method':
                self.__vm_writer.write_push("argument", 0)
                self.__vm_writer.write_pop("pointer", 0)

            elif subroutine_type == 'constructor':
                constructor = True
                self.__vm_writer.write_push("constant", SymbolTable.get_total_fields())
                self.__vm_writer.write_call("Memory.alloc", 1)
                self.__vm_writer.write_pop("pointer", 0)

            self.compileStatements(constructor)
            self.compileSymbol(True, '}')

        subroutine_type = self.__scanner.current_token().value 
        self.compileKeyword(True, "constructor", "function", "method")

        if subroutine_type == 'method':
            SymbolTable.set_argument_counter_to_one()

        if self.__scanner.current_token().value == 'void':
            self.compileKeyword(True, "void")
        else:
            self.compileType()

        function_name = self.__scanner.current_token().value 
        self.compileIdentifier()

        self.compileSymbol(True, '(')
        self.compileParameterList()
        self.compileSymbol(True, ')')

        compileSubroutineBody()


    def compileParameterList(self) -> None:

        current_token = self.__scanner.current_token()
        if not current_token.token_type is TokenType.SYMBOL:
            
            var_type = self.__scanner.current_token().value
            self.compileType()

            identifier = self.__scanner.current_token().value
            self.compileIdentifier()

            SymbolTable.add(identifier, 'arg', var_type)

            while self.__scanner.current_token().value == ',':
                self.compileSymbol(True, ',')

                var_type = self.__scanner.current_token().value
                self.compileType()

                identifier = self.__scanner.current_token().value
                self.compileIdentifier()

                SymbolTable.add(identifier, 'arg', var_type)

    def compileVarDec(self) -> None:
        self.compileKeyword(True, 'var')

        var_type = self.__scanner.current_token().value
        self.compileType()

        current_token = self.__scanner.current_token()
        self.compileIdentifier()

        SymbolTable.add(current_token.value, 'var', var_type)

        while self.__scanner.current_token().value == ',':
            self.compileSymbol(True, ',')

            current_token = self.__scanner.current_token()
            self.compileIdentifier()

            SymbolTable.add(current_token.value, 'var', var_type)

        self.compileSymbol(True, ';')

    """ STATEMENTS GRAMMAR """ 

    def compileStatements(self, constructor=False) -> None:
        value = self.__scanner.current_token().value 

        while value in ['let', 'if', 'while', 'return', 'do']:

            if value == 'let':
                self.compileLet()
            elif value == 'if':
                self.compileIf()
            elif value == 'while':
                self.compileWhile()
            elif value == 'return':
                self.compileReturn(constructor)
            elif value == 'do':
                self.compileDo()

            value = self.__scanner.current_token().value 


    def compileDo(self) -> None:

        self.compileKeyword(True, 'do')
        self.compileSubroutineCall()
        self.compileSymbol(True, ';')

        self.__vm_writer.write_pop("temp", 0)

    def compileLet(self) -> None:
        array_let = False

        self.compileKeyword(True, 'let')
        variable = SymbolTable.get_variable(self.__scanner.current_token().value)
        self.compileIdentifier()
        
        if self.__scanner.current_token().value == '[':
            array_let = True

            self.__vm_writer.write_push(variable.memory_segment, variable.index)

            self.compileSymbol(True, '[')
            self.compileExpression()
            self.compileSymbol(True, ']')

            self.__vm_writer.write_arithmetic('+')

        self.compileSymbol(True, '=')
        self.compileExpression()
        self.compileSymbol(True, ';')

        if array_let:
            self.__vm_writer.write_pop("temp", 0)
            self.__vm_writer.write_pop("pointer", 1)
            self.__vm_writer.write_push("temp", 0)
            self.__vm_writer.write_pop("that", 0)

        else:
            self.__vm_writer.write_pop(variable.memory_segment, variable.index)


    def compileWhile(self) -> None:
        self.__vm_writer.write_label(f'{self.__class_name}$secondLabel${self.__label_number}')
        self.compileKeyword(True, 'while')

        self.__compileBasicStatement()
        self.__vm_writer.write_label(f'{self.__class_name}$not_true${self.__label_number}')

        self.__label_number += 1


    def compileReturn(self, constructor: False) -> None:
        self.compileKeyword(True, 'return')

        if not self.__scanner.current_token().value == ';':
            self.compileExpression()
        elif constructor:
            self.__vm_writer.write_push("pointer", 0)
        else:
            self.__vm_writer.write_push("constant", 0)

        self.__vm_writer.write_return()

        self.compileSymbol(True, ';')
        SymbolTable.reset_subroutine_table()

    def compileIf(self) -> None:
        self.compileKeyword(True, 'if')
        self.__compileBasicStatement()
        self.__vm_writer.write_label(f'{self.__class_name}$not_true${self.__label_number}')

        if self.__scanner.current_token().value == 'else':

            self.compileKeyword(True, 'else')
            self.compileSymbol(True, '{')
            self.compileStatements()
            self.compileSymbol(True, '}')

        self.__vm_writer.write_label(f'{self.__class_name}$secondLabel${self.__label_number}')
        self.__label_number += 1


    def compileSubroutineCall(self) -> None:
        
        basic_args = 0
        subroutine_name = self.__scanner.current_token().value
        self.compileIdentifier()

        if self.__scanner.current_token().value == '.':

            same_class = False
            self.compileSymbol(True, '.')
            method_name = self.__scanner.current_token().value
            self.compileIdentifier()

            if SymbolTable.contains(subroutine_name):
                variable = SymbolTable.get_variable(subroutine_name)
                basic_args = 1
                self.__vm_writer.write_push(variable.memory_segment, variable.index)
                class_name = variable.class_name
            else:
                class_name = subroutine_name

        else:
            same_class = True
            if subroutine_name != 'new':
                basic_args = 1
                self.__vm_writer.write_push("pointer", 0)

        self.compileSymbol(True, '(')
        n_args = self.compileExpressionList()
        self.compileSymbol(True, ')')

        if same_class:
            self.__vm_writer.write_call(f'{self.__class_name}.{subroutine_name}', n_args+basic_args)
        else:
            self.__vm_writer.write_call(f'{class_name}.{method_name}', n_args+basic_args)

    def __compileBasicStatement(self) -> None:

        self.compileSymbol(True, '(')
        self.compileExpression()

        self.__vm_writer.write_arithmetic('~')
        self.__vm_writer.write_if(f'{self.__class_name}$not_true${self.__label_number}')

        self.compileSymbol(True, ')')

        self.compileSymbol(True, '{')
        self.compileStatements()
        self.compileSymbol(True, '}')

        self.__vm_writer.write_goto(f'{self.__class_name}$secondLabel${self.__label_number}')

    """ EXPRESSIONS GRAMMAR """

    def compileExpression(self) -> None:

        self.compileTerm()
        while self.__scanner.current_token().value in ['+', '-', '*', '/', '&', '|', '<', '>', '=']:
            op_token = self.__scanner.current_token().value

            self.compileSymbol()
            self.compileTerm()

            self.__vm_writer.write_arithmetic(op_token)


    def compileTerm(self) -> None:
        token = self.__scanner.current_token()

        if token.token_type is TokenType.INTEGER_CONSTANT:
            self.compileIntegerConstant()
            self.__vm_writer.write_push('constant', token.value)

        elif token.token_type is TokenType.KEYWORD:
            self.compileKeyword()

            if token.value in ['false', 'null']:
                self.__vm_writer.write_push('constant', 0)

            elif token.value == 'true':
                self.__vm_writer.write_push('constant', 1)
                self.__vm_writer.write_arithmetic('~')

        elif token.token_type is TokenType.STRING_CONSTANT:
            self.compileStringConstant()

        elif token.value == '(':
            self.compileSymbol(True, '(')
            self.compileExpression()
            self.compileSymbol(True, ')')

        elif token.value in ['-', '~']:
            self.compileSymbol(True, token.value)
            self.compileTerm()
            self.__vm_writer.write_arithmetic(token.value)

        elif token.token_type is TokenType.IDENTIFIER:

            if self.__scanner.has_more_tokens():
                next_token = self.__scanner.next_token()

                if next_token.value == '[':
                    variable = SymbolTable.get_variable(token.value)
                    self.__vm_writer.write_push(variable.memory_segment, variable.index)

                    self.compileIdentifier()
                    self.compileSymbol(True, '[')
                    self.compileExpression()
                    self.compileSymbol(True, ']')

                    self.__vm_writer.write_arithmetic('+')
                    self.__vm_writer.write_pop('pointer', 1)
                    self.__vm_writer.write_push('that', 0)

                elif next_token.value == '(' or next_token.value == '.':
                    self.compileSubroutineCall()

                else:
                    self.compileIdentifier()

                    variable = SymbolTable.get_variable(token.value)
                    self.__vm_writer.write_push(variable.memory_segment, variable.index)

            else:
                self.compileIdentifier()
 

    def compileExpressionList(self) -> int:

        number_of_args = 0
        if self.__scanner.current_token().value != ')':
            self.compileExpression()
            number_of_args += 1
            while self.__scanner.current_token().value == ',':
                self.compileSymbol(True, ',')
                self.compileExpression()
                number_of_args += 1

        return number_of_args
