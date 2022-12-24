TOKEN_TERM = 0
TOKEN_NONTERM = 1

class MyToken:
    def __init__(self, type, symbol: str):
        self.type = type
        self.symbol = symbol
    
    def isTerm(self) -> bool:
        return self.type == TOKEN_TERM
    
    def isNonTerm(self) -> bool:
        return self.type == TOKEN_NONTERM

    def __eq__(self, other: 'MyToken') -> bool:
        return (self.type == other.type) and (self.symbol == other.symbol)
    
    def __hash__(self) -> int:
        return self.symbol.__hash__() + self.type
    
    def __str__(self) -> str:
        t = ""
        if self.isNonTerm():
            t = "NonTerm"
        else:
            t = "Term"
        return t + " " + self.symbol
