from grammar import Grammar as Gr

def __makeGrammarWithCoolRules(grammar: Gr, coolN: set[str]) -> Gr:
    """Возвращает грамматику только с нетерминалами из которых выводятся терминалы"""
    coolRules = dict()
    for nonterm in coolN:
        coolRules[nonterm] = list()
        for rule in grammar.P[nonterm]:
            ruleLen = len(rule)
            TIntersect = grammar.T.intersection(rule) # Пересечение терминалов грамматики и терминалов правила
            lenTIntersect = len(TIntersect)
            NIntersect = coolN.intersection(rule) # Пересечение полезных нетерминалов и нетерминалов правила 
            lenNIntersect = len(NIntersect)

            if (lenTIntersect == ruleLen) or ((lenNIntersect + lenTIntersect) == ruleLen):
                coolRules[nonterm].append(rule)
    return Gr(coolN, grammar.T, coolRules, grammar.S)


def isLanguageEmpty(grammar: Gr) -> tuple[bool, Gr|None]:
    """Порождает ли грамматика непустой язык"""
    N0 = set() # Шаг 1
    N1 = set()
    while True:
        for nonterm in grammar.P:
            for rule in grammar.P[nonterm]:
                ruleLen = len(rule)
                TIntersect = grammar.T.intersection(rule) # Пересечение терминалов грамматики и терминалов правила
                lenTIntersect = len(TIntersect)
                NIntersect = N0.intersection(rule) # Пересечение полезных нетерминалов и нетерминалов правила 
                lenNIntersect = len(NIntersect)

                if (lenTIntersect == ruleLen) or ((lenNIntersect + lenTIntersect) == ruleLen):
                    N1.add(nonterm) # Шаг 2: если из нетерминала nonterm выводится чистая строка терминалов,
                    break     # либо строка терминалов и полезных нетерминалов, то добавляем текущий нетерминал в список полезных нетерминалов
        if N0 == N1: # Шаг 3
            break
        else:
            N0 = N1.copy()
    if grammar.S in N1: # Шаг 4
        return False, __makeGrammarWithCoolRules(grammar, N1)
    else:
        return True, None

def unreachable_symbols(grammar: Gr) -> Gr:
    V0 = set()
    V0.add(grammar.S) # Шаг 1
    V1 = set()
    wasHere = set()
    while True:
        NT = V0.intersection(grammar.N) # Шаг 2
        for nonterm in NT:
            if nonterm not in wasHere:
                rules = grammar.P.get(nonterm, None)
                if rules is not None:
                    for rule in rules:
                        V1.update(rule)
            wasHere.add(nonterm)

        if V0 == V1: # Шаг 3
            break
        else:
            V0 = V1.copy()

    newNonTerms = V1.intersection(grammar.N)
    newTerms = V1.intersection(grammar.T)
    newRules = dict()
    for nonterm in newNonTerms:
        rules = grammar.P.get(nonterm, None)
        if rules is not None:
            newRules[nonterm] = list()
            for rule in rules:
                newRules[nonterm].append(rule)
    return Gr(newNonTerms, newTerms, newRules, grammar.S)

def useless_symbols(grammar: Gr) -> Gr|None:
    isEmpty, gr1 = isLanguageEmpty(grammar)
    if not isEmpty:
        return unreachable_symbols(gr1) # type: ignore
    return None
