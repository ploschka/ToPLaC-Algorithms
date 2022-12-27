from alg.isLanguageEmpty import isLanguageEmpty
from alg.unreachableSymbols import unreachableSymbols
from alg.uselessSymbols import uselessSymbols
from alg.chomskyNormalForm import chomskyNormalForm

from grammar import Grammar as Gr
from mytoken import *
from mytoken import MyToken as Tk

import unittest


class TestIsLanguageEmpty(unittest.TestCase):
    def test_classic(self):
        input_g = Gr({"E", "T", "F"},  # Нетерминалы
                     {"a", "+", "*", "(", ")"},  # Терминалы
                     {  # Правила вывода
                         Tk(TOKEN_NONTERM, "E"): {(Tk(TOKEN_NONTERM, "E"), Tk(TOKEN_TERM, "+"), Tk(TOKEN_NONTERM, "T")),
                                                  (Tk(TOKEN_NONTERM, "T"),)},
                         Tk(TOKEN_NONTERM, "T"): {(Tk(TOKEN_NONTERM, "T"), Tk(TOKEN_TERM, "*"), Tk(TOKEN_NONTERM, "F")),
                                                  (Tk(TOKEN_NONTERM, "F"),)},
                         Tk(TOKEN_NONTERM, "F"): {(Tk(TOKEN_TERM, "("), Tk(TOKEN_NONTERM, "E"), Tk(TOKEN_TERM, ")")),
                                                  (Tk(TOKEN_TERM, "a"),)},
                     },
                     "E"  # Аксиома
                     )
        expected_answer = False
        self.assertEqual(
            isLanguageEmpty(input_g)[0],
            expected_answer
        )

    def test_classic_missing_rule(self):
        input_g = Gr({"E", "T", "F"},  # Нетерминалы
                     {"a", "+", "*", "(", ")"},  # Терминалы
                     {  # Правила вывода
                         Tk(TOKEN_NONTERM, "E"): {(Tk(TOKEN_NONTERM, "E"), Tk(TOKEN_TERM, "+"), Tk(TOKEN_NONTERM, "T")),
                                                  (Tk(TOKEN_NONTERM, "T"),)},
                         Tk(TOKEN_NONTERM, "F"): {(Tk(TOKEN_TERM, "("), Tk(TOKEN_NONTERM, "E"), Tk(TOKEN_TERM, ")")),
                                                  (Tk(TOKEN_TERM, "a"),)},
                     },
                     "E")  # Аксиома
        expected_answer = True
        self.assertEqual(
            isLanguageEmpty(input_g)[0],
            expected_answer
        )

    def test_no_rules(self):
        input_g = Gr({"E", "T", "F"},  # Нетерминалы
                     {"a", "+", "*", "(", ")"},  # Терминалы
                     dict(),  # Правила вывода
                     "E")  # Аксиома
        expected_answer = True
        self.assertEqual(
            isLanguageEmpty(input_g)[0],
            expected_answer
        )

    def test_immediate_terminal(self):
        input_g = Gr({"E", "T", "F"},  # Нетерминалы
                     {"a", "+", "*", "(", ")"},  # Терминалы
                     {  # Правила вывода
                         Tk(TOKEN_NONTERM, "E"): {(Tk(TOKEN_TERM, "a"),)},
                     },
                     "E")  # Аксиома
        expected_answer = False
        self.assertEqual(
            isLanguageEmpty(input_g)[0],
            expected_answer
        )

    def test_cycle(self):
        input_g = Gr({"A", "B", "C"},  # Нетерминалы
                     set(),  # Терминалы
                     {  # Правила вывода
                         Tk(TOKEN_NONTERM, "A"): {(Tk(TOKEN_NONTERM, "B"),)},
                         Tk(TOKEN_NONTERM, "B"): {(Tk(TOKEN_NONTERM, "C"),)},
                         Tk(TOKEN_NONTERM, "C"): {(Tk(TOKEN_NONTERM, "A"),)},
                     },
                     "A")  # Аксиома
        expected_answer = True
        self.assertEqual(
            isLanguageEmpty(input_g)[0],
            expected_answer
        )

    def test_repeating_chars(self):
        input_g = Gr({"A", "B", "C"},  # Нетерминалы
                     {"a", "b", "c"},  # Терминалы
                     {  # Правила вывода
                         Tk(TOKEN_NONTERM, "A"): {(Tk(TOKEN_NONTERM, "B"), Tk(TOKEN_TERM, "a"), Tk(TOKEN_TERM, "a"),
                                                   Tk(TOKEN_NONTERM, "B"))},
                         Tk(TOKEN_NONTERM, "B"): {(Tk(TOKEN_NONTERM, "C"), Tk(TOKEN_TERM, "c"), Tk(TOKEN_NONTERM, "C"),
                                                   Tk(TOKEN_TERM, "c"), Tk(TOKEN_NONTERM, "C"))},
                         Tk(TOKEN_NONTERM, "C"): {(Tk(TOKEN_TERM, "c"), Tk(TOKEN_TERM, "c"), Tk(TOKEN_TERM, "c"))},
                     },
                     "A")  # Аксиома
        expected_answer = False
        self.assertEqual(
            isLanguageEmpty(input_g)[0],
            expected_answer
        )

    def test_many_nonterminals(self):
        input_g = Gr({"A", "B", "C", "O"},  # Нетерминалы
                     {"a", "b", "c", "o"},  # Терминалы
                     {  # Правила вывода
                         Tk(TOKEN_NONTERM, "A"): {(Tk(TOKEN_NONTERM, "A"), Tk(TOKEN_NONTERM, "B"),
                                                   Tk(TOKEN_NONTERM, "O"), Tk(TOKEN_NONTERM, "B"),
                                                   Tk(TOKEN_NONTERM, "A")),
                                                  (Tk(TOKEN_NONTERM, "A"), Tk(TOKEN_NONTERM, "B"),
                                                   Tk(TOKEN_NONTERM, "B"), Tk(TOKEN_NONTERM, "A")),
                                                  (Tk(TOKEN_NONTERM, "B"),)},
                         Tk(TOKEN_NONTERM, "B"): {
                             (Tk(TOKEN_NONTERM, "C"), Tk(TOKEN_TERM, "o"), Tk(TOKEN_NONTERM, "C"), Tk(TOKEN_TERM, "a")),
                             (Tk(TOKEN_NONTERM, "B"), Tk(TOKEN_TERM, "b"))},
                         Tk(TOKEN_NONTERM, "C"): {(Tk(TOKEN_TERM, "c"), Tk(TOKEN_TERM, "c"), Tk(TOKEN_TERM, "c"))},
                         Tk(TOKEN_NONTERM, "O"): {(Tk(TOKEN_TERM, "a"), Tk(TOKEN_TERM, "b"), Tk(TOKEN_NONTERM, "O"),
                                                   Tk(TOKEN_TERM, "b"), Tk(TOKEN_TERM, "a")),
                                                  (Tk(TOKEN_NONTERM, "A"),)},
                     },
                     "A")  # Аксиома
        expected_answer = False
        self.assertEqual(
            isLanguageEmpty(input_g)[0],
            expected_answer
        )


