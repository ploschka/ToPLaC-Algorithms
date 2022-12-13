from grammar import Grammar as Gr


def __makeGrammarWithCoolRules(grammar: Gr, coolN: set[str]) -> Gr:
    """Возвращает грамматику только с нетерминалами из которых выводятся терминалы"""
    coolRules = dict()
    for nonterm in coolN:
        coolRules[nonterm] = list()
        for rule in grammar.P[nonterm]:
            ruleset = set(rule)
            ruleLen = len(ruleset)
            TIntersect = grammar.T.intersection(ruleset)  # Пересечение терминалов грамматики и терминалов правила
            lenTIntersect = len(TIntersect)
            NIntersect = coolN.intersection(ruleset)  # Пересечение полезных нетерминалов и нетерминалов правила
            lenNIntersect = len(NIntersect)

            if (lenTIntersect == ruleLen) or ((lenNIntersect + lenTIntersect) == ruleLen):
                coolRules[nonterm].append(rule)
    return Gr(coolN, grammar.T, coolRules, grammar.S)


def isLanguageEmpty(grammar: Gr) -> tuple[bool, Gr]:
    """Порождает ли грамматика пустой язык"""
    N0 = set()  # Шаг 1
    N1 = set()
    while True:
        for nonterm in grammar.P:  # Берём нетерминал, из которого можно что-то вывести по правилу
            for rule in grammar.P[nonterm]:  # Для этого нетерминала берём правило
                ruleset = set(rule)
                ruleLen = len(ruleset)  # Количество символов в правиле
                TIntersect = grammar.T.intersection(ruleset)  # Пересечение терминалов грамматики и терминалов правила
                lenTIntersect = len(TIntersect)  # Количество терминалов в правиле
                NIntersect = N0.intersection(ruleset)  # Пересечение полезных нетерминалов и нетерминалов правила
                lenNIntersect = len(NIntersect)  # Количество полезных нетерминалов в правиле

                if (lenTIntersect == ruleLen) or ((lenNIntersect + lenTIntersect) == ruleLen):
                    N1.add(nonterm)  # Шаг 2: если из нетерминала nonterm выводится чистая строка терминалов,
                    break  # либо строка терминалов и полезных нетерминалов, то добавляем текущий нетерминал в список полезных нетерминалов
        if N0 == N1:  # Шаг 3
            break
        else:
            N0 = N1.copy()
    if grammar.S in N1:  # Шаг 4
        return False, __makeGrammarWithCoolRules(grammar, N1)
    else:
        return True, grammar


def unreachableSymbols(grammar: Gr) -> Gr:
    """Устранение недостижимых символов в грамматике"""
    V0 = set()  # Множество достижимых символов
    V0.add(grammar.S)  # Шаг 1
    V1 = V0.copy()
    wasHere = set()
    while True:
        NT = V0.intersection(grammar.N)  # Шаг 2. Получаем все нетерминалы, которых достигли за предыдущие шаги
        for nonterm in NT:  # Проходимся по всем достигнутым нетерминалам
            if nonterm not in wasHere:  # Если нетерминал раннее не рассматривался
                rules = grammar.P.get(nonterm, None)  # Ищем для этого нетерминала правило
                if rules is not None:  # Если правило существует
                    for rule in rules:
                        V1.update(rule)  # Добавляем все символы правила в множество достижимых символов
            wasHere.add(nonterm)

        if V0 == V1:  # Шаг 3
            break
        else:
            V0 = V1.copy()

    newNonTerms = V1.intersection(grammar.N)  # Все достижимые нетерминалы
    newTerms = V1.intersection(grammar.T)  # Все достижимые терминалы
    newRules = dict()  # Все правила для достижимых нетерминалов
    for nonterm in newNonTerms:
        rules = grammar.P.get(nonterm, None)
        if rules is not None:
            newRules[nonterm] = list()
            for rule in rules:
                newRules[nonterm].append(rule)
    return Gr(newNonTerms, newTerms, newRules, grammar.S)


def unreachableSymbolsShort(g: Gr) -> Gr:
    reachable = {g.S}
    [reachable := reachable | set.union(*[set(g.P.get(ch, [])[i]) for ch in reachable for i in range(len(g.P.get(ch, [])))]) for _ in range(len(g.P))]
    return Gr(g.N.intersection(reachable), g.T.intersection(reachable), {ch: g.P[ch] for ch in reachable if g.P.get(ch) is not None}, g.S)

def uselessSymbols(grammar: Gr) -> Gr:
    """Устранение бесполезных символов в грамматике"""
    isEmpty, gr1 = isLanguageEmpty(grammar)
    if not isEmpty:
        return unreachableSymbols(gr1)
    return grammar
