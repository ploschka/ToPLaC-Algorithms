class Grammar:
    def __init__(self, N: set[str], T: set[str], P: dict[str, list[str]], S: str):
        self.N = N # нетерминалы
        self.T = T # терминалы
        self.P = P # правила
        self.S = S # аксиома (начальный символ грамматики)