class TestUnreachableSymbols(unittest.TestCase):
    def test_classic(self):
        input_g = Gr({"E", "T", "F"},  # Нетерминалы
                     {"a", "+", "*", "(", ")"},  # Терминалы
                     {  # Правила вывода
                         Tk(TOKEN_NONTERM, "E"): {(Tk(TOKEN_NONTERM, "E"), Tk(TOKEN_TERM, "+"), Tk(TOKEN_NONTERM, "T")),
                                                  (Tk(TOKEN_NONTERM, "T"),)},
                         Tk(TOKEN_NONTERM, "T"): {(Tk(TOKEN_NONTERM, "T"), Tk(TOKEN_TERM, "*"), Tk(TOKEN_NONTERM, "F")),
                                                  (Tk(TOKEN_NONTERM, "F"),)},
                         Tk(TOKEN_NONTERM, "F"): {(Tk(TOKEN_TERM, "("), Tk(TOKEN_NONTERM, "E"), Tk(TOKEN_TERM, ")")),
                                                  (Tk(TOKEN_TERM, "a"),)},
                     },
                     "E")  # Аксиома
        expected_g = Gr({"E", "T", "F"},  # Нетерминалы
                        {"a", "+", "*", "(", ")"},  # Терминалы
                        {  # Правила вывода
                            Tk(TOKEN_NONTERM, "E"): {
                                (Tk(TOKEN_NONTERM, "E"), Tk(TOKEN_TERM, "+"), Tk(TOKEN_NONTERM, "T")),
                                (Tk(TOKEN_NONTERM, "T"),)},
                            Tk(TOKEN_NONTERM, "T"): {
                                (Tk(TOKEN_NONTERM, "T"), Tk(TOKEN_TERM, "*"), Tk(TOKEN_NONTERM, "F")),
                                (Tk(TOKEN_NONTERM, "F"),)},
                            Tk(TOKEN_NONTERM, "F"): {(Tk(TOKEN_TERM, "("), Tk(TOKEN_NONTERM, "E"), Tk(TOKEN_TERM, ")")),
                                                     (Tk(TOKEN_TERM, "a"),)},
                        },
                        "E")  # Аксиома

        self.assertEqual(
            unreachableSymbols(input_g),
            expected_g
        )
        # self.assertEqual(
        #     unreachableSymbolsShort(input_g),
        #     expected_g
        # )

    def test_classic_missing_rule(self):
        input_g = Gr({"E", "T", "F"},  # Нетерминалы
                     {"a", "+", "*", "(", ")"},  # Терминалы
                     {  # Правила вывода
                         Tk(TOKEN_NONTERM, "E"): {(Tk(TOKEN_NONTERM, "E"), Tk(TOKEN_TERM, "+"), Tk(TOKEN_NONTERM, "T")),
                                                  (Tk(TOKEN_NONTERM, "T"),)},
                         Tk(TOKEN_NONTERM, "F"): {(Tk(TOKEN_TERM, "("), Tk(TOKEN_NONTERM, "E"), Tk(TOKEN_TERM, ")")),
                                                  (Tk(TOKEN_TERM, "a"),)},
                     },
                     "E")  # Аксиома
        expected_g = Gr({"E", "T"},  # Нетерминалы
                        {"+"},  # Терминалы
                        {  # Правила вывода
                            Tk(TOKEN_NONTERM, "E"): {
                                (Tk(TOKEN_NONTERM, "E"), Tk(TOKEN_TERM, "+"), Tk(TOKEN_NONTERM, "T")),
                                (Tk(TOKEN_NONTERM, "T"),)},
                        },
                        "E")  # Аксиома
        self.assertEqual(
            unreachableSymbols(input_g),
            expected_g
        )
        # self.assertEqual(
        #     unreachableSymbolsShort(input_g),
        #     expected_g
        # )


