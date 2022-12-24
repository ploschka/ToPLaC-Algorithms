from grammar import Grammar as Gr
from mytoken import *
from mytoken import MyToken as Tk

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
            newRules[nonterm] = set()
            for rule in rules:
                newRules[nonterm].add(rule)
    return Gr(set([i.symbol for i in newNonTerms]), set([i.symbol for i in newTerms]), newRules, grammar.S.symbol)
