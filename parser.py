from scanner import Scanner

class Parser:

    def __init__(self, scanner: Scanner):
        self.scanner = scanner

    """ LEXICAL ELEMENTS """

    def compileKeyword(self):
        pass

    def compileSymbol(self):
        pass

    def compileIntegerConstant(self):
        pass

    def compileStringConstant(self):
        pass

    def compileIdentifier(self):
        pass

    """ PROGRAM STRUCTURE GRAMMAR """

    def compileClass(self):
        pass

    def compileClassVarDec(self):
        pass

    def compileType(self):
        pass

    def compileSubroutine(self):
        pass

    def compileParameterList(self):
        pass

    def compileVarDec(self):
        pass

    """ STATEMENTS GRAMMAR """ 

    def compileStatements(self):
        pass

    def compileDo(self):
        pass

    def compileLet(self):
        pass

    def compileWhile(self):
        pass

    def compileReturn(self):
        pass

    def compileIf(self):
        pass
    
    """ EXPRESSIONS GRAMMAR """

    def compileExpression(self):
        pass

    def compileTerm(self):
        pass

    def compileExpressionList(self):
        pass

    def compileOp(self):
        pass

    def compileUnaryOp(self):
        pass

    def compileKeywordConstant(self):
        pass
