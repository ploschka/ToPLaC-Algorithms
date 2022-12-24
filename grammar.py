from mytoken import *
from mytoken import MyToken as Tk

class Grammar:
    Tokens = dict()
    N = set()
    T = set()

    def __init__(self, N: set[str], T: set[str], P: dict[Tk, set[tuple]], S: str):
        for i in N:
            self.Tokens[i] = Tk(TOKEN_NONTERM, i)
            self.N.add(self.Tokens[i]) # Нетерминалы. Например, {"E", "T", "F"}
        for i in T:
            self.Tokens[i] = Tk(TOKEN_TERM, i)
            self.T.add(self.Tokens[i]) # Терминалы. Например, {"a", "(", ")"}
        self.P = P # Правила. Например, { "E": {"E+T", "T"}, "T": {"T*F", "F"}, "F": {"(E)", "a"} }
        self.S = self.Tokens[S] # Аксиома (начальный символ грамматики). Например, "E"

    def getN(self):
        return set([i.symbol for i in self.N])

    def getT(self):
        return set([i.symbol for i in self.T])

    def getS(self):
        return self.S.symbol

    def __str__(self):
        """Метод для красивого вывода грамматики с помощью print()"""
        rules = ""
        for non_term in self.P.keys():
            rules += f"\n\t\t{non_term.symbol} -> " + " | ".join(*[([nt.symbol for nt in st]) for st in self.P[non_term]])
        return f"""{{
    Нетерминалы: {self.N}
    Терминалы: {self.T}
    Правила: {rules}
    Аксиома: {self.S}
}}"""

    def __eq__(self, other):
        """Оператор равенства грамматик"""
        if set(self.P.keys()) == set(other.P.keys()):
            for rule in self.P:
                if self.P[rule] != other.P[rule]:
                    return False
        else:
            return False
        return self.N == other.N and \
               self.T == other.T and \
               self.S == other.S
