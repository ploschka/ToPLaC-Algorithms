from grammar import Grammar as Gr
from mytoken import *
from mytoken import MyToken as Tk


def leftRecursionRemoval(grammar: Gr) -> Gr:
    """
    Алгоритм устранения левой рекурсии
    grammar - приведённая контекстно-свободная грамматика
    Возвращает грамматику без левых рекурсий
    """
    N = list(grammar.N)  # Шаг 0: Упорядочиваем нетерминалы
    N.sort(key=lambda x: x.symbol)
    i = 0  # Шаг 1: Указатель, последовательно проходится по нетерминалам в N
    while True:
        # Шаг 2: Ищем у нетерминала правила с левой рекурсией и изменяем их соответствующим образом
        curr_nonterm = N[i]  # Текущий нетерминал, у которого убираем левую рекурсию
        left_rec_rules, no_left_rec_rules = __find_left_rec_rules(grammar.P[curr_nonterm], curr_nonterm)
        if len(left_rec_rules) != 0:  # Если из нетерминала выводится левая рекурсия и правила нужно изменить
            new_nonterm = Tk(TOKEN_NONTERM, curr_nonterm.symbol + "'")
            grammar.P[curr_nonterm] = no_left_rec_rules | {rule + (new_nonterm,) for rule in no_left_rec_rules}
            grammar.P[new_nonterm] = {rule[1:] for rule in left_rec_rules} | \
                                     {rule[1:] + (new_nonterm,) for rule in left_rec_rules}

        if i == len(N) - 1:  # Шаг 3: Проверяем, дошли ли мы до конца изначальных нетерминалов
            return grammar
        i += 1
        # Шаг 4: Ищем возникновение левых рекурсий в правилах предыдущих нетерминалов и исправляем
        Ai = N[i]
        for j in range(0, i):
            Aj = N[j]
            left_rec_rules, no_left_rec_rules = __find_left_rec_rules(grammar.P[Ai], Aj)
            grammar.P[Ai] = no_left_rec_rules
            for recursed_rule in left_rec_rules:  # Правила вида Ai -> Aj... | Aj... Нужно заменить Aj на его правила
                Aj_rules = grammar.P[Aj]
                for Aj_rule in Aj_rules:  # Правила вида Aj -> ... | ...
                    grammar.P[Ai].add(Aj_rule + recursed_rule[1:])


def __find_left_rec_rules(rules: set[tuple[Tk, ...]], target: Tk) -> tuple[set[tuple[Tk, ...]], set[tuple[Tk, ...]]]:
    """Разделяет множество правил rules на два множества:
    1. Правила, начинающиеся с символа target
    2. Правила, не начинающиеся с символа target
    """
    left_rec_rules = set()  # Правила с левой рекурсией
    no_left_rec_rules = set()  # Правила без левой рекурсии
    for rule in rules:  # Ищем правила, начинающиеся с нетерминала curr_nonterm
        if rule[0] == target:
            left_rec_rules.add(rule)
        else:
            no_left_rec_rules.add(rule)
    return left_rec_rules, no_left_rec_rules