# class TestExcessLambdaRules(unittest.TestCase):
#     def test_classic1(self):
#         input_g = Gr(
#             {'A', 'B', 'M', 'N', 'K', 'S'},
#             {'a', 'b'},
#             {  # Правила вывода
#                 'A': {''},
#                 'B': {''},
#                 'M': {'AB'},
#                 'N': {'Ab'},
#                 'K': {'ab'},
#                 'S': {'KNM'}
#             },
#             'S'
#         )
#         expected_g = Gr(
#             {'N', 'K', 'S'},
#             {'a', 'b'},
#             {  # Правила вывода
#                 'N': {'b'},
#                 'K': {'ab'},
#                 'S': {'KN'},
#             },
#             'S'
#         )

#         self.assertEqual(
#             wipeExcessLambdaRules(input_g),
#             expected_g
#         )

#     def test_classic2(self):
#         input_g = Gr(
#             {'A', 'B', 'M', 'N', 'K', 'S'},
#             {'a', 'b', 'c', 'p'},
#             {  # Правила вывода
#                 'A': {'', 'c'},
#                 'B': {'', 'p'},
#                 'M': {'AB'},
#                 'N': {'Ab'},
#                 'K': {'ab'},
#                 'S': {'KNM'},
#             },
#             'S'
#         )
#         expected_g = Gr(
#             {'A', 'B', 'M', 'N', 'K', 'S'},
#             {'a', 'b', 'c', 'p'},
#             {  # Правила вывода
#                 'A': {'c'},
#                 'B': {'p'},
#                 'M': {'AB', 'A', 'B'},
#                 'N': {'Ab', 'b'},
#                 'K': {'ab'},
#                 'S': {'KNM', 'KN'},
#             },
#             'S'
#         )

