from grammar import Grammar as Gr
from mytoken import *
from mytoken import MyToken as Tk

def __makeGrammarWithCoolRules(grammar: Gr, coolN: set[Tk]) -> Gr:
    """Возвращает грамматику только с нетерминалами из которых выводятся терминалы"""
    coolRules = dict()
    for nonterm in coolN:
        coolRules[nonterm] = set()
        for rule in grammar.P[nonterm]:
            ruleset = set(rule)
            ruleLen = len(ruleset)
            TIntersect = grammar.T.intersection(ruleset)  # Пересечение терминалов грамматики и терминалов правила
            lenTIntersect = len(TIntersect)
            NIntersect = coolN.intersection(ruleset)  # Пересечение полезных нетерминалов и нетерминалов правила
            lenNIntersect = len(NIntersect)

            if (lenTIntersect == ruleLen) or ((lenNIntersect + lenTIntersect) == ruleLen):
                coolRules[nonterm].add(rule)
    return Gr(set([i.symbol for i in coolN]), grammar.getT(), coolRules, grammar.S.symbol)

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
