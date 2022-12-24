from grammar import Grammar as Gr
from mytoken import *
from mytoken import MyToken as Tk
import itertools

# def __add_new_rules_to_dict_of_p_i(dict_of_p_i: dict,
#                                      dict_key: str,
#                                      string: str,
#                                      list_of_indexes_to_alternate: list[int]):
#     amount_of_indexes = len(list_of_indexes_to_alternate)
#     p_i_right_part: set[str] = set()
#     if amount_of_indexes > 0:
#         listed_pattern: list[int]
#         buffer_string: str
#         index_shift: int
#         combination_patterns = iter(
#             itertools.product([0, 1], repeat=amount_of_indexes)
#         )
#         for pattern in combination_patterns:
#             listed_pattern = list(pattern)
#             buffer_string = string
#             index_shift = 0
#             for i in range(0, len(listed_pattern)):
#                 if listed_pattern[i] == 0:
#                     buffer_string = buffer_string[:list_of_indexes_to_alternate[i]-index_shift] + \
#                                     buffer_string[list_of_indexes_to_alternate[i]-index_shift+1:]
#                     index_shift += 1
#             p_i_right_part.add(buffer_string)
#     else:
#         p_i_right_part.add(string)
#     if dict_key in dict_of_p_i.keys():
#         dict_of_p_i[dict_key].update(p_i_right_part)
#         dict_of_p_i[dict_key] = set(dict_of_p_i[dict_key])
#     else:
#         dict_of_p_i[dict_key] = p_i_right_part

# def wipeExcessLambdaRules(grammar: Gr) -> Gr:
#     """
#     Алгоритм устранения лишних лямбда-правил!
#     ---
#     Некоторые понятия в комментариях могут быть Вам незнакомы.
#     Это потому что я их сам придумал! Определения им даю почти сразу при употреблении.
#     """
#     """
#     1-й шаг.
#     n_lambda - все нетерминалы, из которых выводятся лямбда-цепочки.
#     n_term_plus - все нетерминалы, из которых выводятся непустые терминальные цепочки.
#     """
#     n_lambda = set()
#     n_term_plus = set()
#     """
#     А-й подшаг 1-го шага.
#     Поиск и добавление нечистых и чистых первородных лямбда-нетерминалов. 
#     Нечистые первородные лямбда-нетерминалы - нетерминалы, из которых непосредственно выводится НЕ ТОЛЬКО лямбда.
#     Пример: A -> λ | a.
#     Чистые первородные лямбда-нетерминалы - нетерминалы, из которых непосредственно выводится ТОЛЬКО лямбда.
#     Пример: A -> λ.
    
#     Чистые первородные лямбда-нетерминалы также добавим в множество pure_n_lambda. 
#     Такие нетерминалы точно не окажутся в n_term_plus.
#     """
#     count_of_all_lambda_consequents: int
#     pure_n_lambda = set()
#     for non_term in grammar.N:
#         if non_term not in grammar.P.keys():
#             continue
#         if '' in grammar.P[non_term]:
#             n_lambda.add(non_term)
#             if len(grammar.P[non_term]) == 1:
#                 pure_n_lambda.add(non_term)

#     """
#     Б-й подшаг 1-го шага.
#     Поиск и добавление нечистых и чистых старшеродных лямбда-нетерминалов. 
#     Нечистые старшеродные лямбда-нетерминалы - нетерминалы, из которых транзитивно выводится НЕ ТОЛЬКО лямбда.
#     Пример: A -> λ | a.
#     Чистые старшеродные лямбда-нетерминалы - нетерминалы, из которых транзитивно выводится ТОЛЬКО лямбда.
#     Пример: A -> λ.
#     Чистые старшеродные лямбда-нетерминалы также добавим в множество pure_n_lambda. 
#     Такие нетерминалы точно не окажутся в n_term_plus.
#     """
#     while True:
#         is_n_lambda_appended = False
#         for non_term in grammar.N:
#             if not(non_term in grammar.P.keys() and non_term not in n_lambda):
#                 continue
#             count_of_all_lambda_consequents = 0
#             count_of_pure_lambda_consequents = 0
#             for consequent in grammar.P[non_term]:
#                 for symbol in consequent:
#                     if symbol in n_lambda:
#                         count_of_all_lambda_consequents += consequent.count(symbol)
#                         if symbol in pure_n_lambda:
#                             count_of_pure_lambda_consequents += consequent.count(symbol)
#                 if len(consequent) == count_of_all_lambda_consequents:
#                     n_lambda.add(non_term)
#                     is_n_lambda_appended = True
#                     if len(consequent) == count_of_pure_lambda_consequents:
#                         pure_n_lambda.add(non_term)
#         if not is_n_lambda_appended:
#             break

