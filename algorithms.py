from grammar import Grammar as Gr
import itertools


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
            newRules[nonterm] = set()
            for rule in rules:
                newRules[nonterm].add(rule)
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

def __add_new_rules_to_dict_of_p_i(dict_of_p_i: dict,
                                     dict_key: str,
                                     string: str,
                                     list_of_indexes_to_alternate: list[int]):
    amount_of_indexes = len(list_of_indexes_to_alternate)
    p_i_right_part: list[str] = []
    if amount_of_indexes > 0:
        listed_pattern: list[int]
        buffer_string: str
        index_shift: int
        combination_patterns = iter(
            itertools.product([0, 1], repeat=amount_of_indexes)
        )
        for pattern in combination_patterns:
            listed_pattern = list(pattern)
            buffer_string = string
            index_shift = 0
            for i in range(0, len(listed_pattern)):
                if listed_pattern[i] == 0:
                    buffer_string = buffer_string[:list_of_indexes_to_alternate[i]-index_shift] + \
                                    buffer_string[list_of_indexes_to_alternate[i]-index_shift+1:]
                    index_shift += 1
            p_i_right_part.append(buffer_string)
    else:
        p_i_right_part.append(string)
    if dict_key in dict_of_p_i.keys():
        dict_of_p_i[dict_key] += p_i_right_part
        dict_of_p_i[dict_key] = list(set(dict_of_p_i[dict_key]))
    else:
        dict_of_p_i[dict_key] = p_i_right_part

def wipeExcessLambdaRules(grammar: Gr) -> Gr:
    """
    Алгоритм устранения лишних лямбда-правил!
    ---
    Некоторые понятия в комментариях могут быть Вам незнакомы.
    Это потому что я их сам придумал! Определения им даю почти сразу при употреблении.
    """
    """
    1-й шаг.
    n_lambda - все нетерминалы, из которых выводятся лямбда-цепочки.
    n_term_plus - все нетерминалы, из которых выводятся непустые терминальные цепочки.
    """
    n_lambda = set()
    n_term_plus = set()
    """
    А-й подшаг 1-го шага.
    Поиск и добавление нечистых и чистых первородных лямбда-нетерминалов. 
    Нечистые первородные лямбда-нетерминалы - нетерминалы, из которых непосредственно выводится НЕ ТОЛЬКО лямбда.
    Пример: A -> λ | a.
    Чистые первородные лямбда-нетерминалы - нетерминалы, из которых непосредственно выводится ТОЛЬКО лямбда.
    Пример: A -> λ.
    
    Чистые первородные лямбда-нетерминалы также добавим в множество pure_n_lambda. 
    Такие нетерминалы точно не окажутся в n_term_plus.
    """
    count_of_all_lambda_consequents: int
    pure_n_lambda = set()
    for non_term in grammar.N:
        if non_term not in grammar.P.keys():
            continue
        if '' in grammar.P[non_term]:
            n_lambda.add(non_term)
            if len(grammar.P[non_term]) == 1:
                pure_n_lambda.add(non_term)

    """
    Б-й подшаг 1-го шага.
    Поиск и добавление нечистых и чистых старшеродных лямбда-нетерминалов. 
    Нечистые старшеродные лямбда-нетерминалы - нетерминалы, из которых транзитивно выводится НЕ ТОЛЬКО лямбда.
    Пример: A -> λ | a.
    Чистые старшеродные лямбда-нетерминалы - нетерминалы, из которых транзитивно выводится ТОЛЬКО лямбда.
    Пример: A -> λ.
    Чистые старшеродные лямбда-нетерминалы также добавим в множество pure_n_lambda. 
    Такие нетерминалы точно не окажутся в n_term_plus.
    """
    while True:
        is_n_lambda_appended = False
        for non_term in grammar.N:
            if not(non_term in grammar.P.keys() and non_term not in n_lambda):
                continue
            count_of_all_lambda_consequents = 0
            count_of_pure_lambda_consequents = 0
            for consequent in grammar.P[non_term]:
                for symbol in consequent:
                    if symbol in n_lambda:
                        count_of_all_lambda_consequents += consequent.count(symbol)
                        if symbol in pure_n_lambda:
                            count_of_pure_lambda_consequents += consequent.count(symbol)
                if len(consequent) == count_of_all_lambda_consequents:
                    n_lambda.add(non_term)
                    is_n_lambda_appended = True
                    if len(consequent) == count_of_pure_lambda_consequents:
                        pure_n_lambda.add(non_term)
        if not is_n_lambda_appended:
            break

    """
    В-й подшаг 1-го шага.
    Поиск и добавление нетерминалов, из которых выводятся 
    непустые терминальные цепочки, в n_term_plus.
    """
    for non_term in grammar.N:
        if non_term in grammar.P.keys() and non_term not in pure_n_lambda:
            n_term_plus.add(non_term)

    """
    2-й шаг.
    new_rules - новый набор правил.
    """
    new_rules: dict = {}

    """
    3-й шаг.
    Найдём q - множество всех правил, в правых частях которых есть символы n_lambda
    """
    q: dict = {}

    for key in grammar.P:
        is_key_added = False
        for string in grammar.P[key]:
            for symbol in n_lambda:
                if string.find(symbol) > -1:
                    q[key] = grammar.P[key]
                    is_key_added = True
                    break
            if is_key_added:
                break
        if is_key_added:
            continue

    """
    Добавим dict_of_p_i - множество правил на основе каждого i-го правила из q.
    Причём из каждого нового правила выводятся непустые цепочки
    """
    dict_of_p_i: dict = {}
    list_of_indexes_to_alternate: list[int]
    for key in q:
        for string in q[key]:
            i = 0
            list_of_indexes_to_alternate = []
            string_length = len(string)
            while i < string_length:
                if string[i] in n_lambda and string[i] in n_term_plus:
                    list_of_indexes_to_alternate.append(i)
                    i += 1
                elif string[i] in n_lambda:
                    string = string[:i] + string[i+1:]
                    string_length -= 1
                else:
                    i += 1
            if len(string) > 0:
                __add_new_rules_to_dict_of_p_i(dict_of_p_i,
                                                    key,
                                                    string,
                                                    list_of_indexes_to_alternate)

    """
    Шаг 4.
    Добавляем в new_p все правила вида B -> a, где a не содержит символов из n_lambda
    и a != lambda.
    """
    for key in grammar.P:
        if key in n_lambda:
            continue
        is_non_lambda = True
        for consequents in grammar.P[key]:
            for consequent in consequents:
                for symbol in n_lambda:
                    if consequent.find(symbol) > -1:
                        is_non_lambda = False
                        break
                if not is_non_lambda:
                    break
            if not is_non_lambda:
                break
        if is_non_lambda:
            new_rules[key] = grammar.P[key]
    for key in dict_of_p_i:
        new_rules[key] = dict_of_p_i[key]

    """
    Шаг 5.
    Проверяем аксиому.
    Если S = lambda || S принадл. n_lambda, 
    то добавим в new_p правило new_axiom -> S|lambda
    """
    new_axiom: str = grammar.S
    if grammar.S == "" or grammar.S in n_lambda:
        new_axiom = "new_" + grammar.S
        new_rules[new_axiom] = [grammar.S, ""]

    """
    Шаг 6.
    Формируем новую грамматику.
    """

    new_non_terminals = n_term_plus
    new_non_terminals.add(new_axiom)

    return Gr(new_non_terminals, grammar.T, new_rules, new_axiom)