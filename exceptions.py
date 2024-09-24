class JACKFileNeeded(Exception):
    pass

class OutOfTokens(Exception):
    pass

class KeywordExpectedException(Exception):
    pass

class SymbolExpectedException(Exception):
    pass

class SpecificKeywordExpectedException(Exception):
    pass

class SpecificSymbolExpectedException(Exception):
    pass

class IdentifierExpectedException(Exception):
    pass
