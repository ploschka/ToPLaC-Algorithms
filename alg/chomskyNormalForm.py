from grammar import Grammar as Gr
from mytoken import *
from mytoken import MyToken as Tk

def __termToNonTerm(term: Tk) -> Tk:
    return Tk(TOKEN_NONTERM, term.symbol + "`")

def __processRule(nonterm: Tk, rule: tuple) -> dict[Tk, tuple]:
    result = dict()
    if len(rule) > 2:
        left = rule[0]
        right = rule[1:]
        rightSymbol = Tk(TOKEN_NONTERM, "".join([i.symbol for i in right]))
        res = __processRule(rightSymbol, right)
        if left.isTerm():
            newLeft = __termToNonTerm(left)
            result[newLeft] = (left,)
            left = newLeft
        result[nonterm] = (left, rightSymbol)
        result.update(res)
    else:
        lt = rule[0].isTerm()
        rt = rule[1].isTerm()
        left = rule[0]
        right = rule[1]

        if lt:
            newLeft = __termToNonTerm(left)
            result[newLeft] = (left,)
            left = newLeft
        if rt:
            newRight = __termToNonTerm(right)
            result[newRight] = (right,)
            right = newRight
        result[nonterm] = (left, right)
    
    return result
        

def chomskyNormalForm(grammar: Gr) -> Gr:
    newRules = dict() # Словарь с подходящими правилами
    rulesToProcess = dict() # Словарь с неподходящими правилами
    newNonTerms = grammar.N.copy()

    for nonterm in grammar.P: # Заполнение словарей
        newRules[nonterm] = set()
        badRules = set()
        for rule in grammar.P[nonterm]:
            rulelen = len(rule)
            if rulelen == 2 and rule[0].isNonTerm() and rule[1].isNonTerm():
                newRules[nonterm].add(rule)
            elif rulelen == 1 and rule[0].isTerm():
                newRules[nonterm].add(rule)
            else:
                badRules.add(rule)
        if len(badRules) > 0:
            rulesToProcess[nonterm] = badRules.copy()
    
    for nonterm in rulesToProcess:
        for rule in rulesToProcess[nonterm]:
            processed = __processRule(nonterm, rule)
            keys = processed.keys()
            newNonTerms.update(keys)
            for key in keys:
                if key not in newRules:
                    newRules[key] = set()
                newRules[key].add(processed[key])

    return Gr(set([i.symbol for i in newNonTerms]), grammar.getT() , newRules, grammar.getS())