#         self.assertEqual(
#             wipeExcessLambdaRules(input_g),
#             expected_g
#         )

#     def test_classic3(self):
#         input_g = Gr(
#             {'S'},
#             {'a', 'b'},
#             {  # Правила вывода
#                 'S': {'aSbS', 'bSaS', ''}
#             },
#             'S'
#         )
#         expected_g = Gr(
#             {'S', 'new_S'},
#             {'a', 'b'},
#             {  # Правила вывода
#                 'S': {'aSbS', 'abS', 'aSb', 'ab', 'bSaS', 'bSa', 'baS', 'ba'},
#                 'new_S': {'', 'S'}
#             },
#             'new_S'
#         )

#         self.assertEqual(
#             wipeExcessLambdaRules(input_g),
#             expected_g
#         )

#     def test_no_lambda_rules(self):
#         input_g = Gr(
#             {'S', 'new_S'},
#             {'a', 'b'},
#             {  # Правила вывода
#                 'S': {'aSbS', 'abS', 'aSb', 'ab', 'bSaS', 'bSa', 'baS', 'ba'},
#                 'new_S': {'', 'S'}
#             },
#             'new_S'
#         )
#         expected_g = Gr(
#             {'S', 'new_S'},
#             {'a', 'b'},
#             {  # Правила вывода
#                 'S': {'aSbS', 'abS', 'aSb', 'ab', 'bSaS', 'bSa', 'baS', 'ba'},
#                 'new_S': {'', 'S'}
#             },
#             'new_S'
#         )

#         self.assertEqual(
#             wipeExcessLambdaRules(input_g),
#             expected_g
#         )

#     def test_empty_language(self):
#         input_g = Gr(
#             {'S', 'E', 'M'},
#             {'a', 'b', 'c'},
#             {  # Правила вывода
#                 'E': {''},
#                 'M': {''},
#                 'S': {'E', 'M', ''},
#             },
#             'S'
#         )
#         expected_g = Gr(
#             {'S'},
#             {'a', 'b', 'c'},
#             {  # Правила вывода
#                 'S': {''},
#             },
#             'S'
#         )

#         self.assertEqual(
#             wipeExcessLambdaRules(input_g),
#             expected_g
#         )