#     """
#     В-й подшаг 1-го шага.
#     Поиск и добавление нетерминалов, из которых выводятся 
#     непустые терминальные цепочки, в n_term_plus.
#     """
#     for non_term in grammar.N:
#         if non_term in grammar.P.keys() and non_term not in pure_n_lambda:
#             n_term_plus.add(non_term)

#     """
#     2-й шаг.
#     new_rules - новый набор правил.
#     """
#     new_rules: dict = {}

#     """
#     3-й шаг.
#     Найдём q - множество всех правил, в правых частях которых есть символы n_lambda
#     """
#     q: dict = {}

#     for key in grammar.P:
#         is_key_added = False
#         for string in grammar.P[key]:
#             for symbol in n_lambda:
#                 if string.find(symbol) > -1:
#                     q[key] = grammar.P[key]
#                     is_key_added = True
#                     break
#             if is_key_added:
#                 break
#         if is_key_added:
#             continue

#     """
#     Добавим dict_of_p_i - множество правил на основе каждого i-го правила из q.
#     Причём из каждого нового правила выводятся непустые цепочки
#     """
#     dict_of_p_i: dict = {}
#     list_of_indexes_to_alternate: list[int]
#     for key in q:
#         for string in q[key]:
#             i = 0
#             list_of_indexes_to_alternate = []
#             string_length = len(string)
#             while i < string_length:
#                 if string[i] in n_lambda and string[i] in n_term_plus:
#                     list_of_indexes_to_alternate.append(i)
#                     i += 1
#                 elif string[i] in n_lambda:
#                     string = string[:i] + string[i+1:]
#                     string_length -= 1
#                 else:
#                     i += 1
#             if len(string) > 0:
#                 __add_new_rules_to_dict_of_p_i(dict_of_p_i,
#                                                     key,
#                                                     string,
#                                                     list_of_indexes_to_alternate)

#     """
#     Шаг 4.
#     Добавляем в new_p все правила вида B -> a, где a не содержит символов из n_lambda
#     и a != lambda.
#     """
#     for key in grammar.P:
#         if key in n_lambda:
#             continue
#         is_non_lambda = True
#         for consequents in grammar.P[key]:
#             for consequent in consequents:
#                 for symbol in n_lambda:
#                     if consequent.find(symbol) > -1:
#                         is_non_lambda = False
#                         break
#                 if not is_non_lambda:
#                     break
#             if not is_non_lambda:
#                 break
#         if is_non_lambda:
#             new_rules[key] = grammar.P[key]
#     for key in dict_of_p_i:
#         new_rules[key] = dict_of_p_i[key]

#     """
#     Шаг 5.
#     Проверяем аксиому.
#     Если S = lambda || S принадл. n_lambda, 
#     то добавим в new_p правило new_axiom -> S|lambda
#     """
#     new_axiom: str = grammar.S
#     if grammar.S == "" or grammar.S in n_lambda:
#         new_axiom = "new_" + grammar.S
#         new_rules[new_axiom] = {grammar.S, ""}

#     """
#     Шаг 6.
#     Формируем новую грамматику.
#     """

#     new_non_terminals = n_term_plus
#     new_non_terminals.add(new_axiom)

#     return Gr(new_non_terminals, grammar.T, new_rules, new_axiom)
