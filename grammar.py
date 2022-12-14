class Grammar:
    def __init__(self, N: set[str], T: set[str], P: dict[str, set[str]], S: str):
        self.N = N  # Нетерминалы. Например, {"E", "T", "F"}
        self.T = T  # Терминалы. Например, {"a", "(", ")"}
        self.P = P  # Правила. Например, { "E": ["E+T", "T"], "T": {"T*F", "F"}, "F": {"(E)", "a"} }
        self.S = S  # Аксиома (начальный символ грамматики). Например, "E"

    def __str__(self):
        """Метод для красивого вывода грамматики с помощью print()"""
        rules = ""
        for non_term in self.P.keys():
            rules += f"\n\t\t{non_term} -> " + \
                     " | ".join(self.P[non_term])
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