class TestChomskyNormalForm(unittest.TestCase):
    def test_example1(self):
        """
            S -> aAB | BA
            A -> BBB | a
            B -> AS | b
        """
        input_g = Gr(
            {"S", "A", "B"},
            {"a", "b"},
            {
                Tk(TOKEN_NONTERM, "S"): {
                    (Tk(TOKEN_TERM, "a"), Tk(TOKEN_NONTERM, "A"), Tk(TOKEN_NONTERM, "B")),
                    (Tk(TOKEN_NONTERM, "B"), Tk(TOKEN_NONTERM, "A")),
                },
                Tk(TOKEN_NONTERM, "A"): {
                    (Tk(TOKEN_NONTERM, "B"), Tk(TOKEN_NONTERM, "B"), Tk(TOKEN_NONTERM, "B")),
                    (Tk(TOKEN_TERM, "a"),),
                },
                Tk(TOKEN_NONTERM, "B"): {
                    (Tk(TOKEN_NONTERM, "A"), Tk(TOKEN_NONTERM, "S")),
                    (Tk(TOKEN_TERM, "b"),),
                },
            },
            "S"
        )

        """
            S -> <a`><AB> | BA
            A -> B<BB> | a
            B -> AS | b
            <a`> -> a
            <AB> -> AB
            <BB> -> BB
        """
        expected_g = Gr(
            {"S", "A", "B", "BB", "AB", "a`"},
            {"a", "b"},
            {
                Tk(TOKEN_NONTERM, "S"): {
                    (Tk(TOKEN_NONTERM, "a`"), Tk(TOKEN_NONTERM, "AB")),
                    (Tk(TOKEN_NONTERM, "B"), Tk(TOKEN_NONTERM, "A")),
                },
                Tk(TOKEN_NONTERM, "A"): {
                    (Tk(TOKEN_NONTERM, "B"), Tk(TOKEN_NONTERM, "BB")),
                    (Tk(TOKEN_TERM, "a"),),
                },
                Tk(TOKEN_NONTERM, "B"): {
                    (Tk(TOKEN_NONTERM, "A"), Tk(TOKEN_NONTERM, "S"),),
                    (Tk(TOKEN_TERM, "b"),),
                },
                Tk(TOKEN_NONTERM, "a`"): {
                    (Tk(TOKEN_TERM, "a"),),
                },
                Tk(TOKEN_NONTERM, "AB"): {
                    (Tk(TOKEN_NONTERM, "A"), Tk(TOKEN_NONTERM, "B")),
                },
                Tk(TOKEN_NONTERM, "BB"): {
                    (Tk(TOKEN_NONTERM, "B"), Tk(TOKEN_NONTERM, "B")),
                },
            },
            "S"
        )
        self.assertEqual(
            chomskyNormalForm(input_g),
            expected_g
        )

    def test_example2(self):
        """
            S -> aA | λ
            A -> BBB | AB | a
            B -> b
        """
        input_g = Gr(
            {"S", "A", "B"},
            {"a", "b"},
            {
                Tk(TOKEN_NONTERM, "S"): {
                    (Tk(TOKEN_TERM, "a"), Tk(TOKEN_NONTERM, "A")),
                    (Tk(TOKEN_TERM, ""),),
                },
                Tk(TOKEN_NONTERM, "A"): {
                    (Tk(TOKEN_NONTERM, "B"), Tk(TOKEN_NONTERM, "B"), Tk(TOKEN_NONTERM, "B")),
                    (Tk(TOKEN_NONTERM, "A"), Tk(TOKEN_NONTERM, "B")),
                    (Tk(TOKEN_TERM, "a"),),
                },
                Tk(TOKEN_NONTERM, "B"): {
                    (Tk(TOKEN_TERM, "b"),),
                },
            },
            "S"
        )

        """
            S -> <a`>A | λ
            A -> B<BB> | AB | a
            B -> b
            <a`> -> a
            <BB> -> BB
        """
        expected_g = Gr(
            {"S", "A", "B", "BB", "a`"},
            {"a", "b"},
            {
                Tk(TOKEN_NONTERM, "S"): {
                    (Tk(TOKEN_NONTERM, "a`"), Tk(TOKEN_NONTERM, "A")),
                    (Tk(TOKEN_TERM, ""),),
                },
                Tk(TOKEN_NONTERM, "A"): {
                    (Tk(TOKEN_NONTERM, "B"), Tk(TOKEN_NONTERM, "BB")),
                    (Tk(TOKEN_NONTERM, "A"), Tk(TOKEN_NONTERM, "B")),
                    (Tk(TOKEN_TERM, "a"),),
                },
                Tk(TOKEN_NONTERM, "B"): {
                    (Tk(TOKEN_TERM, "b"),),
                },
                Tk(TOKEN_NONTERM, "a`"): {
                    (Tk(TOKEN_TERM, "a"),),
                },
                Tk(TOKEN_NONTERM, "BB"): {
                    (Tk(TOKEN_NONTERM, "B"), Tk(TOKEN_NONTERM, "B")),
                },
            },
            "S"
        )
        self.assertEqual(
            chomskyNormalForm(input_g),
            expected_g
        )

    def test_no_changes(self):
        """
            S -> AB
            A -> AA | a
            B -> b
        """
        input_g = Gr(
            {"S", "A", "B"},
            {"a", "b"},
            {
                Tk(TOKEN_NONTERM, "S"): {
                    (Tk(TOKEN_NONTERM, "A"), Tk(TOKEN_NONTERM, "B")),
                },
                Tk(TOKEN_NONTERM, "A"): {
                    (Tk(TOKEN_NONTERM, "A"), Tk(TOKEN_NONTERM, "A")),
                    (Tk(TOKEN_TERM, "a"),),
                },
                Tk(TOKEN_NONTERM, "B"): {
                    (Tk(TOKEN_TERM, "b"),),
                },
            },
            "S"
        )

        """
            S -> AB
            A -> AA | a
            B -> b
        """
        expected_g = Gr(
            {"S", "A", "B"},
            {"a", "b"},
            {
                Tk(TOKEN_NONTERM, "S"): {
                    (Tk(TOKEN_NONTERM, "A"), Tk(TOKEN_NONTERM, "B")),
                },
                Tk(TOKEN_NONTERM, "A"): {
                    (Tk(TOKEN_NONTERM, "A"), Tk(TOKEN_NONTERM, "A")),
                    (Tk(TOKEN_TERM, "a"),),
                },
                Tk(TOKEN_NONTERM, "B"): {
                    (Tk(TOKEN_TERM, "b"),),
                },
            },
            "S"
        )
        self.assertEqual(
            chomskyNormalForm(input_g),
            expected_g
        )

    def test_many_terminals(self):
        """
            S -> aaaaa
        """
        input_g = Gr(
            {"S", },
            {"a", },
            {
                Tk(TOKEN_NONTERM, "S"): {
                    (Tk(TOKEN_TERM, "a"), Tk(TOKEN_TERM, "a"), Tk(TOKEN_TERM, "a"), Tk(TOKEN_TERM, "a"), Tk(TOKEN_TERM, "a")),
                },
            },
            "S"
        )

        """
            S -> <a`><aaaa>
            <a`> -> a
            <aaaa> -> <a`><aaa>
            <aaa> -> <a`><aa>
            <aa> -> <a`><a`>
        """
        expected_g = Gr(
            {"S", "a`", "aaaa", "aaa", "aa"},
            {"a", },
            {
                Tk(TOKEN_NONTERM, "S"): {
                    (Tk(TOKEN_NONTERM, "a`"), Tk(TOKEN_NONTERM, "aaaa")),
                },
                Tk(TOKEN_NONTERM, "a`"): {
                    (Tk(TOKEN_TERM, "a"),),
                },
                Tk(TOKEN_NONTERM, "aaaa"): {
                    (Tk(TOKEN_NONTERM, "a`"), Tk(TOKEN_NONTERM, "aaa")),
                },
                Tk(TOKEN_NONTERM, "aaa"): {
                    (Tk(TOKEN_NONTERM, "a`"), Tk(TOKEN_NONTERM, "aa")),
                },
                Tk(TOKEN_NONTERM, "aa"): {
                    (Tk(TOKEN_NONTERM, "a`"), Tk(TOKEN_NONTERM, "a`")),
                },
            },
            "S"
        )
        self.assertEqual(
            chomskyNormalForm(input_g),
            expected_g
        )

    def test_terminal_second(self):
        """
            S -> Aa
        """
        input_g = Gr(
            {"S", "A"},
            {"a", },
            {
                Tk(TOKEN_NONTERM, "S"): {
                    (Tk(TOKEN_NONTERM, "A"), Tk(TOKEN_TERM, "a")),
                },
            },
            "S"
        )

        """
            S -> A<a`>
            <a`> -> a
        """
        expected_g = Gr(
            {"S", "A", "a`"},
            {"a", },
            {
                Tk(TOKEN_NONTERM, "S"): {
                    (Tk(TOKEN_NONTERM, "A"), Tk(TOKEN_NONTERM, "a`")),
                },
                Tk(TOKEN_NONTERM, "a`"): {
                    (Tk(TOKEN_TERM, "a"),),
                },
            },
            "S"
        )
        self.assertEqual(
            chomskyNormalForm(input_g),
            expected_g
        )


unittest.main()
